import math
from statsmodels.tsa.api import ExponentialSmoothing
import numpy as np


def linear(a, b, x):
    return a * x + b


def quadratic(a, b, c, x):
    return a * x ** 2 + b * x + c


def logarithmic(a, b, x):
    return a * math.log(x) + b


def exponential(a, b, x):
    return a * math.exp(x) + b


def holt_win_fcast(data, forecast_length):
    exp_fit = ExponentialSmoothing(data, seasonal_periods=7, trend='add', seasonal='add',
                                   damped_trend=True, use_boxcox=True).fit()
    exp_forecast = exp_fit.forecast(forecast_length)
    return exp_forecast
