from fastapi import FastAPI
from datetime import datetime
import random

app = FastAPI(title="Quant Risk API")


##################################################
# VAR ENDPOINT
##################################################

@app.get("/api/risk/var")
def get_var(portfolio_id: str, confidence: float = 0.95, method: str = "historical"):

    var_value = random.randint(900000, 1400000)
    es_value = int(var_value * 1.3)

    return {
        "portfolio_id": portfolio_id,
        "var_1d": var_value,
        "expected_shortfall": es_value,
        "confidence": confidence,
        "method": method
    }


##################################################
# VAR HISTORY
##################################################

@app.get("/api/risk/var/history")
def get_var_history(portfolio_id: str):

    data = []

    base = 1000000

    for i in range(10):

        base += random.randint(-100000, 100000)

        data.append({
            "date": f"2024-01-{i+1:02d}",
            "var": base
        })

    return data


##################################################
# STRESS TEST RESULTS
##################################################

@app.get("/api/stress/results")
def stress_results(portfolio_id: str):

    return [
        {"scenario_name": "Global Market Crash", "pnl_impact": -2500000},
        {"scenario_name": "Interest Rate Shock", "pnl_impact": -900000},
        {"scenario_name": "Volatility Spike", "pnl_impact": -1500000},
        {"scenario_name": "Oil Price Shock", "pnl_impact": -600000}
    ]


##################################################
# ALERTS
##################################################

@app.get("/api/alerts")
def alerts(portfolio_id: str):

    return [
        {
            "message": "VaR limit exceeded",
            "severity": "HIGH",
            "created_at": str(datetime.now()),
            "details": {
                "limit": 1000000,
                "current_var": 1250000
            }
        },
        {
            "message": "Volatility spike detected",
            "severity": "MEDIUM",
            "created_at": str(datetime.now()),
            "details": {
                "vix_level": 35
            }
        }
    ]


##################################################
# GREEKS
##################################################

@app.get("/api/risk/greeks")
def get_greeks(portfolio_id: str):

    return {
        "delta": random.randint(-5000, 5000),
        "gamma": round(random.uniform(100, 400), 2),
        "vega": round(random.uniform(200, 700), 2),
        "theta": round(random.uniform(-100, -20), 2)
    }


##################################################
# POSITIONS (FIXES YOUR 404 ERROR)
##################################################

@app.get("/api/portfolios/{portfolio_id}/positions")
def get_positions(portfolio_id: str):

    return [
        {
            "instrument_id": "AAPL",
            "asset_class": "Equity",
            "quantity": 120,
            "current_price": 185,
            "position_value": 22200,
            "pnl_today": 500
        },
        {
            "instrument_id": "MSFT",
            "asset_class": "Equity",
            "quantity": 80,
            "current_price": 410,
            "position_value": 32800,
            "pnl_today": -200
        },
        {
            "instrument_id": "TSLA",
            "asset_class": "Equity",
            "quantity": 50,
            "current_price": 240,
            "position_value": 12000,
            "pnl_today": 700
        },
        {
            "instrument_id": "US10Y",
            "asset_class": "Bond",
            "quantity": 100,
            "current_price": 98,
            "position_value": 9800,
            "pnl_today": -50
        }
    ]
