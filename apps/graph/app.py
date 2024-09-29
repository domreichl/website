from flask import Flask, render_template, request
import plotly.io as pio
import plotly.graph_objects as go
import pandas as pd

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    pr = pd.read_csv("predictions.csv")
    unique_names = pr["Model"].unique()
    unique_criteria = pr["ISIN"].unique()

    selected_name = None
    selected_criteria = request.form.getlist(
        "criteria"
    )  # Assuming you're adding a multi-select for criteria

    if request.method == "POST":
        selected_name = request.form.get("name")
        # Filter the DataFrame based on the selected name
        if selected_name:
            pr = pr[pr["Model"] == selected_name]

        # Further filter based on additional criteria (if applicable)
        if selected_criteria:
            pr = pr[pr["ISIN"].isin(selected_criteria)]

    # Create a plot
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=pr["Date"],
            y=pr["Price"],
            name="actual",
            line=dict(color="navy", width=5),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=pr["Date"],
            y=pr["PricePredicted"],
            name="predicted",
            line=dict(color="blueviolet", width=5),
        )
    )
    fig.update_traces(marker={"size": 12})
    fig.update_layout(
        yaxis_title="Price [€]",
        xaxis=dict(title="Date", tickformat="%b %d"),
    )

    # Render the plot and form
    return render_template(
        "template.html",
        plot=pio.to_html(fig, full_html=False),
        unique_names=unique_names,
        selected_name=selected_name,
        unique_criteria=unique_criteria,
    )


if __name__ == "__main__":
    app.run(debug=True)
