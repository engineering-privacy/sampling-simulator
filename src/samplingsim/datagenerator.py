import random
from faker import Faker

from .datamodel import DataModel
from .models import Patient, PatientRecord

REDACTED = "REDACTED"


class RecordsGenerator:
    def __init__(self, datamodel: DataModel, mode: str = "percentage") -> None:
        self.mode = mode
        self.datamodel = datamodel
        self.faker = Faker("en_GB")

    def populate_db(
        self,
        num_patients: int,
        num_records: int,
        mislabelled_percentage: float | None = None,
        stochastic_error_rate: float | None = None,
        reset_tables: bool = True,
    ) -> None:
        if reset_tables:
            self.datamodel.reset()

        patient_ids = []

        # Generate patients
        for i in range(1, num_patients + 1):
            patient_id = f"hsp-{i:06d}"
            patient_ids.append(patient_id)

            patient = Patient(
                first_name=self.faker.first_name(),
                surname=self.faker.last_name(),
                dob=self.faker.date_of_birth(minimum_age=1, maximum_age=100).isoformat(),
                address=self.faker.address().replace("\n", ", "),
                postcode=self.faker.postcode(),
                phone_number=self.faker.cellphone_number(),
                patient_id=patient_id,
            )

            self.datamodel.insert_patient(patient)

        # Generate records
        if self.mode == "percentage":
            num_mislabelled = round(num_records * (mislabelled_percentage / 100))
            mislabelled_indices = set(random.sample(range(num_records), num_mislabelled))

            for i in range(num_records):
                true_id = random.choice(patient_ids)

                published_id = true_id if i in mislabelled_indices else REDACTED

                record = PatientRecord(
                    true_patient_id=true_id,
                    published_patient_id=published_id,
                    is_mislabelled=0 if published_id == REDACTED else 1,
                    record=self.faker.text(max_nb_chars=200),
                )

                self.datamodel.insert_patient_record(record)

        else:
            for _ in range(num_records):
                true_id = random.choice(patient_ids)
                is_mislabelled = random.random() < stochastic_error_rate

                published_id = true_id if is_mislabelled else REDACTED

                record = PatientRecord(
                    true_patient_id=true_id,
                    published_patient_id=published_id,
                    is_mislabelled=1 if is_mislabelled else 0,
                    record=self.faker.text(max_nb_chars=200),
                )

                self.datamodel.insert_patient_record(record)

        self.datamodel.commit()