"""
Gradient boosting model for taking lat/long/date

pip install xgboost pandas fastparquet
"""

import sys
import pickle
import json

import numpy as np
import pandas as pd
import xgboost as xgb

path = '../backend/Python/xg_dewst/'

_dewst:xgb.XGBRFRegressor = xgb.XGBRFRegressor()
_dewst.load_model(path + "dewst01.model")

_history = pd.read_parquet(path + "history.parquet")
_cities = pd.read_parquet(path + "cities.parquet")
with open(path + "city_kd.pkl", "rb") as f:
    _kdtree = pickle.load(f)

def _get_feat_names():
    X_feat = ["Longitude", "Latitude", "day", "month", "year"]
    y_feat = ["tempmin", "tempmean", "tempmax", "tdmean", "vpdmin", "vpdmax"]

    return X_feat, y_feat

def _compute_nearest_city(latitude, longitude):
    dist, index = _kdtree.query([latitude, longitude])
    return _cities["Name"][index]

def _get_date_range(date_str, days_back, days_forward):
    dt_str = pd.to_datetime(date_str)

    start = dt_str - pd.Timedelta(days=days_back - 1)
    back_range = pd.date_range(start=start, end=dt_str)

    start = dt_str + pd.Timedelta(days=1)
    end = dt_str + pd.Timedelta(days=days_forward)
    forward_range = pd.date_range(start=start, end=end)
    
    return back_range, forward_range


def _get_history_dict(pred_df, back_range):
    hist = pred_df.loc[back_range]
    hist["date"] = hist.index.strftime("%Y-%m-%d")
    return hist.set_index("date").T.to_dict()

def _make_predictions(pred_df, forward_range, n_shift=5):
    """i am not proud, but i am angry"""
    def shift_cols(df, n, feat):
        for i in range(1, n+1):
            df[f"{feat}-{i}"] = df[feat].shift(i)

    X_feat, y_feat = _get_feat_names()

    start = forward_range[0] - pd.Timedelta(days=5)
    end = forward_range[-1]
    date_range = pd.date_range(start=start, end=end)
    pred_df = pred_df.loc[date_range]

    for feat in y_feat:
        shift_cols(pred_df, n_shift, feat)
        for i in range(n_shift):
            X_feat.append(f"{feat}-{i+1}")

    pred_df = pred_df.reset_index()

    pred_df["day"] = pred_df["index"].dt.day
    pred_df["month"] = pred_df["index"].dt.month
    pred_df["year"] = pred_df["index"].dt.year

    start_cols = ["Longitude", "Latitude", "day", "month", "year"]
    new_order = start_cols + [col for col in pred_df.columns if col not in start_cols + y_feat]
    pred_df = pred_df[new_order].drop("Name", axis=1).set_index("index")

    X = np.array(pred_df.loc[forward_range])
    y = _dewst.predict(X)

    y_df = pd.DataFrame(y, columns=y_feat)
    y_df["date"] = forward_range.strftime("%Y-%m-%d")

    return y_df.set_index("date").T.to_dict()


def project_climate_metrics(
    latitude: float, 
    longitude: float, 
    date: str,  # ex 2020-07-31
    days_back=5,
    days_forward=5,
) -> list[dict]:
    """
    returns a list of 2 dictionaries representing metrics for days_back days
    (inclusive) and (prognosticated) days_forward days in the future

    date is string of YYYY-MM-DD (ex 2020-07-31)
    """
    nearest_city = _compute_nearest_city(latitude, longitude)

    back_range, forward_range = _get_date_range(date, days_back, days_forward)

    pred_df = _history[_history["Name"] == nearest_city].set_index("dt")

    history_dict = _get_history_dict(pred_df, back_range)

    prediction_dict = _make_predictions(pred_df, forward_range)

    return [
        nearest_city,
        history_dict,
        prediction_dict
    ]
    

if __name__ == "__main__":
    # print(project_climate_metrics(-74.0, 29, "2021-08-21"))

    latitude = sys.argv[1]
    longitude = sys.argv[2]
    date_str = sys.argv[3]

    data = project_climate_metrics(latitude, longitude, date_str)#, history_days, predict_days)

    print(json.dumps(data))
