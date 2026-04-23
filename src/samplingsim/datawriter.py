from pathlib import Path

from openpyxl import Workbook

from .models import ExperimentResults


class DataWriter:
    def __init__(self, output_path: str | Path) -> None:
        self.output_path = Path(output_path)

    def write(self, experiment_results: ExperimentResults) -> None:
        workbook = Workbook()

        summary_sheet = workbook.active
        summary_sheet.title = "summary"

        summary_sheet.append(["total_trials", "detections", "detection_rate"])
        summary_sheet.append(
            [
                experiment_results.total_trials,
                experiment_results.detections,
                experiment_results.detection_rate,
            ]
        )

        trial_sheet = workbook.create_sheet(title="trial_results")
        trial_sheet.append(
            [
                "trial_number",
                "sample_size",
                "population_size",
                "sampled_records",
                "affected_patients",
                "detected_issue",
            ]
        )

        for index, result in enumerate(experiment_results.trial_results, start=1):
            detected_issue = len(result.affected_patients) > 0
            trial_sheet.append(
                [
                    index,
                    result.sample_size,
                    result.population_size,
                    len(result.patient_records),
                    len(result.affected_patients),
                    detected_issue,
                ]
            )
    
            self.output_path.parent.mkdir(parents=True, exist_ok=True)
            workbook.save(self.output_path)