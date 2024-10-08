from flask import Flask, render_template, request
import plotly.io as pio
import plotly.graph_objects as go
import pandas as pd

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    MODEL = "exp_smoothing"
    prices = pd.read_csv("/home/wisigern/forecast/recent_prices.csv").rename(
        columns={"Close": "Price"}
    )
    pr = pd.read_csv("/home/wisigern/forecast/forecast.csv")
    pr = pd.concat(
        [
            pr[pr["Model"] == MODEL],
            prices[prices["Date"] == prices["Date"].max()].assign(Model=MODEL),
        ]
    )
    pr.sort_values(["Date", "Stock"], inplace=True)
    stocks = pr["ISIN"].unique()

    if request.method == "POST":
        selected_stock = request.form.get("ISIN")
    else:
        selected_stock = stocks[0]

    pr = pr[pr["ISIN"] == selected_stock]
    prices = prices[prices["ISIN"] == selected_stock]
    selected_stock_name = str(pr[pr["ISIN"] == selected_stock]["Stock"].iloc[0])

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=pr["Date"],
            y=pr["Price"],
            name="forecast",
            line=dict(color="blueviolet", width=5),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=prices["Date"],
            y=prices["Price"],
            name="actual",
            line=dict(color="navy", width=5),
        )
    )
    fig.update_traces(marker={"size": 12})
    fig.update_layout(
        title={
            "text": f"10-Day Forecast for Stock '{selected_stock_name}'",
            "y": 0.98,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": dict(size=20, color="white"),
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        yaxis_title="Price [€]",
        xaxis=dict(title="Date", tickformat="%b %d"),
        margin=dict(l=80, r=80, t=25, b=80),
    )

    return render_template(
        "template.html",
        plot=pio.to_html(fig, full_html=False),
        stocks=stocks,
        selected_stock=selected_stock,
    )


if __name__ == "__main__":
    app.run(debug=True)
