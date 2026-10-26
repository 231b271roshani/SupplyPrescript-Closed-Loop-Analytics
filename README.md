# SupplyPrescript — Closed-Loop Prescriptive Analytics

An ML-powered supply chain decision-support system that predicts shipment delays, recommends cost-effective actions, and evaluates real-world outcomes to improve future decisions.

##Overview

Traditional predictive analytics tells businesses what might happen, but it does not always explain what action they should take.

**SupplyPrescript** aims to bridge this gap by combining machine learning, mathematical optimization, and interactive analytics in a single application.

The system predicts potential supply chain disruptions, evaluates alternative actions based on cost and time constraints, and helps users make informed operational decisions.


## Problem Statement

Supply chain disruptions can cause shipment delays, increased transportation costs, inventory shortages, and missed product-launch deadlines.

Organizations need a system that can:

- Predict shipment delays using historical data.
- Recommend alternative actions based on business constraints.
- Compare cost, delivery time, and operational trade-offs.
- Record decisions and evaluate their actual outcomes.
- Use outcome analysis to improve future recommendations.

## Key Features

- **Shipment Delay Prediction:** Estimate shipment delays using machine learning.
- **Prescriptive Analytics:** Recommend suitable actions using mathematical optimization.
- **Cost Optimization:** Compare alternative decisions under budget and time constraints.
- **Interactive Dashboard:** Visualize predictions, recommendations, and trade-offs.
- **Decision Tracking:** Store selected actions and their outcomes.
- **Closed-Loop Feedback:** Compare predicted and actual results to inform future model improvements.

*These features describe the intended project scope. Individual features will be marked complete as they are implemented and tested.*

## Proposed Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Machine Learning | XGBoost / Scikit-learn |
| Optimization | SciPy / PuLP |
| Backend API | FastAPI |
| Database | PostgreSQL |
| Frontend | React / Next.js |
| Data Analysis | Pandas, NumPy |
| Visualization | Plotly / Matplotlib |
| Version Control | Git and GitHub |

## System Architecture

```text
Historical Supply Chain Data
            |
            v
     Data Preprocessing
            |
            v
 Shipment Delay Prediction
       (Machine Learning)
            |
            v
  Prescriptive Optimization
  (Cost, Time, Capacity)
            |
            v
  Recommended Alternatives
            |
            v
   Interactive Dashboard
            |
            v
    User Decision
            |
            v
   Database Write-Back
            |
            v
 Actual Outcome Evaluation
            |
            v
   Model Improvement
```

## Example Use Case

Imagine a shipment of microchips is predicted to arrive 14 days late.

SupplyPrescript could evaluate alternatives such as:

1. **Air Freight:** Pay additional transportation costs to reduce delivery time.
2. **Alternative Supplier:** Purchase from another supplier at a price premium.
3. **Delay the Launch:** Accept the delay to avoid additional procurement costs.

The optimization engine compares feasible alternatives according to configured business constraints and presents the trade-offs to the user.

The final decision remains subject to business requirements and user approval.

## Project Structure

```text
SupplyPrescript-Closed-Loop-Analytics/
├── backend/
│   └── main.py
├── ml/
│   ├── data.py
│   └── train_model.py
├── data/                 # Generated sample CSV and local SQLite database
├── tests/
│   └── test_week_one.py
├── requirements.txt
└── README.md
```

The initial implementation uses FastAPI and SQLite as a local foundation; PostgreSQL and a separate React frontend remain possible future replacements as the product grows.

## Getting Started

### Prerequisites

- Python 3.11.
- Git.

### 1. Install dependencies

```bash
python -m venv .venv
```

Activate the environment, then install the pinned dependencies:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

On macOS/Linux, activate it with:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Generate data and train the baseline

The command below creates a reproducible 600-row fictional shipment dataset at `data/sample_shipments.csv`, cleans and labels it, evaluates an XGBoost classifier using a stratified 75/25 train/test split, and saves the model and metrics under `ml/artifacts/`.

```bash
python -m ml.train_model
```

Features include supplier, product, order and promised dates, shipping method and cost, and weather, port, and supplier disruption indicators. The delay target is derived from actual versus promised delivery dates; actual outcomes are excluded from model inputs.

Metrics include accuracy, precision, recall, F1, ROC AUC, and the dataset's delay rate. `random_state=42` keeps data generation and evaluation reproducible. On the generated 600-row sample, the baseline held-out metrics were accuracy **0.76**, precision **0.4737**, recall **0.2571**, F1 **0.3333**, and ROC AUC **0.6976**. This is an initial benchmark, not a production-ready model.

### 3. Start the application

```bash
uvicorn backend.main:app --reload
```

Open `http://127.0.0.1:8000/` for the shipment lookup page. Enter an ID such as `SP-00001` to view shipment details and its predicted delay probability. The API is documented at:

`http://127.0.0.1:8000/docs`

The API also provides `GET /api/shipments` and `GET /api/shipments/{shipment_id}`. SQLite creates `data/supplyprescript.db` and imports the generated shipment records at startup. Set `SUPPLYPRESCRIPT_DB` to use a different database file.

### 4. Run focused tests

```bash
pytest -q
```

Generated data, model artifacts, and the local database are runtime outputs; delete them to recreate the sample and model from scratch.

## Evaluation Metrics

The project will evaluate predictive and operational performance using suitable metrics.

### Machine Learning

- Mean Absolute Error (MAE), where predicting delay duration.
- Root Mean Squared Error (RMSE), where predicting delay duration.
- Precision, Recall, and F1-score, where classifying delayed shipments.
- Appropriate validation on unseen data.

### Optimization and Business Outcomes

- Total recommended cost.
- Expected delivery time.
- Budget and capacity constraint violations.
- Difference between predicted and actual outcomes.
- Decision success rate, when supported by defined outcome criteria.

## Development Roadmap

- [x] Generate and clean reproducible sample supply-chain data.
- [x] Train and evaluate a baseline shipment-delay classifier.
- [x] Add local persistence, API endpoints, and an individual shipment lookup.
- [ ] Develop the optimization engine.
- [ ] Integrate PostgreSQL for decisions and outcomes.
- [ ] Create the interactive dashboard.
- [ ] Implement decision tracking and outcome evaluation.
- [ ] Test the complete workflow.
- [x] Document the Week 1 workflow and local run instructions.

## Collaboration

Contributions are welcome.

1. Fork the repository or obtain collaborator access.
2. Create a feature branch.
3. Implement and test your changes.
4. Submit a pull request for review.

Example:

```bash
git checkout -b feature/shipment-prediction
git add .
git commit -m "Add shipment delay prediction"
git push -u origin feature/shipment-prediction
```

## Future Enhancements

- Real-time shipment tracking integration.
- Advanced optimization under uncertainty.
- Model monitoring and drift detection.
- Automated retraining based on verified outcome data.
- Cloud deployment and role-based access control.

## License

This project can be distributed under the MIT License once the repository owner adds the appropriate `LICENSE` file.

## Author

**Project:** SupplyPrescript — Closed-Loop Prescriptive Analytics

**Domain:** Supply Chain Analytics, Machine Learning, and Operations Research

Developed as an advanced Data Analytics portfolio project.
