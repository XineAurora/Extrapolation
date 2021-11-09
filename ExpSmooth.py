import pandas as pd


def parse_csv(a):
    data = []
    file = pd.read_csv(a)
    for elem in file["Цена"]:
        new_elem = elem.replace(".", "")
        new_elem = new_elem.replace(",", ".")
        data.append(float(new_elem))
    return data


def exp_smooth(data):
    forecasted_data = []
    forecast = data[0]
    smooth_factor = 0.5
    for value in data:
        forecast = smooth_factor * value + (1 - smooth_factor) * forecast
        forecasted_data.append(forecast)
    for i in range(30):
        forecast = smooth_factor * forecasted_data[len(forecasted_data) - 1] + (1 - smooth_factor) * forecast
        forecasted_data.append(forecast)
    return forecasted_data
