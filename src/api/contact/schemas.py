from pydantic import BaseModel, Field


# Contact request
class ContactRequest(BaseModel):
  reason: str = Field(min_length=1, max_length=50)
  name: str = Field(min_length=1, max_length=100)
  message: str = Field(min_length=1, max_length=5000)


# Contact response
class ContactResponse(BaseModel):
  status: str = "sent"
