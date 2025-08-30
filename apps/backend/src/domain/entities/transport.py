"""
Transport entity representing a transportation unit/vehicle
"""
from typing import Optional
from pydantic import BaseModel, Field
from src.domain.exceptions import ValidationError


class Transport(BaseModel):
    """Entity representing a transportation unit with capacity and operational status"""
    
    id: Optional[str] = Field(None, description="Unique identifier for the transport")
    code: str = Field(..., description="Unique code for the transport unit")
    capacity: float = Field(..., description="Transport capacity in kg")
    active: bool = Field(default=True, description="Whether the transport is active")

    def ensure_valid(self) -> None:
        """Ensure the transport entity is in a valid state"""
        if len(self.code) < 2:
            raise ValidationError("Code must be at least 2 characters long")
        if self.capacity <= 0:
            raise ValidationError("Capacity must be greater than 0")

    def activate(self) -> None:
        """Activate the transport unit"""
        self.active = True

    def deactivate(self) -> None:
        """Deactivate the transport unit"""
        self.active = False

    class Config:
        """Pydantic configuration"""
        from_attributes = True