from dataclasses import dataclass
from typing import List


@dataclass 
class Patient:
    first_name: str
    surname: str
    dob: str
    address: str
    postcode: str
    phone_number: str
    patient_id: str 

@dataclass
class PatientRecord:
    true_patient_id: str
    published_patient_id: str
    is_mislabelled: bool
    record: str


@dataclass
class Results: 
    sample_size: int
    population_size: int 
    patient_records: List[PatientRecord]
    affected_patients: List[Patient]


@dataclass
class ExperimentResults:
    trial_results: List[Results]

    total_trials: int
    detections: int
    detection_rate: float



