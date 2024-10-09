from typing import Callable, Any


class Route:
    def __init__(
            self,
            path: str,
            endpoint: Callable[..., Any],
            *,
            methods: list[str] | None = None,
    ) -> None:
        assert path.startswith("/"), "Routed paths must start with '/'"
        self.path = path
        self.endpoint = endpoint

        if methods is None:
            self.methods = None
        else:
            self.methods = {method.upper() for method in methods}
