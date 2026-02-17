from typing import Any, Protocol


class InitComponentsProtocol(Protocol): ...


class InitComponentProtocol(Protocol): ...


class DisposeComponentsProtocol(Protocol): ...


class DisposeComponentProtocol(Protocol): ...


class MAppProtocol(Protocol):
    @property
    def api(self) -> Any: ...  # noqa: ANN401


class VAppProtocol(MAppProtocol, Protocol):
    @property
    def path(self) -> str: ...
