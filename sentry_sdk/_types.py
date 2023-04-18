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


    class Device(TypedDict):
        name: NotRequired[str]
        manufacturer: NotRequired[str]
        brand: NotRequired[str]
        family: NotRequired[str]
        model: NotRequired[str]
        family: NotRequired[str]
        model: NotRequired[str]
        model_id: NotRequired[str]
        archs: NotRequired[list[str]]
        battery_level: NotRequired[float]
        charging: NotRequired[bool]
        online: NotRequired[bool]
        simulator: NotRequired[bool]
        memory_size: NotRequired[int]
        free_memory: NotRequired[int]
        usable_memory: NotRequired[int]
        low_memory: NotRequired[bool]
        storage_size: NotRequired[int]
        free_storage: NotRequired[int]
        external_storage_size: NotRequired[int]
        external_free_storage: NotRequired[int]
        screen_width_pixels: NotRequired[int]
        screen_height_pixels: NotRequired[int]
        screen_density: NotRequired[float]
        screen_dpi: NotRequired[int]
        boot_time: NotRequired[datetime.date]
        timezone: NotRequired[datetime.timezone]
        id: NotRequired[str]
        language: NotRequired[str]
        locale: NotRequired[str]
        connection_type: NotRequired[str]
        battery_temperature: NotRequired[float]
        processor_count: NotRequired[int]
        processor_frequency: NotRequired[float]
        cpu_description: NotRequired[str]


    class OperatingSystem(TypedDict):
        name: NotRequired[str]
        version: NotRequired[str]
        raw_description: NotRequired[str]
        build: NotRequired[str]
        kernel_version: NotRequired[str]
        rooted: NotRequired[bool]


    class SentryRuntime(TypedDict):
        name: NotRequired[str]
        version: NotRequired[str]
        raw_description: NotRequired[str]


    class Contexts(TypedDict):
        trace: NotRequired[SpanContext]
        device: NotRequired[Device]
        os: NotRequired[OperatingSystem]
        runtime: NotRequired[SentryRuntime]


    class SentryPackage(TypedDict):
        name: NotRequired[str]
        version: NotRequired[str]


    class SDKVersion(TypedDict):
        name: NotRequired[str]
        version: NotRequired[str]
        deserialized_packages: NotRequired[set[SentryPackage]]
        deserialized_integrations:  NotRequired[set[str]]
        

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
        segment:  NotRequired[str]
        ip_address: NotRequired[str]
        name: NotRequired[str]
        geo: NotRequired[Geo]
        data: NotRequired[dict[str, str]]


    class Breadcrumb(TypedDict):
        timestamp: NotRequired[datetime.date]
        message: NotRequired[str]
        type: NotRequired[str]
        data: NotRequired[dict[str, Any]]
        category: NotRequired[str]
        level: NotRequired[str]


    class SentryStackFrame(TypedDict):
        function: NotRequired[str]
        module: NotRequired[str]
        filename: NotRequired[str]
        abs_path: NotRequired[str]
        lineno: NotRequired[int]
        pre_context: NotRequired[list[str]]
        context_line: NotRequired[str]
        post_context: NotRequired[list[str]]
        vars: NotRequired[dict[str, Any]]


    class Mechanism(TypedDict):
        type: str
        description: NotRequired[str]
        help_link: NotRequired[str]
        handled: NotRequired[bool]
        meta: dict[str, Any]
        errno: dict[str, Any]
        number: NotRequired[int]


    class SentryException(TypedDict):
        type: NotRequired[str]
        value: NotRequired[str]
        module: NotRequired[str]
        thread_id: NotRequired[str]
        stacktrace: NotRequired[list[SentryStackFrame]]
        mechanism: NotRequired[Mechanism]


    class SentryEvent(TypedDict):
        event_id: NotRequired[str]
        contexts: Contexts
        sdk: NotRequired[SDKVersion]
        request: NotRequired[Request]
        tags: NotRequired[dict[str, str]]
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

    class Attachment(TypedDict):
        serializable: NotRequired[dict[str, Any] | list[Any]]
        pathname: NotRequired[str]
        filename: NotRequired[str]
        content_type: NotRequired[str]
        add_to_transactions: bool
        attachment_type: str

    class Hint(TypedDict):
        internal_storage: dict[str, Any]
        attachments: list[Attachment]
        screenshot: NotRequired[Attachment]
        view_hierarchy: NotRequired[Attachment]


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
