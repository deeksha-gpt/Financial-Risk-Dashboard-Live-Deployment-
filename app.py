import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import requests
import time

# Import modules
from visualization import create_3d_risk_surface
from regulatory import BaselReporting


##############################################
# PAGE CONFIG
##############################################

st.set_page_config(
    page_title="Quantitative Risk Dashboard",
    page_icon="📊",
    layout="wide",
)

##############################################
# CUSTOM CSS
##############################################

st.markdown("""
<style>
.metric-card {
    background-color:#f0f2f6;
    border-radius:10px;
    padding:20px;
}
.critical-alert{
    background-color:#ff4b4b;
    color:white;
    padding:10px;
    border-radius:5px;
}
.warning-alert{
    background-color:#ffa500;
    color:white;
    padding:10px;
    border-radius:5px;
}
</style>
""", unsafe_allow_html=True)


##############################################
# DASHBOARD CLASS
##############################################

class RiskDashboard:

    def __init__(self):
        self.api_base_url = "https://financial-risk-dashboard-live-deployment-6j9f.onrender.com/api"
        self.init_session_state()

    ##########################################

    def init_session_state(self):
        if "portfolio_id" not in st.session_state:
            st.session_state.portfolio_id = "PF001"

    ##########################################
    # FIXED FETCH FUNCTION (Retry + Timeout)
    ##########################################

    def fetch_data(self, endpoint, params=None):

        url = f"{self.api_base_url}/{endpoint}"

        for i in range(3):
            try:
                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()
                return response.json()

            except Exception as e:
                if i < 2:
                    time.sleep(5)
                else:
                    st.error(f"API error: {e}")
                    return None

    ##########################################
    # HEADER
    ##########################################

    def render_header(self):
        st.title("📊 Quantitative Risk Dashboard")

    ##########################################
    # SIDEBAR
    ##########################################

    def render_sidebar(self):

        with st.sidebar:
            st.header("Controls")

            portfolio_id = st.text_input(
                "Portfolio ID",
                value=st.session_state.portfolio_id
            )

            confidence = st.slider("Confidence", 90, 99, 95)
            var_method = st.selectbox("Method", ["historical", "monte_carlo"])

            page = st.radio("View", [
                "Executive Summary",
                "Stress Tests",
                "Alerts",
                "Positions"
            ])

        return {
            "portfolio_id": portfolio_id,
            "confidence": confidence / 100,
            "var_method": var_method,
            "page": page
        }

    ##########################################
    # KEY METRICS
    ##########################################

    def render_key_metrics(self, config):

        st.subheader("🎯 Key Risk Metrics")

        with st.spinner("Fetching live risk data..."):
            var_data = self.fetch_data(
                "risk/var",
                {
                    "portfolio_id": config["portfolio_id"],
                    "confidence": config["confidence"],
                    "method": config["var_method"]
                }
            )

        if not var_data:
            st.warning("No data")
            return

        col1, col2 = st.columns(2)

        with col1:
            st.metric("VaR", f"${var_data.get('var_1d',0):,.0f}")

        with col2:
            st.metric("Expected Shortfall", f"${var_data.get('expected_shortfall',0):,.0f}")

    ##########################################
    # VAR CHART
    ##########################################

    def render_var_chart(self, config):

        st.subheader("📈 VaR Trend")

        with st.spinner("Loading VaR trend..."):
            data = self.fetch_data(
                "risk/var/history",
                {"portfolio_id": config["portfolio_id"]}
            )

        if not data:
            return

        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["date"], y=df["var"]))

        st.plotly_chart(fig, use_container_width=True)

    ##########################################
    # STRESS TEST
    ##########################################

    def render_stress_tests(self, config):

        st.subheader("📊 Stress Tests")

        data = self.fetch_data(
            "stress/results",
            {"portfolio_id": config["portfolio_id"]}
        )

        if not data:
            return

        df = pd.DataFrame(data)

        fig = px.bar(df, x="scenario_name", y="pnl_impact")
        st.plotly_chart(fig)

    ##########################################
    # ALERTS
    ##########################################

    def render_alerts(self, config):

        st.subheader("🚨 Alerts")

        alerts = self.fetch_data(
            "alerts",
            {"portfolio_id": config["portfolio_id"]}
        )

        if not alerts:
            return

        for a in alerts:
            if a["severity"] == "HIGH":
                st.markdown(f"<div class='critical-alert'>{a['message']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='warning-alert'>{a['message']}</div>", unsafe_allow_html=True)

    ##########################################
    # POSITIONS
    ##########################################

    def render_positions(self, config):

        st.subheader("📊 Positions")

        data = self.fetch_data(
            f"portfolios/{config['portfolio_id']}/positions"
        )

        if not data:
            return

        df = pd.DataFrame(data)
        st.dataframe(df)

    ##########################################
    # RUN APP
    ##########################################

    def run(self):

        self.render_header()
        config = self.render_sidebar()

        if config["page"] == "Executive Summary":
            self.render_key_metrics(config)
            self.render_var_chart(config)

        elif config["page"] == "Stress Tests":
            self.render_stress_tests(config)

        elif config["page"] == "Alerts":
            self.render_alerts(config)

        elif config["page"] == "Positions":
            self.render_positions(config)


##############################################
# RUN
##############################################

if __name__ == "__main__":
    app = RiskDashboard()
    app.run()
