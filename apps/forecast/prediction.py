import os
import joblib
import numpy as np
import pandas as pd
from prophet import Prophet
from tensorflow.keras.models import load_model
from sktime.forecasting.arima import ARIMA
from sktime.forecasting.exp_smoothing import ExponentialSmoothing


class Predictor:
    def __init__(
        self,
        data: pd.DataFrame,
        dates: int,
        lbws: int,
        fh: int,
        securities: dict,
        models_dir: str,
        scaler_path: str,
    ):
        self.data = data
        self.dates = dates
        self.lbws = lbws
        self.fh = fh
        self.securities = securities
        self.models_dir = models_dir
        self.scaler = joblib.load(scaler_path)
        self.x, self.y = self._prepare_features()

    def generate_forecast(self, model_name: str) -> pd.DataFrame:
        y_preds = self._predict(model_name)
        price_col, isin_col = [], []
        for isin, pred in y_preds.items():
            returns = np.exp(
                np.squeeze(self.scaler.inverse_transform(np.array(pred).reshape(-1, 1)))
            )
            price = float(
                self.data[self.data["ISIN"] == isin]["Close"].tolist()[-self.fh]
            )
            for r in returns:
                price *= r
                price_col.append(round(price, 2))
                isin_col.append(isin)
        forecast = pd.DataFrame(
            {
                "ISIN": isin_col,
                "Price": price_col,
                "Date": self.dates * len(y_preds),
            }
        ).assign(Model=model_name)
        return forecast

    def _prepare_features(self) -> tuple:
        x_dict, y_dict = {}, {}
        for isin in self.securities.keys():
            log_returns = np.array(self.data[self.data["ISIN"] == isin]["LogReturn"])
            x_dict[isin], y_dict[isin] = [], []
            for i in range(self.fh):
                x_dict[isin].append(log_returns[i : i + self.lbws])
                y_dict[isin].append(log_returns[i + self.lbws])
        x = np.stack([np.array(features) for features in x_dict.values()], 2)
        y = np.stack([np.array(labels) for labels in y_dict.values()], 1)
        x_scaled = self.scaler.transform(x.reshape(-1, 1)).reshape(
            self.fh, self.lbws, len(self.securities)
        )
        y_scaled = self.scaler.transform(y.reshape(-1, 1)).reshape(
            self.fh, len(self.securities)
        )
        return x_scaled, y_scaled

    def _predict(self, model_name: str) -> dict:
        match model_name:
            case "arima":
                y_preds = self._predict_sktime(
                    ARIMA(
                        order=(0, 0, 0),
                        seasonal_order=(0, 0, 0, 0),
                        suppress_warnings=True,
                    )
                )
            case "exp_smoothing":
                y_preds = self._predict_sktime(ExponentialSmoothing())
            case "lgbm_regressor":
                y_preds = self._predict_boosting(model_name)
            case "nn_regressor":
                y_preds = self._predict_neural_net(model_name)
            case "prophet":
                y_preds = self._predict_prophet()
            case "rnn_regressor":
                y_preds = self._predict_neural_net(model_name)
            case "xgb_regressor":
                y_preds = self._predict_boosting(model_name)
            case _:
                raise Exception(f"Model {model_name} not implemented.")
        return y_preds

    def _predict_boosting(self, model_name: str) -> dict:
        model = joblib.load(os.path.join(self.models_dir, f"{model_name}.pkl"))
        y_preds = self._init_y_preds()
        x = self._get_full_features()
        train_days = self._get_train_days()
        for i in range(self.fh):
            y_hat = []
            model.fit(self._build_train_df(x, train_days))
            result = model.predict(h=1)
            for isin in self.securities.keys():
                y_hat.append(
                    float(
                        result[result["unique_id"] == isin][result.columns[2]].iloc[0]
                    )
                )
                y_preds[isin].append(y_hat[-1])
            x = np.concatenate([x[1:], np.expand_dims(y_hat, 0)], axis=0)
            train_days = train_days[1:] + [self.dates[i]]
        return y_preds

    def _predict_neural_net(self, model_name: object, lbws: int = 25) -> dict:
        model = load_model(os.path.join(self.models_dir, f"{model_name}.keras"))
        model.fit(x=self.x[:, -lbws:, :], y=self.y)
        x = np.concatenate([self.x[-1, -lbws + self.fh :, :], self.y], axis=0)
        result = np.squeeze(model.predict(np.expand_dims(x, 0)))
        y_preds = {
            isin: list(result[:, i]) for i, isin in enumerate(self.securities.keys())
        }
        return y_preds

    def _predict_prophet(self):
        y_preds = self._init_y_preds()
        x = self._get_full_features()
        train_days = self._get_train_days()
        for i in range(self.fh):
            y_hat = []
            train_df = self._build_train_df(x, train_days)
            for isin in self.securities.keys():
                model = Prophet(
                    growth="flat",
                    daily_seasonality=True,
                    weekly_seasonality=False,
                    yearly_seasonality=False,
                ).fit(train_df[train_df["unique_id"] == isin])
                result = model.predict(
                    model.make_future_dataframe(
                        periods=1, freq="B", include_history=False
                    )
                )
                y_hat.append(float(result["yhat"].iloc[0]))
                y_preds[isin].append(y_hat[-1])
            x = np.concatenate([x[1:], np.expand_dims(y_hat, 0)], axis=0)
            train_days = train_days[1:] + [self.dates[i]]
        return y_preds

    def _predict_sktime(self, model: object) -> dict:
        y_preds = self._init_y_preds()
        x = np.concatenate([self.x[-self.fh, :, :], self.y], 0)
        for i in range(self.fh):
            result = np.squeeze(model.fit_predict(x, fh=1))
            for i, isin in enumerate(self.securities.keys()):
                y_preds[isin].append(result[i])
            x = np.concatenate([x[1:], np.expand_dims(result, 0)], axis=0)
        return y_preds

    def _get_full_features(self) -> np.array:
        return np.concatenate([self.x[-1, -self.lbws + self.fh :, :], self.y], axis=0)

    def _get_train_days(self) -> np.array:
        return list(self.data["Date"].unique()[-self.lbws :])

    def _init_y_preds(self) -> dict:
        return {isin: [] for isin in self.securities.keys()}

    def _build_train_df(self, x: np.array, train_days: list) -> pd.DataFrame:
        train_df = (
            pd.DataFrame(
                {isin: x[:, i] for i, isin in enumerate(self.securities.keys())},
                index=train_days,
            )
            .unstack()
            .reset_index()
        )
        train_df.columns = ["unique_id", "ds", "y"]
        train_df["ds"] = pd.to_datetime(train_df["ds"])
        return train_df
