# 📊 Risk Analytics Dashboard

A full-stack financial risk analytics platform that provides real-time portfolio risk monitoring, stress testing, and regulatory reporting using modern data science and visualization tools.

---

## 🌐 Live Demo

🔗 **Dashboard:** https://live-financial-risk-dashboard.streamlit.app
🔗 **API Docs:** https://financial-risk-dashboard-live-deployment-6j9f.onrender.com/docs

---

## 🚀 Features

### 📉 Risk Metrics

* 1-Day Value at Risk (VaR)
* Expected Shortfall (ES)
* Historical VaR trend visualization

### 📊 Stress Testing

* Predefined macroeconomic scenarios:

  * Global Market Crash
  * Interest Rate Shock
  * Volatility Spike
  * Oil Price Shock

### 🤖 ML Risk Monitoring

* Anomaly detection using Isolation Forest
* Detects unusual portfolio risk behavior

### 📈 Risk Surface Visualization

* 3D Gamma surface across strike & expiry
* Interactive Plotly visualizations

### 📑 Regulatory Reporting

* Basel III compliant VaR reporting
* Capital charge calculation
* Backtesting results

### 🚨 Alerts System

* Real-time risk alerts
* Severity-based highlighting (HIGH / MEDIUM)

### 📊 Portfolio Positions

* Instrument-level breakdown
* PnL tracking and exposure analysis

---

## 🏗️ Tech Stack

**Frontend**

* Streamlit
* Plotly
* Pandas

**Backend**

* FastAPI
* Uvicorn

**Machine Learning**

* Scikit-learn (Isolation Forest)
* PyTorch (LSTM for VaR prediction)

**Deployment**

* Streamlit Cloud (Frontend)
* Render (Backend API)

---

## 📂 Project Structure

```
.
├── app.py               # Streamlit dashboard
├── api_server.py        # FastAPI backend
├── ml_models.py         # ML models (Anomaly Detection, LSTM)
├── regulatory.py        # Basel III reporting logic
├── visualization.py     # 3D risk surface plots
├── requirements.txt     # Dependencies
```

---

## ⚙️ How to Run Locally

### 1️⃣ Clone repository

```bash
git clone https://github.com/your-username/quant-risk-dashboard.git
cd quant-risk-dashboard
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run backend

```bash
uvicorn api_server:app --reload
```

### 4️⃣ Run frontend

```bash
streamlit run app.py
```

---

## 🌍 Deployment Architecture

```
Streamlit (Frontend)
        ↓
FastAPI (Render Backend)
        ↓
Risk Models + Simulations
```

---

## 📌 Key Highlights

* Full-stack financial analytics system
* Real-time API-driven architecture
* Interactive dashboards for decision-making
* Scalable deployment with cloud services
* Combines finance + ML + data visualization

---

## 🔮 Future Enhancements

* Live market data integration (Yahoo Finance / APIs)
* User authentication system
* Portfolio upload (CSV / Excel)
* Advanced Monte Carlo simulation engine
* Downloadable PDF risk reports

---

## 👩‍💻 Author

**Deeksha Gupta**
Aspiring Data Scientist | Financial Analytics Enthusiast

---

## ⭐ If you like this project

Give it a ⭐ on GitHub and feel free to fork or contribute!
