from logging import LogRecord


try:
    from typing import TYPE_CHECKING as TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False


# Re-exported for compat, since code out there in the wild might use this variable.
MYPY = TYPE_CHECKING


if TYPE_CHECKING:
    import datetime
    from types import TracebackType
    from typing import Any
    from typing import Callable
    from typing import Optional
    from typing import Type
    from typing import Union
    from typing_extensions import Literal
    from typing import NotRequired
    from typing import TypedDict
    from opentelemetry.trace import SpanContext
    from typing import Dict, Tuple

    ExcInfo = Tuple[
        Optional[Type[BaseException]], Optional[BaseException], Optional[TracebackType]
    ]

    class AppContext(TypedDict):
        app_name: NotRequired[str]
        app_start_time: NotRequired[str]
        app_version: NotRequired[str]
        app_identifier: NotRequired[str]
        build_type: NotRequired[str]
        app_memory: NotRequired[int]

    class Device(TypedDict):
        name: NotRequired[str]
        family: NotRequired[str]
        model: NotRequired[str]
        model_id: NotRequired[str]
        architecture: NotRequired[str]
        battery_level: NotRequired[float]
        orientation: NotRequired[Literal["portrait", "landscape"]]
        manufacturer: NotRequired[str]
        brand: NotRequired[str]
        screen_height_pixels: NotRequired[int]
        screen_width_pixels: NotRequired[int]
        screen_density: NotRequired[float]
        screen_dpi: NotRequired[int]
        online: NotRequired[bool]
        charging: NotRequired[bool]
        low_memory: NotRequired[bool]
        simulator: NotRequired[bool]
        memory_size: NotRequired[int]
        free_memory: NotRequired[int]
        usable_memory: NotRequired[int]
        storage_size: NotRequired[int]
        free_storage: NotRequired[int]
        external_storage_size: NotRequired[int]
        external_free_storage: NotRequired[int]
        boot_time: NotRequired[str]
        processor_count: NotRequired[int]
        cpu_description: NotRequired[str]
        processor_frequency: NotRequired[float]
        device_type: NotRequired[str]
        battery_status: NotRequired[str]
        device_unique_identifier: NotRequired[str]
        supports_vibration: NotRequired[bool]
        supports_accelerometer: NotRequired[bool]
        supports_gyroscope: NotRequired[bool]
        supports_audio: NotRequired[bool]
        supports_location_service: NotRequired[bool]

    class OperatingSystem(TypedDict):
        name: NotRequired[str]
        version: NotRequired[str]
        build: NotRequired[str]
        kernel_version: NotRequired[str]

    class CultureContext(TypedDict):
        calendar: NotRequired[str]
        display_name: NotRequired[str]
        locale: NotRequired[str]
        is_24_hour_format: NotRequired[bool]
        timezone: NotRequired[datetime.timezone]

    class ResponseContext(TypedDict):
        type: NotRequired[str]
        cookies: NotRequired[dict[list[list[str]]] | dict[str, str]]
        headers: NotRequired[dict[str, str]]
        status_code: int
        body_size: int

    class SentryRuntime(TypedDict):
        name: NotRequired[str]
        version: NotRequired[str]
        raw_description: NotRequired[str]

    class Contexts(TypedDict):
        app: NotRequired[AppContext]
        trace: NotRequired[SpanContext]
        device: NotRequired[Device]
        os: NotRequired[OperatingSystem]
        culture: NotRequired[CultureContext]
        response: NotRequired[ResponseContext]

    class Span(TypedDict):
        description: NotRequired[str]
        op: NotRequired[str]
        status: NotRequired[str]
        parent_span_id: NotRequired[str]
        sampled: NotRequired[bool]
        span_id: NotRequired[str]
        trace_id: NotRequired[str]
        tags: NotRequired[dict[str, Any]]
        data: NotRequired[dict[str, Any]]
        start_timestamp: NotRequired[datetime.datetime]
        end_timestamp: NotRequired[datetime.datetime]
        instrumenter: NotRequired[Literal["sentry", "otel"]]

    class SentryPackage(TypedDict):
        name: NotRequired[str]
        version: NotRequired[str]

    class SDKVersion(TypedDict):
        name: NotRequired[str]
        version: NotRequired[str]
        deserialized_packages: NotRequired[set[SentryPackage]]
        deserialized_integrations: NotRequired[set[str]]

    class Request(TypedDict):
        url: NotRequired[str]
        method: NotRequired[str]
        queryString: NotRequired[str]
        data: NotRequired[Any]
        cookies: NotRequired[str]
        headers: NotRequired[dict[str, str]]
        env: NotRequired[dict[str, str]]
        body_size: NotRequired[int]
        other: NotRequired[dict[str, str]]
        fragment: NotRequired[str]

    class Geo(TypedDict):
        city: NotRequired[str]
        country_code: NotRequired[str]
        region: NotRequired[str]

    class User(TypedDict):
        email: NotRequired[str]
        id: NotRequired[str]
        username: NotRequired[str]
        segment: NotRequired[str]
        ip_address: NotRequired[str]
        name: NotRequired[str]
        geo: NotRequired[Geo]
        data: NotRequired[dict[str, str]]

    Severity = Literal["fatal", "error", "warning", "log", "info", "debug"]

    class Breadcrumb(TypedDict):
        type: NotRequired[str]
        level: NotRequired[Severity]
        event_id: NotRequired[str]
        category: NotRequired[str]
        message: NotRequired[str]
        data: NotRequired[dict[str, Any]]
        timestamp: NotRequired[datetime.date]

    class SentryStackFrame(TypedDict):
        filename: NotRequired[str]
        function: NotRequired[str]
        module: NotRequired[str]
        platform: NotRequired[str]
        lineno: NotRequired[int]
        colno: NotRequired[int]
        abs_path: NotRequired[str]
        context_line: NotRequired[str]
        pre_context: NotRequired[list[str]]
        post_context: NotRequired[list[str]]
        in_app: NotRequired[bool]
        instruction_addr: NotRequired[str]
        addr_mode: NotRequired[str]
        vars: NotRequired[dict[str, Any]]
        debug_id: NotRequired[str]

    class StackTrace(TypedDict):
        frames: NotRequired[list[SentryStackFrame]]
        frames_omitted: NotRequired[tuple[int, ...]]

    class Mechanism(TypedDict):
        type: str
        description: NotRequired[str]
        help_link: NotRequired[str]
        handled: NotRequired[bool]
        meta: dict[str, Any]
        errno: dict[str, Any]
        number: NotRequired[int]
        data: NotRequired[dict[str, str | bool]]

    class SentryException(TypedDict):
        type: NotRequired[str]
        value: NotRequired[str]
        module: NotRequired[str]
        thread_id: NotRequired[str]
        stacktrace: NotRequired[StackTrace]
        mechanism: NotRequired[Mechanism]

    DurationUnit = Literal[
        "nanosecond",
        "microsecond",
        "millisecond",
        "second",
        "minute",
        "hour",
        "day",
        "week",
    ]
    InformationUnit = Literal[
        "bit",
        "byte",
        "kilobyte",
        "kibibyte",
        "megabyte",
        "mebibyte",
        "gigabyte",
        "terabyte",
        "tebibyte",
        "petabyte",
        "exabyte",
        "exbibyte",
    ]
    FractionUnit = Literal["ratio", "percent"]
    NoneUnit = Literal["", "none"]

    class Measurements(TypedDict):
        value: float
        unit: Literal[DurationUnit, InformationUnit, FractionUnit, NoneUnit]

    class WasmDebugImage(TypedDict):
        type: Literal["wasm"]
        debug_id: str
        code_id: str | None
        code_file: str
        debug_file: str | None

    class SourceMapDebugImage(TypedDict):
        type: Literal["sourcemap"]
        code_file: str
        debug_id: str

    class DebugMeta(TypedDict):
        images: NotRequired[WasmDebugImage | SourceMapDebugImage]

    class TransactionInfo(TypedDict):
        source: NotRequired[
            Literal["custom", "url", "route", "view", "component", "task"]
        ]

    class SentryThread(TypedDict):
        id: NotRequired[int]
        name: NotRequired[str]
        stacktrace: StackTrace
        crashed: NotRequired[bool]
        current: NotRequired[bool]

    class SentryEvent(TypedDict):
        event_id: NotRequired[str]
        message: NotRequired[str]
        timestamp: NotRequired[datetime.datetime]
        start_timestamp: NotRequired[datetime.datetime]
        level: NotRequired[Severity]
        platform: NotRequired[str]
        logger: NotRequired[str]
        server_name: NotRequired[str]
        release: NotRequired[str]
        dist: NotRequired[str]
        environment: NotRequired[str]
        sdk: NotRequired[SDKVersion]
        request: NotRequired[Request]
        transaction: NotRequired[str]
        modules: NotRequired[dict[str, str]]
        fingerprint: NotRequired[str]
        exception: NotRequired[list[SentryException]]
        breadcrumbs: NotRequired[list[Breadcrumb]]
        contexts: Contexts
        tags: NotRequired[dict[str, Any]]
        extra: NotRequired[dict[str, Any]]
        user: NotRequired[User]
        type: NotRequired[Literal["transaction", "profile", "replay_event"]]
        spans: NotRequired[list[Span]]
        measurements: NotRequired[Measurements]
        debug_meta: NotRequired[DebugMeta]
        transaction_info: NotRequired[TransactionInfo]
        threads: NotRequired[SentryThread]

    class Attachment(TypedDict):
        serializable: NotRequired[dict[str, Any] | list[Any]]
        pathname: NotRequired[str]
        filename: NotRequired[str]
        content_type: NotRequired[str]
        attachment_type: NotRequired[str]
        add_to_transactions: NotRequired[bool]

    class Hint(TypedDict):
        event_id: NotRequired[str]
        exc_info: tuple[type[BaseException], BaseException, TracebackType]
        attachments: list[Attachment]
        data: NotRequired[Any]
        integrations: NotRequired[list[str]]
        log_record: NotRequired[LogRecord]

    BreadcrumbHint = Dict[str, Any]

    SamplingContext = Dict[str, Any]

    EventProcessor = Callable[[SentryEvent, Hint], Optional[SentryEvent]]
    ErrorProcessor = Callable[[SentryEvent, ExcInfo], Optional[SentryEvent]]
    BreadcrumbProcessor = Callable[[Breadcrumb, BreadcrumbHint], Optional[Breadcrumb]]
    TransactionProcessor = Callable[[SentryEvent, Hint], Optional[SentryEvent]]

    TracesSampler = Callable[[SamplingContext], Union[float, int, bool]]

    # https://github.com/python/mypy/issues/5710
    NotImplementedType = Any

    EventDataCategory = Literal[
        "default",
        "error",
        "crash",
        "transaction",
        "security",
        "attachment",
        "session",
        "internal",
        "profile",
    ]
    SessionStatus = Literal["ok", "exited", "crashed", "abnormal"]
    EndpointType = Literal["store", "envelope"]

    DurationUnit = Literal[
        "nanosecond",
        "microsecond",
        "millisecond",
        "second",
        "minute",
        "hour",
        "day",
        "week",
    ]

    InformationUnit = Literal[
        "bit",
        "byte",
        "kilobyte",
        "kibibyte",
        "megabyte",
        "mebibyte",
        "gigabyte",
        "gibibyte",
        "terabyte",
        "tebibyte",
        "petabyte",
        "pebibyte",
        "exabyte",
        "exbibyte",
    ]

    FractionUnit = Literal["ratio", "percent"]
    MeasurementUnit = Union[DurationUnit, InformationUnit, FractionUnit, str]

    ProfilerMode = Literal["sleep", "thread", "gevent", "unknown"]
