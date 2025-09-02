from sqlmodel import Field, SQLModel, Session

class VinCodesTable(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, description="The primary key column.")
    vin_valid: str = Field(nullable=True, max_length=255, description="Syntactically valid VIN codes.")
    vin_valid_length_invalid_regex: str = Field(nullable=True, max_length=255, description="VIN with valid length but invalid regex.")
    vin_invalid_length: str = Field(nullable=True, max_length=255, description="VIN with invalid length.")
    name: str = Field(nullable=True, max_length=255, description="An arbitrary name.")

if __name__ == "__main__":
   pass