from __future__ import annotations

import html
import hmac
import re
import textwrap
from pathlib import Path
from typing import Annotated, Any

from fastapi import Cookie, Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, Response
from pydantic import BaseModel, Field

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
    "default-src 'none'; "
    "script-src 'self' 'unsafe-inline'; "
    "style-src 'self' 'unsafe-inline'; "
    "img-src data:; connect-src 'none'; font-src 'none'; media-src 'none'; "
    "object-src 'none'; frame-ancestors 'self'; form-action 'none'; base-uri 'none'; "
    "sandbox allow-scripts"
)


class LoginBody(BaseModel):
    nickname: str
    client: str = "browser"


class PromptBody(BaseModel):
    assignment_id: int
    prompt: str
    client_request_id: str = Field(min_length=8, max_length=100)


class InterpretationBody(BaseModel):
    application_for: str
    primary_user: str
    final_action_causes: str


class PassBody(BaseModel):
    assignment_id: int
    request_key: str = Field(min_length=8, max_length=100)
    interpretation: InterpretationBody | None = None


class ReviewBody(BaseModel):
    assignment_id: int
    notes: str = Field(default="", max_length=12000)


def _token_from_request(
    authorization: str | None, cookie_token: str | None
) -> str:
    if authorization and authorization.lower().startswith("bearer "):
        return authorization[7:].strip()
    return cookie_token or ""


def _plain_markdown(markdown: str) -> str:
    text = re.sub(r"^#{1,6}\s*", "", markdown, flags=re.MULTILINE)
    text = text.replace("**", "").replace("`", "")
    text = re.sub(r"^[-*]\s+", "• ", text, flags=re.MULTILINE)
    return text.strip()


def _spec_svg(title: str, markdown: str) -> str:
    lines: list[str] = []
    for paragraph in _plain_markdown(markdown).splitlines():
        if not paragraph.strip():
            lines.append("")
            continue
        lines.extend(textwrap.wrap(paragraph, width=86, break_long_words=False))
    line_height = 24
    height = max(420, 126 + line_height * len(lines))
    text_nodes = []
    y = 104
    for line in lines:
        if line:
            text_nodes.append(
                f'<text x="54" y="{y}" class="body">{html.escape(line)}</text>'
            )
        y += line_height
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="{height}" viewBox="0 0 1080 {height}">
<rect width="1080" height="{height}" rx="26" fill="#f7f5ef"/>
<rect x="22" y="22" width="1036" height="{height - 44}" rx="18" fill="#fff" stroke="#d8d3c6"/>
<text x="54" y="62" class="eyebrow">SPEC-0 · PRODUCT CONSTITUTION</text>
<text x="54" y="91" class="title">{html.escape(title)}</text>
{''.join(text_nodes)}
<style>
.eyebrow {{ font: 700 14px ui-monospace, SFMono-Regular, Consolas, monospace; letter-spacing: 2px; fill: #6750a4; }}
.title {{ font: 700 22px Inter, Arial, sans-serif; fill: #161824; }}
.body {{ font: 16px Inter, Arial, sans-serif; fill: #2d3142; }}
</style>
</svg>"""


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings.from_env()
    catalog = load_catalog(settings.project_root)
    exercises = select_exercises(
        catalog, settings.exercise_slugs, settings.participant_count
    )
    store = Store(settings, exercises)
    runtime = AgentRuntime(settings)
    service = WorkshopService(settings, store, exercises, runtime)
    web_dir = Path(__file__).resolve().parent / "web"
    slides_dir = settings.project_root / "slides"

    app = FastAPI(title="Context Telephone Workshop", version="0.1.0")
    app.state.settings = settings
    app.state.store = store
    app.state.service = service

    def current_user(
        authorization: Annotated[str | None, Header()] = None,
        workshop_session: Annotated[str | None, Cookie(alias=COOKIE_NAME)] = None,
    ) -> Any:
        token = _token_from_request(authorization, workshop_session)
        return store.authenticate(token)

    def require_admin(
        x_workshop_admin: Annotated[
            str | None, Header(alias="X-Workshop-Admin")
        ] = None,
    ) -> None:
        if not x_workshop_admin or not hmac.compare_digest(
            x_workshop_admin, settings.admin_code
        ):
            raise AuthenticationError("Valid workshop admin code required")

    @app.exception_handler(AuthenticationError)
    async def authentication_error(_: Request, error: AuthenticationError) -> JSONResponse:
        return JSONResponse({"detail": str(error)}, status_code=401)

    @app.exception_handler(NotFoundError)
    async def not_found_error(_: Request, error: NotFoundError) -> JSONResponse:
        return JSONResponse({"detail": str(error)}, status_code=404)

    @app.exception_handler(ValidationError)
    async def validation_error(_: Request, error: ValidationError) -> JSONResponse:
        return JSONResponse({"detail": str(error)}, status_code=422)

    @app.exception_handler(ConflictError)
    async def conflict_error(_: Request, error: ConflictError) -> JSONResponse:
        return JSONResponse({"detail": str(error)}, status_code=409)

    @app.exception_handler(ScopeViolation)
    async def scope_error(_: Request, error: ScopeViolation) -> JSONResponse:
        return JSONResponse(
            {"detail": f"Workspace change rejected: {error}"}, status_code=422
        )

    @app.exception_handler(AgentRuntimeError)
    async def agent_error(_: Request, error: AgentRuntimeError) -> JSONResponse:
        return JSONResponse({"detail": str(error)}, status_code=502)

    @app.exception_handler(StoreError)
    async def store_error(_: Request, error: StoreError) -> JSONResponse:
        return JSONResponse({"detail": str(error)}, status_code=500)

    @app.get("/", include_in_schema=False)
    async def index() -> FileResponse:
        return FileResponse(web_dir / "index.html")

    @app.get("/admin", include_in_schema=False)
    async def admin_page() -> FileResponse:
        return FileResponse(web_dir / "admin.html")

    @app.get("/slides", include_in_schema=False)
    @app.get("/slides/", include_in_schema=False)
    async def slides_page() -> FileResponse:
        return FileResponse(slides_dir / "index.html", headers={"Cache-Control": "no-store"})

    @app.get("/slides/{filename}", include_in_schema=False)
    async def slide_asset(filename: str) -> FileResponse:
        if filename not in {"slides.css", "slides.js"}:
            raise HTTPException(status_code=404)
        return FileResponse(slides_dir / filename, headers={"Cache-Control": "no-store"})

    @app.get("/assets/{filename}", include_in_schema=False)
    async def asset(filename: str) -> FileResponse:
        if filename not in {"styles.css", "app.js", "admin.js"}:
            raise HTTPException(status_code=404)
        return FileResponse(web_dir / filename)

    @app.get("/api/health")
    async def health() -> dict[str, Any]:
        admin = service.admin_state()
        return {
            "status": "ok",
            "agent_mode": settings.agent_mode,
            "model": settings.model,
            "reasoning_effort": settings.reasoning_effort,
            "live_progress": True,
            "capacity": admin["capacity"],
            "exercise_pool": len(exercises),
            "active_exercises": admin["active_participant_count"],
        }

    @app.get("/api/admin/state", dependencies=[Depends(require_admin)])
    async def admin_state() -> dict[str, Any]:
        return service.admin_state()

    @app.post("/api/admin/start", dependencies=[Depends(require_admin)])
    async def admin_start() -> dict[str, Any]:
        return service.start_workshop()

    @app.post("/api/login")
    async def login(body: LoginBody) -> JSONResponse:
        session = store.login(body.nickname)
        payload: dict[str, Any] = {
            "participant": {
                "nickname": session.nickname,
                "slot": session.slot,
            },
            "state": service.public_state(session.user_id),
        }
        if body.client == "cli":
            payload["token"] = session.token
        response = JSONResponse(payload)
        response.set_cookie(
            COOKIE_NAME,
            session.token,
            httponly=True,
            samesite="strict",
            secure=settings.cookie_secure,
            max_age=7 * 24 * 60 * 60,
            path="/",
        )
        return response

    @app.post("/api/logout")
    async def logout(
        authorization: Annotated[str | None, Header()] = None,
        workshop_session: Annotated[str | None, Cookie(alias=COOKIE_NAME)] = None,
    ) -> JSONResponse:
        token = _token_from_request(authorization, workshop_session)
        if token:
            store.logout(token)
        response = JSONResponse({"ok": True})
        response.delete_cookie(COOKIE_NAME, path="/")
        return response

    @app.get("/api/state")
    async def state(user: Any = Depends(current_user)) -> dict[str, Any]:
        return service.public_state(user["id"])

    @app.get("/api/run-progress/{client_request_id}")
    async def run_progress(
        client_request_id: str,
        cursor: int = 0,
        user: Any = Depends(current_user),
    ) -> dict[str, Any]:
        return service.run_progress(
            user_id=user["id"],
            client_request_id=client_request_id,
            cursor=cursor,
        )

    @app.post("/api/run")
    async def run_prompt(
        body: PromptBody, user: Any = Depends(current_user)
    ) -> dict[str, Any]:
        try:
            return await service.run_prompt(
                user_id=user["id"],
                assignment_id=body.assignment_id,
                client_request_id=body.client_request_id,
                prompt=body.prompt,
            )
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @app.post("/api/pass")
    async def pass_assignment(
        body: PassBody, user: Any = Depends(current_user)
    ) -> dict[str, Any]:
        interpretation = body.interpretation.model_dump() if body.interpretation else None
        await service.pass_assignment(
            user_id=user["id"],
            assignment_id=body.assignment_id,
            request_key=body.request_key,
            interpretation=interpretation,
        )
        return service.public_state(user["id"])

    @app.post("/api/review")
    async def review(
        body: ReviewBody, user: Any = Depends(current_user)
    ) -> dict[str, Any]:
        await service.complete_review(
            user_id=user["id"], assignment_id=body.assignment_id, notes=body.notes
        )
        return service.public_state(user["id"])

    @app.get("/api/files/{assignment_id}/{filename}")
    async def project_file(
        assignment_id: int,
        filename: str,
        user: Any = Depends(current_user),
    ) -> Response:
        if filename not in {"index.html", "styles.css", "app.js"}:
            raise HTTPException(status_code=404)
        _, project_dir = service.assignment_project(
            user_id=user["id"], assignment_id=assignment_id
        )
        return Response(
            (project_dir / filename).read_text(encoding="utf-8"),
            media_type="text/plain; charset=utf-8",
            headers={"Cache-Control": "no-store"},
        )

    @app.get("/api/spec0/{assignment_id}.svg")
    async def spec0_image(
        assignment_id: int, user: Any = Depends(current_user)
    ) -> Response:
        assignment, _ = service.assignment_project(
            user_id=user["id"], assignment_id=assignment_id
        )
        if (
            assignment["kind"] != "delta"
            or assignment["stage_number"] != 1
            or assignment["author_user_id"] != user["id"]
        ):
            raise HTTPException(status_code=404)
        exercise = service.exercises[assignment["exercise_slug"]]
        return Response(
            _spec_svg(exercise.title, exercise.spec0),
            media_type="image/svg+xml",
            headers={"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff"},
        )

    @app.get("/preview/{assignment_id}", include_in_schema=False)
    async def preview(
        assignment_id: int, user: Any = Depends(current_user)
    ) -> HTMLResponse:
        assignment, _ = service.assignment_project(
            user_id=user["id"], assignment_id=assignment_id
        )
        ticket = service.preview_ticket(user["id"], assignment_id)
        source = (
            f"/preview-content/{ticket}/{assignment_id}/index.html"
            f"?v={assignment['project_version']}"
        )
        wrapper = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Project preview</title><style>
html,body,iframe{{width:100%;height:100%;margin:0;border:0;background:#eef1f6}}
.label{{position:fixed;right:12px;top:10px;z-index:2;padding:6px 10px;border-radius:999px;background:#171925;color:white;font:12px system-ui}}
</style></head><body><span class="label">Sandboxed preview</span>
<iframe title="Project preview" sandbox="allow-scripts" src="{html.escape(source)}"></iframe></body></html>"""
        return HTMLResponse(wrapper, headers={"Cache-Control": "no-store"})

    @app.get(
        "/preview-content/{ticket}/{assignment_id}/{filename}",
        include_in_schema=False,
    )
    async def preview_content(ticket: str, assignment_id: int, filename: str) -> Response:
        if filename not in {"index.html", "styles.css", "app.js"}:
            raise HTTPException(status_code=404)
        try:
            user_id = service.validate_preview_ticket(ticket, assignment_id)
            _, project_dir = service.assignment_project(
                user_id=user_id, assignment_id=assignment_id
            )
        except (ValueError, StoreError) as error:
            raise HTTPException(status_code=404) from error
        media_types = {
            "index.html": "text/html; charset=utf-8",
            "styles.css": "text/css; charset=utf-8",
            "app.js": "text/javascript; charset=utf-8",
        }
        return Response(
            (project_dir / filename).read_bytes(),
            media_type=media_types[filename],
            headers={
                "Cache-Control": "no-store",
                "Content-Security-Policy": PREVIEW_CSP,
                "X-Content-Type-Options": "nosniff",
                "Referrer-Policy": "no-referrer",
            },
        )

    return app
