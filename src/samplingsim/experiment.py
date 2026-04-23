from .datamodel import DataModel
from .datagenerator import RecordsGenerator
from .models import ExperimentResults, Results
from .strategies.samplestrategy import RandomSamplingStrategy


class Experiment:
    def __init__(
        self,
        db_name: str,
        num_patients: int,
        num_records: int,
        mode: str,
        sample_size: int,
        num_trials: int,
        mislabelled_percentage: float | None = None,
        stochastic_error_rate: float | None = None,
        random_seed: int | None = None,
    ) -> None:
        self.datamodel = DataModel(db_name)

        self.num_patients = num_patients
        self.num_records = num_records
        self.mode = mode

        self.sample_size = sample_size
        self.num_trials = num_trials

        self.mislabelled_percentage = mislabelled_percentage
        self.stochastic_error_rate = stochastic_error_rate

        self.random_seed = random_seed

    def run(self) -> ExperimentResults:
        generator = RecordsGenerator(self.datamodel, mode=self.mode)

        print("Generating dataset...")
        generator.populate_db(
            num_patients=self.num_patients,
            num_records=self.num_records,
            mislabelled_percentage=self.mislabelled_percentage,
            stochastic_error_rate=self.stochastic_error_rate,
        )

        results: list[Results] = []
        print("Running simulation trials...")
        for i in range(self.num_trials):
            if i % 100 == 0:
                print(f"Running trial {i + 1} of {self.num_trials}...")

            seed = self.random_seed + i if self.random_seed else None

            strategy = RandomSamplingStrategy(
                datamodel=self.datamodel,
                sample_size=self.sample_size,
                random_seed=seed,
            )

            results.append(strategy.run_strategy())

        detections = sum(1 for r in results if len(r.affected_patients) > 0)

        return ExperimentResults(
            trial_results=results,
            total_trials=self.num_trials,
            detections=detections,
            detection_rate=detections / self.num_trials,
        )