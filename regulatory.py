from datetime import datetime

class BaselReporting:

    def generate_var_report(self, portfolio_id, report_date):

        return {
            "portfolio_id": portfolio_id,
            "report_date": str(report_date),
            "var_10d_99": 500000,
            "stressed_var": 700000,
            "capital_charge": 800000
        }