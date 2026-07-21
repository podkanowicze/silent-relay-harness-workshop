from __future__ import annotations

from .config import Settings


def main() -> None:
    settings = Settings.from_env()
    from .stdlib_server import serve

    serve(settings)


if __name__ == "__main__":
    main()
