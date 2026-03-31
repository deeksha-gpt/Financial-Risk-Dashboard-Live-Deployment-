import plotly.graph_objects as go

def create_3d_risk_surface(df):

    fig = go.Figure(data=[go.Surface(
        z=df.pivot(index="strike", columns="expiry", values="gamma").values
    )])

    return fig