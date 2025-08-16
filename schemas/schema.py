from sqlalchemy import create_engine
from sqlmodel import Field, SQLModel

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

connection_string = (
    "mssql+pyodbc://@DESKTOP-2LMIUA2/Anomaly-Magician"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)
engine = create_engine(connection_string)

with engine.connect() as conn:
    pass