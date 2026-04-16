import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

DATA_FILE = "formatted_sales_data.csv"

df = pd.read_csv(DATA_FILE)
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

REGIONS = ["north", "east", "south", "west", "all"]
PRICE_INCREASE_MS = pd.Timestamp("2021-01-15").timestamp() * 1000

COLORS = {
    "background": "#0b1220",
    "panel": "#111a2e",
    "accent": "#3b82f6",
    "text": "#e6ecff",
    "muted": "#8aa0c7",
    "grid": "#1f2a44",
}

app = Dash(__name__)
app.title = "Soul Foods — Pink Morsel Sales Visualiser"

app.layout = html.Div(
    style={
        "fontFamily": "'Helvetica Neue', Arial, sans-serif",
        "backgroundColor": COLORS["background"],
        "minHeight": "100vh",
        "padding": "32px 16px",
    },
    children=[
        html.Div(
            style={
                "maxWidth": "1100px",
                "margin": "0 auto",
                "backgroundColor": COLORS["panel"],
                "borderRadius": "12px",
                "boxShadow": "0 4px 24px rgba(0,0,0,0.45)",
                "border": f"1px solid {COLORS['grid']}",
                "padding": "32px",
            },
            children=[
                html.H1(
                    "Soul Foods — Pink Morsel Sales Visualiser",
                    style={
                        "textAlign": "center",
                        "color": COLORS["accent"],
                        "marginBottom": "8px",
                        "fontWeight": "700",
                    },
                ),
                html.P(
                    "Were sales higher before or after the Pink Morsel price "
                    "increase on the 15th of January, 2021?",
                    style={
                        "textAlign": "center",
                        "color": COLORS["muted"],
                        "fontSize": "16px",
                        "marginBottom": "28px",
                    },
                ),
                html.Div(
                    style={
                        "display": "flex",
                        "flexDirection": "column",
                        "alignItems": "center",
                        "marginBottom": "20px",
                    },
                    children=[
                        html.Label(
                            "Filter by region:",
                            style={
                                "fontWeight": "600",
                                "color": COLORS["text"],
                                "marginBottom": "8px",
                            },
                        ),
                        dcc.RadioItems(
                            id="region-filter",
                            options=[{"label": r.capitalize(), "value": r} for r in REGIONS],
                            value="all",
                            inline=True,
                            labelStyle={
                                "marginRight": "18px",
                                "color": COLORS["text"],
                                "cursor": "pointer",
                            },
                            inputStyle={"marginRight": "6px"},
                        ),
                    ],
                ),
                dcc.Graph(id="sales-line-chart"),
            ],
        ),
    ],
)


@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-filter", "value"),
)
def update_chart(region):
    data = df if region == "all" else df[df["Region"] == region]
    daily = data.groupby("Date", as_index=False)["Sales"].sum()

    fig = px.line(
        daily,
        x="Date",
        y="Sales",
        title=f"Pink Morsel Sales Over Time ({region.capitalize()})",
        labels={"Date": "Date", "Sales": "Sales ($)"},
    )
    fig.update_traces(line=dict(color=COLORS["accent"], width=2))
    fig.update_layout(
        plot_bgcolor=COLORS["panel"],
        paper_bgcolor=COLORS["panel"],
        font=dict(family="'Helvetica Neue', Arial, sans-serif", color=COLORS["text"]),
        title_x=0.5,
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis=dict(gridcolor=COLORS["grid"], zerolinecolor=COLORS["grid"]),
        yaxis=dict(gridcolor=COLORS["grid"], zerolinecolor=COLORS["grid"]),
    )
    fig.add_vline(
        x=PRICE_INCREASE_MS,
        line_dash="dash",
        line_color=COLORS["muted"],
        annotation_text="Price increase (2021-01-15)",
        annotation_position="top right",
        annotation_font_color=COLORS["muted"],
    )
    return fig


if __name__ == "__main__":
    app.run(debug=True, port=8051)
