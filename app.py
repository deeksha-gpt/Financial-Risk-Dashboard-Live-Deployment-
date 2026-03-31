import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import time

from visualization import create_3d_risk_surface
from regulatory import BaselReporting
from ml_models import MLAnomalyDetector

st.set_page_config(page_title="Quantitative Risk Dashboard", layout="wide")


class RiskDashboard:

    def __init__(self):
        self.init_session_state()

    def init_session_state(self):
        if "portfolio_id" not in st.session_state:
            st.session_state.portfolio_id = "PF001"

    ##########################################
    # MOCK DATA (FIXED ORDER)
    ##########################################

    def fetch_data(self, endpoint):

        if "risk/var/history" in endpoint:
            return [
                {"date": "2024-01-01", "var": 120000},
                {"date": "2024-01-02", "var": 130000},
                {"date": "2024-01-03", "var": 125000},
                {"date": "2024-01-04", "var": 140000},
                {"date": "2024-01-05", "var": 135000},
            ]

        if "risk/var" in endpoint:
            return {
                "var_1d": 150000,
                "expected_shortfall": 220000
            }

        if "stress/results" in endpoint:
            return [
                {"scenario_name": "2008 Crisis", "pnl_impact": -500000},
                {"scenario_name": "COVID Crash", "pnl_impact": -300000},
                {"scenario_name": "Rate Shock", "pnl_impact": -150000},
            ]

        if "alerts" in endpoint:
            return [
                {"message": "VaR limit breached", "severity": "High"}
            ]

        if "positions" in endpoint:
            return [
                {"asset_class": "Equity", "instrument_id": "AAPL", "position_value": 500000, "pnl_today": 5000},
                {"asset_class": "Equity", "instrument_id": "GOOG", "position_value": 300000, "pnl_today": -2000},
            ]

        return None

    ##########################################
    # SIDEBAR
    ##########################################

    def render_sidebar(self):
        with st.sidebar:
            st.title("Controls")

            page = st.radio(
                "Navigation",
                [
                    "Executive Summary",
                    "Stress Tests",
                    "ML Monitoring",
                    "Risk Surface",
                    "Regulatory Report",
                    "Alerts",
                    "Positions"
                ]
            )

        return {"page": page}

    ##########################################
    # COMPONENTS
    ##########################################

    def render_summary(self):
        data = self.fetch_data("risk/var")

        col1, col2 = st.columns(2)
        col1.metric("VaR", f"${data['var_1d']:,}")
        col2.metric("Expected Shortfall", f"${data['expected_shortfall']:,}")

    def render_var_chart(self):
        data = self.fetch_data("risk/var/history")

        if not data:
            st.warning("No data")
            return

        df = pd.DataFrame(data)

        if "date" not in df.columns:
            st.error("Wrong data format")
            return

        df["date"] = pd.to_datetime(df["date"])

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["date"], y=df["var"], mode="lines+markers"))

        st.plotly_chart(fig, use_container_width=True)

    def render_stress(self):
        df = pd.DataFrame(self.fetch_data("stress/results"))
        st.plotly_chart(px.bar(df, x="scenario_name", y="pnl_impact"))
        st.dataframe(df)

    def render_ml(self):
        st.subheader("ML Monitoring")

        detector = MLAnomalyDetector()

        metrics = {"var": 120000, "delta": 400, "gamma": 0.2, "vega": 1.5}

        st.json(metrics)
        st.success("No anomaly detected")

    def render_surface(self):
        df = pd.DataFrame({
            "strike":[90,90,90,100,100,100,110,110,110],
            "expiry":["1M","3M","6M"]*3,
            "gamma":[0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6]
        })

        fig = create_3d_risk_surface(df)
        st.plotly_chart(fig)

    def render_regulatory(self):
        report = BaselReporting().generate_var_report("PF001", datetime.now())
        st.json(report)

    def render_alerts(self):
        alerts = self.fetch_data("alerts")
        for a in alerts:
            st.error(a["message"])

    def render_positions(self):
        df = pd.DataFrame(self.fetch_data("positions"))
        st.dataframe(df)

    ##########################################
    # RUN
    ##########################################

    def run(self):

        config = self.render_sidebar()

        st.title("📊 Quantitative Risk Dashboard")

        self.render_summary()
        self.render_var_chart()

        if config["page"] == "Stress Tests":
            self.render_stress()

        elif config["page"] == "ML Monitoring":
            self.render_ml()

        elif config["page"] == "Risk Surface":
            self.render_surface()

        elif config["page"] == "Regulatory Report":
            self.render_regulatory()

        elif config["page"] == "Alerts":
            self.render_alerts()

        elif config["page"] == "Positions":
            self.render_positions()


if __name__ == "__main__":
    app = RiskDashboard()
    app.run()