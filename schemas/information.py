from pydantic import BaseModel

class Information(BaseModel):
    name: str
    text: str
    subject: str