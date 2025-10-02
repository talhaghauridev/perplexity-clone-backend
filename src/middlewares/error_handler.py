from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
from src.utils.exceptions import ApiError
from src.config import config
import logging

logger = logging.getLogger(__name__)


async def error_handler_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response

    except ApiError as e:
        logger.warning(f"API Error: {e.message} [{e.status_code}]")
        return JSONResponse(
            status_code=e.status_code, content={"success": False, "message": e.message}
        )

    except ValidationError as e:
        logger.warning(f"Validation Error: {str(e)}")
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "message": "Validation error",
                "details": e.errors() if config.debug else None,
            },
        )

    except SQLAlchemyError as e:
        logger.error(f"Database Error: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Database error" if not config.debug else str(e),
            },
        )

    except Exception as e:
        logger.error(f"Unexpected Error: {str(e)}", exc_info=True)

        if config.debug:
            import traceback

            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": str(e),
                    "type": type(e).__name__,
                    "traceback": traceback.format_exc(),
                },
            )
        else:
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": "Internal server error"},
            )
