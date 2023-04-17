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
    from typing import Dict
    from typing import Optional
    from typing import Tuple
    from typing import Type
    from typing import Union
    from typing_extensions import Literal
    from typing import NotRequired
    from typing import TypedDict
    from opentelemetry.trace import SpanContext

    ExcInfo = Tuple[
        Optional[Type[BaseException]], Optional[BaseException], Optional[TracebackType]
    ]


    class Contexts(TypedDict):
        trace: NotRequired[SpanContext]
        browser: NotRequired[Browser]
        device: NotRequired[Device]
        os: NotRequired[OperatingSystem]
        runtime: NotRequired[Runtime]


    class SentryStackFrame(TypedDict):
        function: NotRequired[str]
        module: NotRequired[str]
        filename: NotRequired[str]
        abs_path: NotRequired[str]
        lineno: NotRequired[int]
        pre_context: NotRequired[list[str]]
        context_line: NotRequired[str]
        post_context: NotRequired[list[str]]
        vars: NotRequired[Dict[str, Any]]


    class Mechanism(TypedDict):
        type: str
        handled: bool
        meta: dict[str, Any]
        errno: dict[str, Any]
        number: NotRequired[int]


    class SentryException(TypedDict):
        type: NotRequired[str]
        value: NotRequired[str]
        module: NotRequired[str]
        mechanism: NotRequired[Mechanism]
        stacktrace: NotRequired[list[SentryStackFrame]]


    class SentryEvent(TypedDict):
        event_id: NotRequired[str]
        contexts: Contexts
        sdk: NotRequired[SDKVersion]
        request: NotRequired[Request]
        tags: NotRequired[Dict[str, str]]
        release: NotRequired[str]
        environment: NotRequired[str]
        platform: NotRequired[str]
        user: NotRequired[User]
        server_name: NotRequired[str]
        dist: NotRequired[str]
        breadcrumbs: NotRequired[list[Breadcrumb]]
        timestamp: datetime.date
        message: NotRequired[str]
        logger: NotRequired[str]
        level: NotRequired[str]
        exception: NotRequired[list[SentryException]]

    Event = Dict[str, Any]
    Hint = Dict[str, Any]

    Breadcrumb = Dict[str, Any]
    BreadcrumbHint = Dict[str, Any]

    SamplingContext = Dict[str, Any]

    EventProcessor = Callable[[Event, Hint], Optional[Event]]
    ErrorProcessor = Callable[[Event, ExcInfo], Optional[Event]]
    BreadcrumbProcessor = Callable[[Breadcrumb, BreadcrumbHint], Optional[Breadcrumb]]
    TransactionProcessor = Callable[[Event, Hint], Optional[Event]]

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
