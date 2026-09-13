"""The composition root.

The only place a repository, an adapter or a service is constructed, and the
only module allowed to import from more than one domain, because wiring is its
whole job. See backend/.claude/rules/repo-rules.md section 9.
"""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.auth import extract_bearer_token, verify_token
from app.core.context import Context
from app.core.errors import AuthenticationError
from app.core.settings import Settings, get_settings
from app.domains.capture.adapters.gateway_extraction_adapter import (
    GatewayExtractionAdapter,
)
from app.domains.capture.adapters.records_task_adapter import RecordsTaskAdapter
from app.domains.capture.interactors.answer_pending_capture import (
    AnswerPendingCaptureInteractor,
)
from app.domains.capture.interactors.discard_pending_capture import (
    DiscardPendingCaptureInteractor,
)
from app.domains.capture.interactors.submit_capture import SubmitCaptureInteractor
from app.domains.capture.repositories.pending_capture_repository import (
    SqlPendingCaptureRepository,
)
from app.domains.gateway.interactors.extract import ExtractInteractor
from app.domains.gateway.repositories.usage_repository import SqlUsageRepository
from app.domains.gateway.services.allowance_service import AllowanceService
from app.domains.gateway.services.langchain_provider import LangChainGeminiProvider
from app.domains.identity.interactors.get_settings import GetSettingsInteractor
from app.domains.identity.interactors.update_timezone import UpdateTimezoneInteractor
from app.domains.identity.repositories.settings_repository import SqlSettingsRepository
from app.domains.records.interactors.delete_tasks import DeleteTasksInteractor
from app.domains.records.interactors.get_record_detail import GetRecordDetailInteractor
from app.domains.records.interactors.list_tasks import ListTasksInteractor
from app.domains.records.interactors.update_task import UpdateTaskInteractor
from app.domains.records.repositories.task_repository import SqlTaskRepository
from app.domains.records.services.records_service import RecordsService


async def build_context(
    *,
    authorization_header: str | None,
    request_id: str,
    session_factory: async_sessionmaker[AsyncSession],
    settings: Settings,
) -> Context:
    """Build the per-request context.

    An absent or unusable token produces a context with no identity rather than
    an error. Refusal is a field's decision, made by its permission class, so
    that a public field remains reachable without a token while every other
    field is closed by ``IsAuthenticated``.
    """
    user_id: uuid.UUID | None = None
    token = extract_bearer_token(authorization_header)
    if token is not None:
        try:
            user_id = verify_token(token, settings)
        except AuthenticationError:
            user_id = None

    return Context(
        user_id=user_id,
        session=session_factory(),
        request_id=request_id,
        session_factory=session_factory,
    )


def build_extract_interactor(
    *, session_factory: async_sessionmaker[AsyncSession], settings: Settings
) -> ExtractInteractor:
    """Wire the gateway.

    This is the only place the provider credential is read, and the only place
    LangChain is named outside the adapter itself. Requirement FR-5: no other
    component holds the key or calls a provider.
    """
    usage_repository = SqlUsageRepository(session_factory)
    return ExtractInteractor(
        provider=LangChainGeminiProvider(
            api_key=settings.gemini_api_key, model=settings.gemini_model
        ),
        usage_repository=usage_repository,
        allowance_service=AllowanceService(usage_repository),
        settings=settings,
    )


def _build_task_port(*, context: Context) -> RecordsTaskAdapter:
    records_service = RecordsService(task_repository=SqlTaskRepository(context.session))
    return RecordsTaskAdapter(records_service=records_service)


def _build_extraction_port(*, context: Context) -> GatewayExtractionAdapter:
    settings = get_settings()
    extract_interactor = build_extract_interactor(
        session_factory=context.session_factory, settings=settings
    )
    return GatewayExtractionAdapter(extract_interactor=extract_interactor)


def build_submit_capture_interactor(context: Context) -> SubmitCaptureInteractor:
    """Wire capture's one use case.

    Epic 001, slice 1 (04.1-capture-core.md). ``capture`` never imports
    ``records`` or ``gateway`` directly; both reach it through a port this
    domain declared and an adapter this function builds, per repo-rules.md
    section 6.
    """
    return SubmitCaptureInteractor(
        pending_capture_repository=SqlPendingCaptureRepository(context.session),
        task_port=_build_task_port(context=context),
        extraction=_build_extraction_port(context=context),
    )


def build_answer_pending_capture_interactor(
    context: Context,
) -> AnswerPendingCaptureInteractor:
    return AnswerPendingCaptureInteractor(
        pending_capture_repository=SqlPendingCaptureRepository(context.session),
        task_port=_build_task_port(context=context),
        extraction=_build_extraction_port(context=context),
    )


def build_discard_pending_capture_interactor(
    context: Context,
) -> DiscardPendingCaptureInteractor:
    return DiscardPendingCaptureInteractor(
        pending_capture_repository=SqlPendingCaptureRepository(context.session)
    )


def build_records_service(context: Context) -> RecordsService:
    """Records' own resolvers may call this directly, the same published
    surface capture's adapter reaches through a port. See 04.2-records-and-
    settings.md section 4: the `tasks` query reuses this, not a new
    interactor, because it is exactly the list `/tasks` already calls."""
    return RecordsService(task_repository=SqlTaskRepository(context.session))


def build_list_tasks_interactor(context: Context) -> ListTasksInteractor:
    return ListTasksInteractor(task_repository=SqlTaskRepository(context.session))


def build_get_record_detail_interactor(context: Context) -> GetRecordDetailInteractor:
    return GetRecordDetailInteractor(task_repository=SqlTaskRepository(context.session))


def build_update_task_interactor(context: Context) -> UpdateTaskInteractor:
    return UpdateTaskInteractor(task_repository=SqlTaskRepository(context.session))


def build_delete_tasks_interactor(context: Context) -> DeleteTasksInteractor:
    return DeleteTasksInteractor(task_repository=SqlTaskRepository(context.session))


def build_get_settings_interactor(context: Context) -> GetSettingsInteractor:
    return GetSettingsInteractor(
        settings_repository=SqlSettingsRepository(context.session)
    )


def build_update_timezone_interactor(context: Context) -> UpdateTimezoneInteractor:
    return UpdateTimezoneInteractor(
        settings_repository=SqlSettingsRepository(context.session)
    )
