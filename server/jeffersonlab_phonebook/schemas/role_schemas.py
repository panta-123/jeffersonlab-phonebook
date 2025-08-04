from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class RoleBase(BaseModel):
    name: str = Field(..., max_length=50)
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None

class RoleResponse(RoleBase):
    id: int
    model_config = ConfigDict(from_attributes=True)