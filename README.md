\# SupplyPrescript — Closed-Loop Prescriptive Analytics



SupplyPrescript predicts shipment delays using a Random Forest model and recommends actions based on predicted risk.



\## Features

\- Manual shipment data entry

 Random Forest delay prediction

\- FastAPI backend

\- Next.js dashboard

\- Risk-based recommendations



\## Project Structure

\- backend/ — API and ML training scripts

\- data/ — Shipment dataset

\- models/ — Trained model

\- frontend/ — Next.js dashboard



\## Run Backend

Install dependencies:



&#x20;   python -m pip install -r backend/requirements.txt



Start the API from the repository root:



&#x20;   python -m uvicorn main:app --app-dir backend --port 8001



API documentation: http://127.0.0.1:8001/docs



\## Run Frontend

Open another terminal:



&#x20;   cd frontend

&#x20;   npm install

&#x20;   npm run dev



Dashboard: http://localhost:3000

