import random
import sqlite3
from typing import TypedDict
from faker import Faker


class Patient(TypedDict):
    first_name: str
    surname: str
    dob: str
    address: str
    postcode: str
    phone_number: str
    patient_id: str 

class PatientRecord(TypedDict):
    true_patient_id: str
    published_patient_id: str
    is_mislabelled: int
    record: str


# generate a SQL Lite DB of a simulated health records. 
class RecordsGenerator:
    def __init__(self, db_name: str = "records", mode: str = 'percentage'):
        self.mode = mode # Can also be 'stochastic' TODO: Replace with enum later
        self.faker = Faker("en_GB")
        self.db_name = db_name
        self.conn = sqlite3.connect(f"{db_name}.db")
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._create_db_tables()
    

    def _create_db_tables(self) -> None:
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS patient (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            first_name TEXT,
                            surname TEXT,
                            dob TEXT, 
                            address TEXT, 
                            postcode TEXT,
                            phone_number TEXT,
                            patient_id TEXT UNIQUE
                            )
                            """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS patient_record (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            true_patient_id TEXT,
                            published_patient_id TEXT,
                            is_mislabelled INTEGER CHECK(is_mislabelled IN (0,1)),
                            record TEXT
                            )
                            """)
        self.conn.commit()
    
    def populate_db(
            self,
            num_patients: int,
            num_records: int,
            mislabelled_percentage:float | None = None,
            stochastic_error_rate: float | None=None
            ) -> None:
        # TODO: validate mode and ensure the correct parameter is provided
        # percentage mode -> mislabelled_percentage required
        # # stochastic mode -> stochastic_error_rate required
        pass


    def _generate_patient(self, patient_id: str) -> Patient:
        pass

    def _generate_patient_record(self, patient_id: str) -> PatientRecord:
        pass


