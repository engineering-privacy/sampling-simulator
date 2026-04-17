import random
import sqlite3
from typing import List, TypedDict
from faker import Faker

REDACTED = "REDACTED"


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
        self.patient_ids:List[str] = []
    

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
            stochastic_error_rate: float | None = None,
            reset_tables: bool = True
            ) -> None:
        
        if reset_tables:
            self.cursor.execute("DELETE FROM patient_record")
            self.cursor.execute("DELETE FROM patient")
            self.cursor.execute("DELETE FROM sqlite_sequence WHERE name='patient'")
            self.cursor.execute("DELETE FROM sqlite_sequence WHERE name='patient_record'")
            
            self.conn.commit()

        
        self.patient_ids = []
        # 1. validate mode + inputs
    # 1. validate mode + inputs
        if self.mode == "percentage":
            if mislabelled_percentage is None:
                raise ValueError("mislabelled_percentage is required in percentage mode")
        elif self.mode == "stochastic":
            if stochastic_error_rate is None:
                raise ValueError("stochastic_error_rate is required in stochastic mode")
        else:
            raise ValueError(
                f"{self.mode} is not a valid mode. Use 'percentage' or 'stochastic'."
            )



        
        # 2. generate patient_ids
        for x in range(1, num_patients + 1):
            patient_id = f'hsp-{x:06d}'
            self.patient_ids.append(patient_id)
            new_patient = self._generate_patient(patient_id=patient_id)
            sql_stmt = "INSERT INTO patient (first_name,surname,dob, address, postcode,phone_number,patient_id) VALUES (?, ?, ?, ?, ?, ?, ?)"
            values = (
                new_patient["first_name"],
                new_patient["surname"],
                new_patient["dob"],
                new_patient["address"],
                new_patient["postcode"],
                new_patient["phone_number"],
                new_patient["patient_id"],
                )

            # 3. insert patients
            self.cursor.execute(sql_stmt, values)


        # 4. determine which records will be mislabelled
        # if percentage → pre-select indices
        sql_stmt = "INSERT INTO patient_record (true_patient_id, published_patient_id, is_mislabelled, record) VALUES (?, ?, ?, ?)"
        if self.mode == 'percentage':
            if not 0 <= mislabelled_percentage <= 100:
                raise ValueError("mislabelled_percentage must be between 0 and 100")
            
            num_mislabelled = round(num_records *(mislabelled_percentage / 100))
            mislabelled_indices = set(random.sample(range(num_records), num_mislabelled))


            for i in range(num_records):
                true_patient_id = random.choice(self.patient_ids)

                if i in mislabelled_indices:
                    published_patient_id = true_patient_id
                else:
                    published_patient_id = REDACTED

                record = self._generate_patient_record(patient_id=true_patient_id, published_patient_id=published_patient_id)
                
                values = (
                    record["true_patient_id"],
                    record["published_patient_id"],
                    record["is_mislabelled"],
                    record["record"]
                )
                self.cursor.execute(sql_stmt, values)
        else:
            # if stochastic → handled per record
            if stochastic_error_rate is None:
                raise ValueError("stochastic_error_rate cannot be None. Please specify a value between 0 and 1")
            if not (0 <= stochastic_error_rate <= 1):
                raise ValueError("stochastic_error_rate must be between 0 and 1")
            
            # 5. generate + insert records
            for _ in range(num_records):
                true_patient_id = random.choice(self.patient_ids)
                is_mislabelled = random.random() < stochastic_error_rate
                
                if is_mislabelled:
                    published_patient_id = true_patient_id
                else:
                    published_patient_id = REDACTED

                record = self._generate_patient_record(patient_id=true_patient_id, published_patient_id=published_patient_id)

                values = (
                    record["true_patient_id"],
                    record["published_patient_id"],
                    record["is_mislabelled"],
                    record["record"]
                )
                self.cursor.execute(sql_stmt, values)



        # 6. commit
        self.conn.commit()




    def _generate_patient(self, patient_id: str) -> Patient:
        return {
            "first_name": self.faker.first_name(),
            "surname": self.faker.last_name(),
            "dob": self.faker.date_of_birth(minimum_age=1, maximum_age=100).isoformat(),
            "address": self.faker.address().replace("\n", ", "),
            "postcode": self.faker.postcode(),
            "phone_number": self.faker.cellphone_number(),
            "patient_id": patient_id
        }

    def _generate_patient_record(self, patient_id: str, published_patient_id: str) -> PatientRecord:
        return {
            "true_patient_id": patient_id,
            "record": self.faker.text(max_nb_chars=200),
            "published_patient_id": published_patient_id,
            "is_mislabelled": 0 if published_patient_id == REDACTED else 1
        }


if __name__ == "__main__":
    generator = RecordsGenerator(mode="percentage")

    generator.populate_db(
        num_patients=100,
        num_records=1000,
        mislabelled_percentage=10
    )

    print("Test DB generated (percentage mode).")

    # Optional: quick check
    rows = generator.cursor.execute(
        "SELECT COUNT(*) as count FROM patient_record WHERE is_mislabelled = 1"
    ).fetchone()

    print(f"Mislabelled records: {rows['count']}")