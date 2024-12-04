from typing import Callable

from fastapi import FastAPI, Request, Response
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from .schemas import SummaryResponse, User
from .services.llm_service import ice_break_with

StrOrCallable = str | Callable[..., str]

RATE_LIMIT_VALUE = "1/30seconds"


def create_app(rate_limit_value: StrOrCallable = RATE_LIMIT_VALUE) -> FastAPI:
    app = FastAPI(root_path="/api/v1")

    # limiter = Limiter(key_func=get_remote_address, headers_enabled=True)
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=[rate_limit_value],
        headers_enabled=True,
    )
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)

    @app.post("/process", response_model=SummaryResponse)
    # @limiter.limit(rate_limit_value)  # this is replaced by the middleware
    async def process(
        user: User, request: Request, response: Response
    ) -> SummaryResponse:  # NOTE: request and response are needed for the rate limiter
        summary, profile_pic_url = ice_break_with(name=user.name, mock=True)
        return SummaryResponse(picture_url=profile_pic_url, **summary.model_dump())

    return app


app = create_app(RATE_LIMIT_VALUE)
