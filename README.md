# 🔍 Sampling Simulator

A tool to simulate and evaluate the effectiveness of sampling strategies for detecting data issues.

This project accompanies the article on sampling for data control validation. It allows you to:

- derive a sample size from an assumed error rate and confidence level
- generate synthetic datasets with controlled error rates
- run repeated sampling experiments
- observe how often issues are actually detected in practice

The goal is to bridge the gap between theory and real-world behaviour.

---

## ⚙️ What it does

Given:
- a population size (`N`)
- an assumed error rate (`r`)
- a desired confidence level (`C`)

You can:

1. calculate a required sample size
2. generate a dataset with simulated errors
3. run repeated sampling trials
4. observe the detection rate

This helps answer:

> “If errors exist at rate *r*, how likely is my sampling approach to detect at least one?”

---

## 🏗️ Project Structure

```text
src/samplingsim/
├── models.py          # shared data structures
├── datamodel.py       # database access layer (SQLite)
├── datagenerator.py   # synthetic data generation
├── experiment.py      # experiment orchestration
├── datawriter.py      # Excel output
├── main.py            # entrypoint
└── strategies/
    ├── base.py
    └── samplestrategy.py   # random sampling implementation

---

## 🚀 Setup

Create and activate a virtual environment:

```bash 
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install faker openpyxl
```

---

## ▶️ Running the Simulation


From the project root:

```
PYTHONPATH=src python -m samplingsim.main
```

This will:

- generate a dataset
- run multiple sampling trials
- output results to an Excel file
- print a summary to the terminal


## 📊 Example Output

```bash
Sample size: 300
Trials: 1000
Detections: 982
Detection rate: 98.20%
```

--- 

## 🧠 Key Idea

This tool is not just about sampling — it is about confidence in detection.

It demonstrates that:

- small samples can easily miss real issues
- detection probability depends on assumptions
- repeated trials converge on theoretical expectations

---

## 🔮 Future Improvements

- support multiple sampling strategies
- CLI interface for configuring experiments
- more precise sample size calculations (hypergeometric)
- performance optimisations for large datasets

---

## 📄 License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).

See the `LICENSE` file for full details.