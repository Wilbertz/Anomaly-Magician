from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from database.database import CONNECTION_STRING
from schemas.schema import SampleCodesTable


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