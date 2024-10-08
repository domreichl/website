import urllib.request
import pandas as pd
import numpy as np
from datetime import datetime


def get_dates(date_format: str, lbws: int, fh: int) -> dict:
    today = pd.Timestamp(datetime.today().date())
    lbw_bdays = pd.date_range(
        end=today - pd.offsets.BDay(1), periods=lbws + fh * 3, freq="B"
    )
    prev_bdays = [
        bday.strftime(date_format)
        for bday in pd.date_range(end=today - pd.offsets.BDay(1), periods=fh, freq="B")
    ]
    next_bdays = [
        bday.strftime(date_format)
        for bday in pd.date_range(start=today, periods=fh, freq="B")
    ]
    return dict(
        today=today, lbw_bdays=lbw_bdays, prev_bdays=prev_bdays, next_bdays=next_bdays
    )


def download_data(
    start_date: datetime, end_date: datetime, securities: dict, total_days: int
) -> pd.DataFrame:
    dfs = []
    columns = ["ISIN", "Stock", "Date", "Close"]
    for isin, security in securities.items():
        date_format = "%d.%m.%Y"
        if security == "ATX-AT0000999982":
            url = f"https://www.wienerborse.at/indizes/aktuelle-indexwerte/historische-daten/?ISIN=AT0000999982&ID_NOTATION=92866&c7012%5BDATETIME_TZ_END_RANGE%5D={end_date.strftime(date_format)}&c7012%5BDATETIME_TZ_START_RANGE%5D={start_date.strftime(date_format)}&c7012%5BDOWNLOAD%5D=csv"
        else:
            url = f"https://www.wienerborse.at/aktien-prime-market/{security}/historische-daten/?c48840%5BDOWNLOAD%5D=csv&c48840%5BDATETIME_TZ_END_RANGE%5D={end_date.strftime(date_format)}&c48840%5BDATETIME_TZ_START_RANGE%5D={start_date.strftime(date_format)}T00%3A00%3A00%2B01%3A00"
        with urllib.request.urlopen(url) as csv_file:
            df = pd.read_csv(csv_file, sep=";")
            df["ISIN"] = isin
            df["Stock"] = "-".join(security.split("-")[:-1])
            df["Date"] = pd.to_datetime(df["Datum"], format=date_format)
            df["Close"] = df["Schlusspreis"].str.replace(",", ".").astype(float)
            dfs.append(df[columns])
    df = pd.concat(dfs)
    df = df.sort_values(by="Date").reset_index(drop=True)
    df["Close"] = df["Close"].ffill()
    df["LogReturn"] = pd.concat(
        [
            np.log(
                df[df["ISIN"] == isin]["Close"]
                / df[df["ISIN"] == isin]["Close"].shift(1)
            )
            for isin in df["ISIN"].unique()
        ]
    )
    df["LogReturn"] = df["LogReturn"].fillna(0.0)
    df = df[df["Date"].isin(list(df["Date"].unique())[-total_days:])]

    return df
