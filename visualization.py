import plotly.graph_objects as go
import pandas as pd


def create_3d_risk_surface(portfolio_data: pd.DataFrame) -> go.Figure:
    """Create 3D surface plot of risk metrics."""

    pivot = portfolio_data.pivot(
        index='strike',
        columns='expiry',
        values='gamma'
    )

    fig = go.Figure(
        data=[
            go.Surface(
                z=pivot.values,
                x=pivot.columns,
                y=pivot.index,
                colorscale='Viridis'
            )
        ]
    )

    fig.update_layout(
        title="Gamma Surface",
        scene=dict(
            xaxis_title="Expiry",
            yaxis_title="Strike",
            zaxis_title="Gamma"
        ),
        height=600
    )

    return fig
