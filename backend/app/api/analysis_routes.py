from fastapi import APIRouter, HTTPException, status

from app.schemas.analysis_request_schemas import AnalysisRequest
from app.services.analysis_orchestrator_service import analyze
from app.utils.response_trimmer import trim_analysis_response

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post(
    "",
    status_code=status.HTTP_200_OK,
)
async def analysis(request: AnalysisRequest):
    try:
        response = await analyze(request)
        return response;
        # return {
        #     "files": trim_analysis_response(response),
        #     "warnings": response.warnings,
        # }
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        # The general Exception catch doesn't return the original error message
        # for security reasons.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while analyzing repositories.",
        ) from exc