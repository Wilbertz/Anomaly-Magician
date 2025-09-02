from sqlmodel import Field, SQLModel, Session

class VinCodesTable(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    vin_fixed_length_valid_regex: str = Field(nullable=True, max_length=255)
    vin_fixed_length_invalid_regex: str = Field(nullable=True, max_length=255)
    vin_variable_length: str = Field(nullable=True, max_length=255)

if __name__ == "__main__":
   pass