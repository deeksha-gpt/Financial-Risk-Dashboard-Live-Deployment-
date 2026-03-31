from fastapi import FastAPI

app = FastAPI()

@app.get("/api/risk/var")
def get_var():
    return {"var_1d":150000, "expected_shortfall":220000}

@app.get("/api/risk/var/history")
def get_var_history():
    return [
        {"date":"2024-01-01","var":120000},
        {"date":"2024-01-02","var":130000}
    ]

@app.get("/api/stress/results")
def stress():
    return [{"scenario_name":"Crash","pnl_impact":-500000}]

@app.get("/api/alerts")
def alerts():
    return [{"message":"VaR breach","severity":"high"}]

@app.get("/api/portfolios/{portfolio_id}/positions")
def positions(portfolio_id:str):
    return [{"instrument_id":"AAPL","position_value":500000}]