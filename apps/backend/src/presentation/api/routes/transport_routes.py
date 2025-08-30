"""
API routes for transport management
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field, validator
from src.application.services.create_transport_service import CreateTransportService
from src.application.services.update_transport_service import UpdateTransportService
from src.application.services.list_transport_service import ListTransportService
from src.infrastructure.persistence.uow import UnitOfWork
from src.domain.exceptions import DomainError, NotFoundError, DuplicateCodeError, ValidationError
from src.presentation.api.di import (
    get_uow, 
    get_create_transport_service, 
    get_update_transport_service, 
    get_list_transport_service
)

router = APIRouter(prefix="/transportes", tags=["transportes"])


# DTOs
class CreateTransportRequest(BaseModel):
    """Request DTO for creating a transport"""
    code: str = Field(..., description="Unique transport code", min_length=2)
    capacity: float = Field(..., description="Transport capacity in kg", gt=0)


class UpdateTransportRequest(BaseModel):
    """Request DTO for updating a transport"""
    code: Optional[str] = Field(None, description="Unique transport code", min_length=2)
    capacity: Optional[float] = Field(None, description="Transport capacity in kg", gt=0)
    active: Optional[bool] = Field(None, description="Active status")

    def __init__(self, **data):
        super().__init__(**data)
        # Validate at least one field is provided
        if not any([self.code, self.capacity, self.active is not None]):
            raise ValueError("At least one field must be provided for update")


class TransportResponse(BaseModel):
    """Response DTO for transport data"""
    id: str
    code: str
    capacity: float
    active: bool

    class Config:
        from_attributes = True


# Exception handlers
def handle_domain_exceptions(e: DomainError):
    """Handle domain exceptions and map to HTTP status codes"""
    if isinstance(e, NotFoundError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    elif isinstance(e, DuplicateCodeError):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)
    elif isinstance(e, ValidationError):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message)
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Routes
@router.post("/", response_model=TransportResponse, status_code=status.HTTP_201_CREATED)
async def create_transport(
    request: CreateTransportRequest,
    uow: UnitOfWork = Depends(get_uow),
    service: CreateTransportService = Depends(get_create_transport_service)
):
    """Create a new transport"""
    try:
        transport = service.execute(uow, request.code, request.capacity)
        return TransportResponse.from_orm(transport)
    except DomainError as e:
        handle_domain_exceptions(e)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.get("/", response_model=List[TransportResponse])
async def list_transports(
    active: Optional[bool] = None,
    uow: UnitOfWork = Depends(get_uow),
    service: ListTransportService = Depends(get_list_transport_service)
):
    """List all transports, optionally filtered by active status"""
    try:
        transports = service.execute(uow, active=active)
        return [TransportResponse.from_orm(transport) for transport in transports]
    except DomainError as e:
        handle_domain_exceptions(e)


@router.put("/{transport_id}", response_model=TransportResponse)
async def update_transport(
    transport_id: str,
    request: UpdateTransportRequest,
    uow: UnitOfWork = Depends(get_uow),
    service: UpdateTransportService = Depends(get_update_transport_service)
):
    """Update a transport with partial data"""
    try:
        transport = service.execute(
            uow, 
            transport_id, 
            code=request.code, 
            capacity=request.capacity, 
            active=request.active
        )
        return TransportResponse.from_orm(transport)
    except DomainError as e:
        handle_domain_exceptions(e)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))