from __future__ import absolute_import

import sys

from sentry_sdk._compat import reraise
from sentry_sdk._types import TYPE_CHECKING
from sentry_sdk import Hub
from sentry_sdk.consts import OP
from sentry_sdk.hub import _should_send_default_pii
from sentry_sdk.integrations import DidNotEnable, Integration
from sentry_sdk.integrations.logging import ignore_logger
from sentry_sdk.tracing import Transaction, TRANSACTION_SOURCE_TASK
from sentry_sdk.utils import (
    capture_internal_exceptions,
    event_from_exception,
    SENSITIVE_DATA_SUBSTITUTE,
)

try:
    import arq.worker
    from arq.version import VERSION as ARQ_VERSION
    from arq.connections import ArqRedis
    from arq.worker import JobExecutionFailed, Retry, RetryJob, Worker
except ImportError:
    raise DidNotEnable("Arq is not installed")

if TYPE_CHECKING:
    from typing import Any, Dict, Optional

    from sentry_sdk._types import EventProcessor, SentryEvent, ExcInfo, Hint

    from arq.jobs import Job
    from arq.typing import WorkerCoroutine
    from arq.worker import Function

ARQ_CONTROL_FLOW_EXCEPTIONS = (JobExecutionFailed, Retry, RetryJob)


class ArqIntegration(Integration):
    identifier = "arq"

    @staticmethod
    def setup_once():
        # type: () -> None

        try:
            if isinstance(ARQ_VERSION, str):
                version = tuple(map(int, ARQ_VERSION.split(".")[:2]))
            else:
                version = ARQ_VERSION.version[:2]
        except (TypeError, ValueError):
            raise DidNotEnable("arq version unparsable: {}".format(ARQ_VERSION))

        if version < (0, 23):
            raise DidNotEnable("arq 0.23 or newer required.")

        patch_enqueue_job()
        patch_run_job()
        patch_func()

        ignore_logger("arq.worker")


def patch_enqueue_job():
    # type: () -> None
    old_enqueue_job = ArqRedis.enqueue_job

    async def _sentry_enqueue_job(self, function, *args, **kwargs):
        # type: (ArqRedis, str, *Any, **Any) -> Optional[Job]
        hub = Hub.current

        if hub.get_integration(ArqIntegration) is None:
            return await old_enqueue_job(self, function, *args, **kwargs)

        with hub.start_span(op=OP.QUEUE_SUBMIT_ARQ, description=function):
            return await old_enqueue_job(self, function, *args, **kwargs)

    ArqRedis.enqueue_job = _sentry_enqueue_job


def patch_run_job():
    # type: () -> None
    old_run_job = Worker.run_job

    async def _sentry_run_job(self, job_id, score):
        # type: (Worker, str, int) -> None
        hub = Hub(Hub.current)

        if hub.get_integration(ArqIntegration) is None:
            return await old_run_job(self, job_id, score)

        with hub.push_scope() as scope:
            scope._name = "arq"
            scope.clear_breadcrumbs()

            transaction = Transaction(
                name="unknown arq task",
                status="ok",
                op=OP.QUEUE_TASK_ARQ,
                source=TRANSACTION_SOURCE_TASK,
            )

            with hub.start_transaction(transaction):
                return await old_run_job(self, job_id, score)

    Worker.run_job = _sentry_run_job


def _capture_exception(exc_info):
    # type: (ExcInfo) -> None
    hub = Hub.current

    if hub.scope.transaction is not None:
        if exc_info[0] in ARQ_CONTROL_FLOW_EXCEPTIONS:
            hub.scope.transaction.set_status("aborted")
            return

        hub.scope.transaction.set_status("internal_error")

    event, hint = event_from_exception(
        exc_info,
        client_options=hub.client.options if hub.client else None,
        mechanism={"type": ArqIntegration.identifier, "handled": False},
    )
    hub.capture_event(event, hint=hint)


def _make_event_processor(ctx, *args, **kwargs):
    # type: (Dict[Any, Any], *Any, **Any) -> EventProcessor
    def event_processor(event, hint):
        # type: (SentryEvent, Hint) -> Optional[SentryEvent]

        hub = Hub.current

        with capture_internal_exceptions():
            if hub.scope.transaction is not None:
                hub.scope.transaction.name = ctx["job_name"]
                event["transaction"] = ctx["job_name"]

            tags = event.setdefault("tags", {})
            tags["arq_task_id"] = ctx["job_id"]
            tags["arq_task_retry"] = ctx["job_try"] > 1
            extra = event.setdefault("extra", {})
            extra["arq-job"] = {
                "task": ctx["job_name"],
                "args": args
                if _should_send_default_pii()
                else SENSITIVE_DATA_SUBSTITUTE,
                "kwargs": kwargs
                if _should_send_default_pii()
                else SENSITIVE_DATA_SUBSTITUTE,
                "retry": ctx["job_try"],
            }

        return event

    return event_processor


def _wrap_coroutine(name, coroutine):
    # type: (str, WorkerCoroutine) -> WorkerCoroutine
    async def _sentry_coroutine(ctx, *args, **kwargs):
        # type: (Dict[Any, Any], *Any, **Any) -> Any
        hub = Hub.current
        if hub.get_integration(ArqIntegration) is None:
            return await coroutine(*args, **kwargs)

        hub.scope.add_event_processor(
            _make_event_processor({**ctx, "job_name": name}, *args, **kwargs)
        )

        try:
            result = await coroutine(ctx, *args, **kwargs)
        except Exception:
            exc_info = sys.exc_info()
            _capture_exception(exc_info)
            reraise(*exc_info)

        return result

    return _sentry_coroutine


def patch_func():
    # type: () -> None
    old_func = arq.worker.func

    def _sentry_func(*args, **kwargs):
        # type: (*Any, **Any) -> Function
        hub = Hub.current

        if hub.get_integration(ArqIntegration) is None:
            return old_func(*args, **kwargs)

        func = old_func(*args, **kwargs)

        if not getattr(func, "_sentry_is_patched", False):
            func.coroutine = _wrap_coroutine(func.name, func.coroutine)
            func._sentry_is_patched = True

        return func

    arq.worker.func = _sentry_func
