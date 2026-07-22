from __future__ import annotations

import asyncio
import hmac
import html
import json
import re
import textwrap
import threading
import urllib.parse
import webbrowser
from http import HTTPStatus
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from .agent_runtime import AgentRuntime, AgentRuntimeError, ScopeViolation
from .catalog import load_catalog, select_exercises
from .config import Settings
from .service import WorkshopService
from .store import (
    AuthenticationError,
    ConflictError,
    NotFoundError,
    Store,
    StoreError,
    ValidationError,
)


COOKIE_NAME = "workshop_session"
PREVIEW_CSP = (
    "default-src 'none'; script-src 'self' 'unsafe-inline'; "
    "style-src 'self' 'unsafe-inline'; img-src data:; connect-src 'none'; "
    "font-src 'none'; media-src 'none'; object-src 'none'; "
    "frame-ancestors 'self'; form-action 'none'; base-uri 'none'; sandbox allow-scripts"
)


def _plain_markdown(markdown: str) -> str:
    text = re.sub(r"^#{1,6}\s*", "", markdown, flags=re.MULTILINE)
    text = text.replace("**", "").replace("`", "")
    text = re.sub(r"^[-*]\s+", "• ", text, flags=re.MULTILINE)
    return text.strip()


def spec_svg(title: str, markdown: str) -> str:
    lines: list[str] = []
    for paragraph in _plain_markdown(markdown).splitlines():
        if not paragraph.strip():
            lines.append("")
        else:
            lines.extend(textwrap.wrap(paragraph, width=86, break_long_words=False))
    line_height = 24
    height = max(420, 126 + line_height * len(lines))
    nodes: list[str] = []
    y = 104
    for line in lines:
        if line:
            nodes.append(
                f'<text x="54" y="{y}" class="body">{html.escape(line)}</text>'
            )
        y += line_height
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="{height}" viewBox="0 0 1080 {height}">
<rect width="1080" height="{height}" rx="26" fill="#f7f5ef"/>
<rect x="22" y="22" width="1036" height="{height - 44}" rx="18" fill="#fff" stroke="#d8d3c6"/>
<text x="54" y="62" class="eyebrow">SPEC-0 · PRODUCT CONSTITUTION</text>
<text x="54" y="91" class="title">{html.escape(title)}</text>
{''.join(nodes)}
<style>
.eyebrow {{ font: 700 14px ui-monospace, Consolas, monospace; letter-spacing: 2px; fill: #6750a4; }}
.title {{ font: 700 22px Inter, Arial, sans-serif; fill: #161824; }}
.body {{ font: 16px Inter, Arial, sans-serif; fill: #2d3142; }}
</style></svg>"""


class WorkshopHTTPServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, address: tuple[str, int], settings: Settings):
        catalog = load_catalog(settings.project_root)
        exercises = select_exercises(
            catalog, settings.exercise_slugs, settings.participant_count
        )
        store = Store(settings, exercises)
        runtime = AgentRuntime(settings)
        self.settings = settings
        self.store = store
        self.service = WorkshopService(settings, store, exercises, runtime)
        self.web_dir = Path(__file__).resolve().parent / "web"
        self.slides_dir = settings.project_root / "slides"
        super().__init__(address, WorkshopRequestHandler)


class WorkshopRequestHandler(BaseHTTPRequestHandler):
    server: WorkshopHTTPServer

    def log_message(self, format: str, *args: Any) -> None:
        # Intentionally logs only the standard request line/status, never bodies or headers.
        super().log_message(format, *args)

    def _send(
        self,
        status: int,
        content: bytes,
        content_type: str,
        headers: dict[str, str] | None = None,
    ) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("X-Content-Type-Options", "nosniff")
        for key, value in (headers or {}).items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(content)

    def _json(
        self,
        status: int,
        payload: Any,
        headers: dict[str, str] | None = None,
    ) -> None:
        content = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self._send(status, content, "application/json; charset=utf-8", headers)

    def _html(self, status: int, source: str, headers: dict[str, str] | None = None) -> None:
        self._send(status, source.encode("utf-8"), "text/html; charset=utf-8", headers)

    def _body(self) -> dict[str, Any]:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as error:
            raise ValidationError("Invalid Content-Length") from error
        if length < 0 or length > 100_000:
            raise ValidationError("Request body size is invalid")
        raw = self.rfile.read(length)
        if not raw:
            return {}
        try:
            value = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValidationError("Request body must be UTF-8 JSON") from error
        if not isinstance(value, dict):
            raise ValidationError("JSON body must be an object")
        return value

    def _token(self) -> str:
        authorization = self.headers.get("Authorization", "")
        if authorization.lower().startswith("bearer "):
            return authorization[7:].strip()
        cookies = SimpleCookie(self.headers.get("Cookie", ""))
        morsel = cookies.get(COOKIE_NAME)
        return morsel.value if morsel else ""

    def _user(self) -> Any:
        return self.server.store.authenticate(self._token())

    def _require_admin(self) -> None:
        supplied = self.headers.get("X-Workshop-Admin", "")
        if not supplied or not hmac.compare_digest(
            supplied, self.server.settings.admin_code
        ):
            raise AuthenticationError("Valid workshop admin code required")

    def _route(self) -> tuple[str, list[str], dict[str, list[str]]]:
        parsed = urllib.parse.urlsplit(self.path)
        path = urllib.parse.unquote(parsed.path)
        segments = [segment for segment in path.split("/") if segment]
        return path, segments, urllib.parse.parse_qs(parsed.query)

    def _handle_error(self, error: Exception) -> None:
        if isinstance(error, AuthenticationError):
            status = HTTPStatus.UNAUTHORIZED
        elif isinstance(error, NotFoundError):
            status = HTTPStatus.NOT_FOUND
        elif isinstance(error, ValidationError | ScopeViolation | ValueError | KeyError):
            status = HTTPStatus.UNPROCESSABLE_ENTITY
        elif isinstance(error, ConflictError):
            status = HTTPStatus.CONFLICT
        elif isinstance(error, AgentRuntimeError):
            status = HTTPStatus.BAD_GATEWAY
        elif isinstance(error, StoreError):
            status = HTTPStatus.INTERNAL_SERVER_ERROR
        else:
            status = HTTPStatus.INTERNAL_SERVER_ERROR
        detail = str(error) if status != HTTPStatus.INTERNAL_SERVER_ERROR else "Internal server error"
        self._json(status, {"detail": detail})

    def do_GET(self) -> None:  # noqa: N802
        try:
            self._do_get()
        except Exception as error:
            self._handle_error(error)

    def _do_get(self) -> None:
        path, segments, query = self._route()
        if path == "/":
            self._send(
                200,
                (self.server.web_dir / "index.html").read_bytes(),
                "text/html; charset=utf-8",
                {"Cache-Control": "no-store"},
            )
            return
        if path == "/admin":
            self._send(
                200,
                (self.server.web_dir / "admin.html").read_bytes(),
                "text/html; charset=utf-8",
                {"Cache-Control": "no-store"},
            )
            return
        if path in {"/slides", "/slides/"}:
            self._send(
                200,
                (self.server.slides_dir / "index.html").read_bytes(),
                "text/html; charset=utf-8",
                {"Cache-Control": "no-store"},
            )
            return
        if len(segments) == 2 and segments[0] == "slides":
            filename = segments[1]
            media = {
                "slides.css": "text/css; charset=utf-8",
                "slides.js": "text/javascript; charset=utf-8",
            }
            if filename not in media:
                raise NotFoundError("Slide asset not found")
            self._send(
                200,
                (self.server.slides_dir / filename).read_bytes(),
                media[filename],
                {"Cache-Control": "no-store"},
            )
            return
        if len(segments) == 2 and segments[0] == "assets":
            filename = segments[1]
            media = {
                "styles.css": "text/css; charset=utf-8",
                "app.js": "text/javascript; charset=utf-8",
                "admin.js": "text/javascript; charset=utf-8",
            }
            if filename not in media:
                raise NotFoundError("Asset not found")
            self._send(200, (self.server.web_dir / filename).read_bytes(), media[filename])
            return
        if path == "/api/health":
            admin_state = self.server.service.admin_state()
            self._json(
                200,
                {
                    "status": "ok",
                    "agent_mode": self.server.settings.agent_mode,
                    "model": self.server.settings.model,
                    "reasoning_effort": self.server.settings.reasoning_effort,
                    "live_progress": True,
                    "capacity": admin_state["capacity"],
                    "active_exercises": admin_state["active_participant_count"],
                    "server": "stdlib",
                },
            )
            return
        if path == "/api/admin/state":
            self._require_admin()
            self._json(200, self.server.service.admin_state())
            return
        if path == "/api/state":
            user = self._user()
            self._json(200, self.server.service.public_state(user["id"]))
            return
        if len(segments) == 3 and segments[:2] == ["api", "run-progress"]:
            user = self._user()
            try:
                cursor = int(query.get("cursor", ["0"])[0])
            except ValueError as error:
                raise ValidationError("Progress cursor must be an integer") from error
            self._json(
                200,
                self.server.service.run_progress(
                    user_id=user["id"],
                    client_request_id=segments[2],
                    cursor=cursor,
                ),
                {"Cache-Control": "no-store"},
            )
            return
        if len(segments) == 4 and segments[:2] == ["api", "files"]:
            user = self._user()
            assignment_id = int(segments[2])
            filename = segments[3]
            if filename not in {"index.html", "styles.css", "app.js"}:
                raise NotFoundError("File not found")
            _, directory = self.server.service.assignment_project(
                user_id=user["id"], assignment_id=assignment_id
            )
            self._send(
                200,
                (directory / filename).read_bytes(),
                "text/plain; charset=utf-8",
                {"Cache-Control": "no-store"},
            )
            return
        if len(segments) == 3 and segments[:2] == ["api", "spec0"]:
            user = self._user()
            assignment_id = int(segments[2].removesuffix(".svg"))
            assignment, _ = self.server.service.assignment_project(
                user_id=user["id"], assignment_id=assignment_id
            )
            if (
                assignment["kind"] != "delta"
                or assignment["stage_number"] != 1
                or assignment["author_user_id"] != user["id"]
            ):
                raise NotFoundError("SPEC-0 not found")
            exercise = self.server.service.exercises[assignment["exercise_slug"]]
            self._send(
                200,
                spec_svg(exercise.title, exercise.spec0).encode("utf-8"),
                "image/svg+xml; charset=utf-8",
                {"Cache-Control": "no-store"},
            )
            return
        if len(segments) == 2 and segments[0] == "preview":
            user = self._user()
            assignment_id = int(segments[1])
            assignment, _ = self.server.service.assignment_project(
                user_id=user["id"], assignment_id=assignment_id
            )
            ticket = self.server.service.preview_ticket(user["id"], assignment_id)
            source = (
                f"/preview-content/{ticket}/{assignment_id}/index.html"
                f"?v={assignment['project_version']}"
            )
            wrapper = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Project preview</title>
<style>html,body,iframe{{width:100%;height:100%;margin:0;border:0;background:#eef1f6}}.label{{position:fixed;right:12px;top:10px;z-index:2;padding:6px 10px;border-radius:999px;background:#171925;color:white;font:12px system-ui}}</style>
</head><body><span class="label">Sandboxed preview</span><iframe title="Project preview" sandbox="allow-scripts" src="{html.escape(source)}"></iframe></body></html>"""
            self._html(200, wrapper, {"Cache-Control": "no-store"})
            return
        if len(segments) == 4 and segments[0] == "preview-content":
            ticket, assignment_text, filename = segments[1:]
            assignment_id = int(assignment_text)
            if filename not in {"index.html", "styles.css", "app.js"}:
                raise NotFoundError("Preview file not found")
            user_id = self.server.service.validate_preview_ticket(ticket, assignment_id)
            _, directory = self.server.service.assignment_project(
                user_id=user_id, assignment_id=assignment_id
            )
            media = {
                "index.html": "text/html; charset=utf-8",
                "styles.css": "text/css; charset=utf-8",
                "app.js": "text/javascript; charset=utf-8",
            }
            self._send(
                200,
                (directory / filename).read_bytes(),
                media[filename],
                {
                    "Cache-Control": "no-store",
                    "Content-Security-Policy": PREVIEW_CSP,
                    "Referrer-Policy": "no-referrer",
                },
            )
            return
        raise NotFoundError("Route not found")

    def do_POST(self) -> None:  # noqa: N802
        try:
            self._do_post()
        except Exception as error:
            self._handle_error(error)

    def _do_post(self) -> None:
        path, _segments, _query = self._route()
        body = self._body()
        if path == "/api/login":
            session = self.server.store.login(str(body.get("nickname", "")))
            payload: dict[str, Any] = {
                "participant": {"nickname": session.nickname, "slot": session.slot},
                "state": self.server.service.public_state(session.user_id),
            }
            if body.get("client") == "cli":
                payload["token"] = session.token
            secure = "; Secure" if self.server.settings.cookie_secure else ""
            cookie = (
                f"{COOKIE_NAME}={session.token}; Path=/; HttpOnly; SameSite=Strict; "
                f"Max-Age={7 * 24 * 60 * 60}{secure}"
            )
            self._json(200, payload, {"Set-Cookie": cookie})
            return
        if path == "/api/logout":
            token = self._token()
            if token:
                self.server.store.logout(token)
            self._json(
                200,
                {"ok": True},
                {"Set-Cookie": f"{COOKIE_NAME}=; Path=/; HttpOnly; SameSite=Strict; Max-Age=0"},
            )
            return
        if path == "/api/admin/start":
            self._require_admin()
            self._json(200, self.server.service.start_workshop())
            return

        user = self._user()
        if path == "/api/run":
            result = asyncio.run(
                self.server.service.run_prompt(
                    user_id=user["id"],
                    assignment_id=int(body["assignment_id"]),
                    client_request_id=str(body["client_request_id"]),
                    prompt=str(body["prompt"]),
                )
            )
            self._json(200, result)
            return
        if path == "/api/pass":
            interpretation = body.get("interpretation")
            if interpretation is not None and not isinstance(interpretation, dict):
                raise ValidationError("interpretation must be an object")
            asyncio.run(
                self.server.service.pass_assignment(
                    user_id=user["id"],
                    assignment_id=int(body["assignment_id"]),
                    request_key=str(body["request_key"]),
                    interpretation=interpretation,
                )
            )
            self._json(200, self.server.service.public_state(user["id"]))
            return
        if path == "/api/review":
            asyncio.run(
                self.server.service.complete_review(
                    user_id=user["id"],
                    assignment_id=int(body["assignment_id"]),
                    notes=str(body.get("notes", "")),
                )
            )
            self._json(200, self.server.service.public_state(user["id"]))
            return
        raise NotFoundError("Route not found")


def build_server(settings: Settings | None = None) -> WorkshopHTTPServer:
    settings = settings or Settings.from_env()
    return WorkshopHTTPServer((settings.host, settings.port), settings)


def serve(settings: Settings | None = None) -> None:
    settings = settings or Settings.from_env()
    server = build_server(settings)
    display_host = settings.host if settings.host != "0.0.0.0" else "127.0.0.1"
    url = f"http://{display_host}:{settings.port}"
    print(f"Context Telephone listening on {url} ({settings.agent_mode} agent)")
    if settings.open_browser:
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
