import random
import sqlite3
from typing import List

from .models import Patient, PatientRecord


class DataModel:
    def __init__(self, db_name: str = "records") -> None:
        self.db_name = db_name
        self.conn = sqlite3.connect(f"{db_name}.db")
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self) -> None:
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

    # ---------- INSERT ----------

    def insert_patient(self, patient: Patient) -> None:
        self.cursor.execute(
            """
            INSERT INTO patient (first_name, surname, dob, address, postcode, phone_number, patient_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                patient.first_name,
                patient.surname,
                patient.dob,
                patient.address,
                patient.postcode,
                patient.phone_number,
                patient.patient_id,
            ),
        )

    def insert_patient_record(self, record: PatientRecord) -> None:
        self.cursor.execute(
            """
            INSERT INTO patient_record (true_patient_id, published_patient_id, is_mislabelled, record)
            VALUES (?, ?, ?, ?)
            """,
            (
                record.true_patient_id,
                record.published_patient_id,
                record.is_mislabelled,
                record.record,
            ),
        )

    def commit(self) -> None:
        self.conn.commit()

    def reset(self) -> None:
        self.cursor.execute("DELETE FROM patient_record")
        self.cursor.execute("DELETE FROM patient")
        self.conn.commit()

    # ---------- QUERIES ----------

    def get_population_size(self) -> int:
        row = self.cursor.execute(
            "SELECT COUNT(*) as count FROM patient_record"
        ).fetchone()
        return row["count"]

    def get_random_sample(self, sample_size: int) -> List[PatientRecord]:
        rows = self.cursor.execute(
            f"""
            SELECT true_patient_id, published_patient_id, is_mislabelled, record
            FROM patient_record
            ORDER BY RANDOM()
            LIMIT {sample_size}
            """
        ).fetchall()

        return [
            PatientRecord(
                true_patient_id=row["true_patient_id"],
                published_patient_id=row["published_patient_id"],
                is_mislabelled=row["is_mislabelled"],
                record=row["record"],
            )
            for row in rows
        ]

    def get_patients_by_ids(self, patient_ids: set[str]) -> List[Patient]:
        if not patient_ids:
            return []

        placeholders = ",".join("?" for _ in patient_ids)

        rows = self.cursor.execute(
            f"""
            SELECT first_name, surname, dob, address, postcode, phone_number, patient_id
            FROM patient
            WHERE patient_id IN ({placeholders})
            """,
            tuple(patient_ids),
        ).fetchall()

        return [
            Patient(
                first_name=row["first_name"],
                surname=row["surname"],
                dob=row["dob"],
                address=row["address"],
                postcode=row["postcode"],
                phone_number=row["phone_number"],
                patient_id=row["patient_id"],
            )
            for row in rows
        ]