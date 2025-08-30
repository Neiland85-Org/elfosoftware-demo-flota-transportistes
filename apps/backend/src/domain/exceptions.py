"""
Domain exceptions for business logic validation
"""


class DomainError(Exception):
    """Base exception for domain-related errors"""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundError(DomainError):
    """Exception raised when a requested entity is not found"""
    pass


class DuplicateCodeError(DomainError):
    """Exception raised when trying to create/update entity with duplicate code"""
    pass


class ValidationError(DomainError):
    """Exception raised when domain validation fails"""
    pass