from pydantic.v1 import PositiveInt
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

from codes.VinCode import VinCode
from database import CONNECTION_STRING
from schemas.schema import VinTable


def create_sample_database(connection_string: str=CONNECTION_STRING):
    engine = create_engine(connection_string, echo=True)
    SQLModel.metadata.create_all(engine)

def create_sample_data(connection_string: str=CONNECTION_STRING, rows: PositiveInt=10000):
    engine = create_engine(connection_string, echo=False)
    vin_codes = VinCode().create_sample_codes(rows)
    with Session(engine) as session:
        for i, code in enumerate(vin_codes):
            sample_data = VinTable(
                vin_valid = code,
                vin_valid_length_invalid_regex=code[:6] + '§' + code[7:],
                vin_invalid_length=code[6:],
                name=f"Sample car: {i}",
                number=i
            )
            session.add(sample_data)
        session.commit()

if __name__ == "__main__":
    #create_sample_database()
    #create_sample_data()
    pass