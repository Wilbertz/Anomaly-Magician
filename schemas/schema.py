from sqlalchemy import create_engine
from sqlmodel import Field, SQLModel

CONNECTION_STRING = (
    "mssql+pyodbc://@DESKTOP-2LMIUA2/Anomaly-Magician"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

class SampleTable(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    value: str = Field(nullable=True, max_length=255)

def create_sample_database(connection_string=CONNECTION_STRING):
    engine = create_engine(connection_string, echo=True)
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_sample_database()