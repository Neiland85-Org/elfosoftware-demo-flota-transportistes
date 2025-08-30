"""
CMR document processing API routes
"""
from typing import Dict, Any
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse

from src.application.use_cases.cmr_use_cases import ProcesarCMRUseCase, ValidarCMRUseCase
from src.domain.services.cmr_normalizer import CMRNormalizer, MockCMRExtractor
from src.domain.entities.cmr_document import CMRDocument

# Dependency injection
def get_cmr_normalizer() -> CMRNormalizer:
    """Get CMR normalizer service"""
    extractor = MockCMRExtractor()
    return CMRNormalizer(extractor)

def get_procesar_cmr_use_case(normalizer: CMRNormalizer = Depends(get_cmr_normalizer)) -> ProcesarCMRUseCase:
    """Get process CMR use case"""
    return ProcesarCMRUseCase(normalizer)

def get_validar_cmr_use_case() -> ValidarCMRUseCase:
    """Get validate CMR use case"""
    return ValidarCMRUseCase()

# Create router
router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/cmr/extract", response_model=CMRDocument)
async def extract_cmr_data(
    file: UploadFile = File(...),
    use_case: ProcesarCMRUseCase = Depends(get_procesar_cmr_use_case),
    validar_use_case: ValidarCMRUseCase = Depends(get_validar_cmr_use_case)
) -> CMRDocument:
    """
    Extract and normalize data from CMR document

    - **file**: PDF file containing the CMR document
    - **returns**: Normalized CMR document data
    """
    try:
        # Validate file type
        if file.filename and not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported"
            )

        if file.content_type and file.content_type != "application/pdf":
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported"
            )

        # Read file content
        file_content = await file.read()

        if not file_content:
            raise HTTPException(
                status_code=400,
                detail="Empty file provided"
            )

        # Process document
        cmr_document = use_case.execute(file_content)

        # Validate result
        if not validar_use_case.execute(cmr_document):
            raise HTTPException(
                status_code=422,
                detail="Invalid CMR document data extracted"
            )

        return cmr_document

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@router.get("/cmr/health")
async def cmr_health_check() -> Dict[str, Any]:
    """Health check for CMR processing service"""
    return {
        "status": "healthy",
        "service": "cmr_processor",
        "version": "1.0.0",
        "capabilities": [
            "pdf_processing",
            "ocr_extraction",
            "data_normalization",
            "validation"
        ]
    }
