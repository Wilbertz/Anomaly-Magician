from pydantic import BaseModel


class CodeModel(BaseModel):
    name: str
    industry: str | None
    iso_code: Bool