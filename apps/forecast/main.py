import os
import pandas as pd

import config
from data import get_dates, download_data
from prediction import Predictor


def run():
    dates = get_dates(config.DATE_FORMAT, config.LBWS, config.FH)
    stock_data = download_data(
        dates["lbw_bdays"][0],
        dates["today"],
        config.SECURITIES,
        config.LBWS + config.FH,
    )

    predictor = Predictor(
        stock_data,
        dates["next_bdays"],
        config.LBWS,
        config.FH,
        config.SECURITIES,
        config.MODELS_DIR,
        os.path.join(config.MODELS_DIR, "scaler.pkl"),
    )

    forecast = pd.concat(
        [predictor.generate_forecast(model_name) for model_name in config.MODELS],
        ignore_index=True,
    ).merge(stock_data[["ISIN", "Stock"]].drop_duplicates(), on="ISIN")
    forecast.to_csv("forecast.csv", index=False)


if __name__ == "__main__":
    run()
