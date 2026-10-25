# SupplyPrescript — Closed-Loop Prescriptive Analytics

An ML-powered supply chain decision-support system that predicts shipment delays, recommends cost-effective actions, and evaluates real-world outcomes to improve future decisions.

## Overview

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
│   ├── main.py
│   ├── routes/
│   └── services/
├── frontend/
├── ml/
│   ├── preprocessing.py
│   ├── train_model.py
│   └── predict.py
├── optimization/
│   └── optimizer.py
├── data/
├── notebooks/
├── tests/
├── .gitignore
├── requirements.txt
└── README.md
```

*The structure is a proposed starting point and may change as development progresses.*

## Getting Started

### Prerequisites

- Python 3.11 or a compatible version.
- Node.js and npm, if using the Next.js frontend.
- PostgreSQL, if database integration is enabled.
- Git.

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/SupplyPrescript-Closed-Loop-Analytics.git
cd SupplyPrescript-Closed-Loop-Analytics
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a Python virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Or on macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install Python dependencies

Once `requirements.txt` has been created:

```bash
pip install -r requirements.txt
```

### 4. Run the backend

After the FastAPI application has been implemented:

```bash
uvicorn backend.main:app --reload
```

The API documentation will typically be available at:

`http://127.0.0.1:8000/docs`

### 5. Run the frontend

After the frontend has been created:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000` in your browser.

*These commands assume the proposed files and application entry points exist. They will need adjustment if your implementation uses a different structure.*

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

- [ ] Collect or generate sample supply chain data.
- [ ] Clean data and perform exploratory analysis.
- [ ] Train and evaluate the shipment-delay prediction model.
- [ ] Develop the optimization engine.
- [ ] Build the FastAPI backend.
- [ ] Integrate PostgreSQL for decisions and outcomes.
- [ ] Create the interactive dashboard.
- [ ] Implement decision tracking and outcome evaluation.
- [ ] Test the complete workflow.
- [ ] Document results and deployment instructions.

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
