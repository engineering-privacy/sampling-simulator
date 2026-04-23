import random

from .base import SamplingStrategy
from ..datamodel import DataModel
from ..models import Results


class RandomSamplingStrategy(SamplingStrategy):
    def __init__(
        self,
        datamodel: DataModel,
        sample_size: int,
        random_seed: int | None = None,
    ) -> None:
        self.datamodel = datamodel
        self.sample_size = sample_size
        self.random_seed = random_seed

    def run_strategy(self) -> Results:
        rng = random.Random(self.random_seed)

        sampled_records = self.datamodel.get_random_sample(self.sample_size)

        affected_ids = {
            r.true_patient_id for r in sampled_records if r.is_mislabelled == 1
        }

        affected_patients = self.datamodel.get_patients_by_ids(affected_ids)

        return Results(
            sample_size=self.sample_size,
            population_size=self.datamodel.get_population_size(),
            patient_records=sampled_records,
            affected_patients=affected_patients,
        )