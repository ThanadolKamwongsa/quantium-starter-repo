import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

DATA_FILE = "formatted_sales_data.csv"

df = pd.read_csv(DATA_FILE)
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

daily_sales = df.groupby("Date", as_index=False)["Sales"].sum()

fig = px.line(
    daily_sales,
    x="Date",
    y="Sales",
    title="Pink Morsel Sales Over Time",
    labels={"Date": "Date", "Sales": "Sales ($)"},
)
fig.add_vline(
    x=pd.Timestamp("2021-01-15").timestamp() * 1000,
    line_dash="dash",
    line_color="red",
    annotation_text="Price increase (2021-01-15)",
    annotation_position="top right",
)

app = Dash(__name__)
app.title = "Soul Foods — Pink Morsel Sales Visualiser"

app.layout = html.Div(
    style={"fontFamily": "Arial, sans-serif", "maxWidth": "1100px", "margin": "0 auto", "padding": "24px"},
    children=[
        html.H1(
            "Soul Foods — Pink Morsel Sales Visualiser",
            style={"textAlign": "center", "color": "#333"},
        ),
        html.P(
            "Were sales higher before or after the Pink Morsel price increase on the 15th of January, 2021?",
            style={"textAlign": "center", "color": "#666"},
        ),
        dcc.Graph(id="sales-line-chart", figure=fig),
    ],
)

if __name__ == "__main__":
    app.run(debug=True, port=8051)
