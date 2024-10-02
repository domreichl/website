from flask import Flask, render_template, request
import plotly.io as pio
import plotly.graph_objects as go
import pandas as pd

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    pr = pd.read_csv("predictions.csv")
    models = pr["Model"].unique()
    stocks = pr["ISIN"].unique()

    selected_model = models[0]
    selected_stock = stocks[0]

    if request.method == "POST":
        if selected_model := request.form.get("Model"):
            pr = pr[pr["Model"] == selected_model]
        if selected_stock := request.form.get("ISIN"):
            pr = pr[pr["ISIN"] == selected_stock]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=pr["Date"],
            y=pr["Price"],
            name="recent",
            line=dict(color="navy", width=5),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=pr["Date"],
            y=pr["PricePredicted"],
            name="forecast",
            line=dict(color="blueviolet", width=5),
        )
    )
    fig.update_traces(marker={"size": 12})
    # TODO: display plot title with Company Name (!) based on ISIN
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="white",
        yaxis_title="Price [€]",
        xaxis=dict(title="Date", tickformat="%b %d"),
        margin=dict(l=80, r=80, t=20, b=80),
    )

    return render_template(
        "template.html",
        plot=pio.to_html(fig, full_html=False),
        models=models,
        stocks=stocks,
        selected_model=selected_model,
        selected_stock=selected_stock,
    )


if __name__ == "__main__":
    app.run(debug=True)
