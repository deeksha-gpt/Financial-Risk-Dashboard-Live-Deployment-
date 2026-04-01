import streamlit as st 
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import requests
import time

# Import advanced modules
from visualization import create_3d_risk_surface
from regulatory import BaselReporting
from ml_models import MLAnomalyDetector


##############################################
# PAGE CONFIG
##############################################

st.set_page_config(
    page_title="Quantitative Risk Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

##############################################
# CUSTOM CSS
##############################################

st.markdown(
    """
    <style>
    .metric-card {
        background-color:#f0f2f6;
        border-radius:10px;
        padding:20px;
        margin:10px 0;
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
    """,
    unsafe_allow_html=True
)


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

        if "auto_refresh" not in st.session_state:
            st.session_state.auto_refresh = True

        if "last_update" not in st.session_state:
            st.session_state.last_update = datetime.now()

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

        try:

            url = f"{self.api_base_url}/{endpoint}"

            response = requests.get(url, params=params, timeout=30)

            response.raise_for_status()

            return response.json()

        except Exception as e:

            st.error(f"API error: {e}")

            return None

    ##########################################
    # HEADER
    ##########################################

    def render_header(self):

        col1, col2, col3 = st.columns([3,1,1])

        with col1:
            st.title("📊 Quantitative Risk Dashboard")

        with col2:
            if st.button("🔄 Refresh"):
                st.session_state.last_update = datetime.now()
                st.rerun()

        with col3:

            st.session_state.auto_refresh = st.checkbox(
                "Auto refresh",
                value=st.session_state.auto_refresh
            )

        st.caption(
            f"Last updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}"
        )

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

            st.session_state.portfolio_id = portfolio_id

            confidence = st.slider(
                "VaR Confidence",
                min_value=90,
                max_value=99,
                value=95
            )

            var_method = st.selectbox(
                "VaR Method",
                ["historical","parametric","monte_carlo"]
            )

            st.divider()

            page = st.radio(
                "View",
                [
                    "Executive Summary",
                    "Risk Metrics",
                    "Stress Tests",
                    "ML Risk Monitoring",
                    "Risk Surface Visualization",
                    "Regulatory Report",
                    "Alerts",
                    "Position Detail"
                ]
            )

        return {

            "portfolio_id": portfolio_id,
            "confidence": confidence/100,
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
        st.metric(
            "1 Day VaR",
            f"${var_data.get('var_1d',0):,.0f}"
        )

    with col2:
        st.metric(
            "Expected Shortfall",
            f"${var_data.get('expected_shortfall',0):,.0f}"
        )
    ##########################################
    # VAR CHART
    ##########################################

    def render_var_chart(self, config):

        st.subheader("📈 VaR Trend")

        data = self.fetch_data(
            "risk/var/history",
            {"portfolio_id":config["portfolio_id"]}
        )

        if not data:
            st.info("No VaR history")
            return

        df = pd.DataFrame(data)

        df["date"] = pd.to_datetime(df["date"])

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=df["date"],
                y=df["var"],
                mode="lines+markers"
            )
        )

        st.plotly_chart(fig, use_container_width=True)

    ##########################################
    # STRESS TEST
    ##########################################

    def render_stress_tests(self, config):

        st.subheader("Stress Tests")

        data = self.fetch_data(
            "stress/results",
            {"portfolio_id":config["portfolio_id"]}
        )

        if not data:
            st.info("No stress data")
            return

        df = pd.DataFrame(data)

        fig = px.bar(
            df,
            x="scenario_name",
            y="pnl_impact",
            color="pnl_impact"
        )

        st.plotly_chart(fig)

        st.dataframe(df)

    ##########################################
    # ML MONITORING
    ##########################################

    def render_ml_monitoring(self):

        st.subheader("🤖 ML Risk Monitoring")

        metrics = {
            "var": 1200000,
            "delta": 450,
            "gamma": 0.12,
            "vega": 1.8
        }

        st.write("Current Risk Metrics")

        st.json(metrics)

        anomaly = False

        if anomaly:

            st.error("🚨 Risk anomaly detected")

        else:

            st.success("Portfolio risk normal")

    ##########################################
    # RISK SURFACE
    ##########################################

    def render_risk_surface(self):

        st.subheader("📊 Gamma Surface")

        data = pd.DataFrame({
            "strike":[90,90,90,100,100,100,110,110,110],
            "expiry":["1M","3M","6M"]*3,
            "gamma":[0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6]
        })

        fig = create_3d_risk_surface(data)

        st.plotly_chart(fig)

    ##########################################
    # REGULATORY REPORT
    ##########################################

    def render_regulatory_report(self):

        st.subheader("📑 Basel III Risk Report")

        reporter = BaselReporting()

        report = reporter.generate_var_report(
            portfolio_id="PF001",
            report_date=datetime.now()
        )

        st.json(report)

    ##########################################
    # ALERTS
    ##########################################

    def render_alerts(self, config):

        st.subheader("🚨 Alerts")

        alerts = self.fetch_data(
            "alerts",
            {"portfolio_id":config["portfolio_id"]}
        )

        if not alerts:

            st.success("No active alerts")

            return

        for a in alerts:

            st.write(a)

    ##########################################
    # POSITIONS
    ##########################################

    def render_positions(self, config):

        st.subheader("📊 Positions")

        data = self.fetch_data(
            f"portfolios/{config['portfolio_id']}/positions"
        )

        if not data:

            st.info("No positions")

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

        elif config["page"] == "Risk Metrics":

            self.render_key_metrics(config)

        elif config["page"] == "Stress Tests":

            self.render_stress_tests(config)

        elif config["page"] == "ML Risk Monitoring":

            self.render_ml_monitoring()

        elif config["page"] == "Risk Surface Visualization":

            self.render_risk_surface()

        elif config["page"] == "Regulatory Report":

            self.render_regulatory_report()

        elif config["page"] == "Alerts":

            self.render_alerts(config)

        elif config["page"] == "Position Detail":

            self.render_positions(config)

        if st.session_state.auto_refresh:

            time.sleep(30)

            st.rerun()


##############################################
# RUN DASHBOARD
##############################################

if __name__ == "__main__":

    dashboard = RiskDashboard()

    dashboard.run()
