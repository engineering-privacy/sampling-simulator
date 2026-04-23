from .datawriter import DataWriter
from .experiment import Experiment


def calculate_sample_size(
    error_rate: float,
    confidence_level: float,
) -> int:
    sample_size = 1

    while True:
        detection_probability = 1 - ((1 - error_rate) ** sample_size)

        if detection_probability >= confidence_level:
            return sample_size

        sample_size += 1


def main() -> None:
    use_calculated_sample_size = True

    num_patients = 100
    num_records = 1000
    mode = "percentage"
    mislabelled_percentage = 1.0
    stochastic_error_rate = None
    num_trials = 1000
    random_seed = 42
    confidence_level = 0.95

    if use_calculated_sample_size:
        if mode == "percentage":
            error_rate = mislabelled_percentage / 100
        elif mode == "stochastic":
            error_rate = stochastic_error_rate
        else:
            raise ValueError("mode must be 'percentage' or 'stochastic'")

        sample_size = calculate_sample_size(
            error_rate=error_rate,
            confidence_level=confidence_level,
        )
    else:
        sample_size = 300

    experiment = Experiment(
        db_name="sampling_simulation",
        num_patients=num_patients,
        num_records=num_records,
        mode=mode,
        mislabelled_percentage=mislabelled_percentage,
        stochastic_error_rate=stochastic_error_rate,
        sample_size=sample_size,
        num_trials=num_trials,
        random_seed=random_seed,
    )

    results = experiment.run()
    print("Writing results workbook...")
    writer = DataWriter("outputs/simulation_results.xlsx")
    writer.write(results)

    print(f"Sample size: {sample_size}")
    print(f"Trials: {results.total_trials}")
    print(f"Detections: {results.detections}")
    print(f"Detection rate: {results.detection_rate:.2%}")


if __name__ == "__main__":
    main()