import plotly.express as px
import plotly.graph_objects as go


def plot_range(result, phase: str = None):
    if phase is None:
        df = result
    else:
        df = result.loc[result["phase"] == phase.upper()]
    
    fig = go.Figure(data=go.Scatter(x=df["timestamp"], y=df["value"],
                    mode="lines", name="value", line_color="#0066ff", fill=None))
    fig = fig.add_trace(go.Scatter(x=df["timestamp"], y=df["minValue"],
                        mode="lines", name="minValue", line_color="#33ccff", fill=None, line=dict(dash="dot")))
    fig = fig.add_trace(go.Scatter(x=df["timestamp"], y=df["maxValue"],
                        mode="lines", name="maxValue", line_color="#ff9999", fill=None, line=dict(dash="dot"), fillcolor="rgba(204,238,255,0.5)"))
    
    return fig


def plot_phase(result):
    df = result.loc[:,["timestamp", "value", "phase"]]
    return px.line(data_frame=df, x="timestamp", y="value", color="phase")


def plot_detail(result):
    df = result.loc[:, ["timestamp", "value", "phase"]]
    return px.line(data_frame=df, x="timestamp", y="value", color="phase", facet_row="phase")


def plot_dist(result):
    df = result.loc[:,["timestamp", "value", "phase"]]

    return px.box(data_frame=df, x="phase", y="value", color="phase", points="all")