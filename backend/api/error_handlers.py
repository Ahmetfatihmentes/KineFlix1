from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import logging

from backend.core import exceptions


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register global exception handlers mapping business errors to HTTP responses.
    """
    logger = logging.getLogger(__name__)

    @app.exception_handler(exceptions.BusinessException)
    async def business_exception_handler(
        request: Request, exc: exceptions.BusinessException
    ) -> JSONResponse:
        logger.warning("Business error on %s: %s", request.url.path, exc.message)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": exc.message},
        )

    @app.exception_handler(exceptions.NotFoundException)
    async def not_found_exception_handler(
        request: Request, exc: exceptions.NotFoundException
    ) -> JSONResponse:
        logger.info("Not found on %s: %s", request.url.path, exc.message)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exc.message},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.exception("Unhandled error on %s", request.url.path)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Beklenmeyen bir sunucu hatasi olustu."},
        )

