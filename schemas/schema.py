from sqlalchemy import create_engine
from sqlmodel import Field, SQLModel, Session

CONNECTION_STRING = (
    "mssql+pyodbc://@DESKTOP-2LMIUA2/Anomaly-Magician"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

class SampleCodesTable(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    value: str = Field(nullable=True, max_length=255)

def create_sample_database(connection_string=CONNECTION_STRING):
    engine = create_engine(connection_string, echo=True)
    SQLModel.metadata.create_all(engine)

def create_sample_data(connection_string=CONNECTION_STRING, rows=10000):
    engine = create_engine(connection_string, echo=False)
    with Session(engine) as session:
        for _ in range(rows):
            sample_data = SampleCodesTable(value="ABCDE")
            session.add(sample_data)
        session.commit()


if __name__ == "__main__":
    create_sample_database()
    create_sample_data()