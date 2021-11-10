import math
import sys
import ExpSmooth
import algebraicFunctions


def linear_approximation(data):
    alpha1_1 = 0
    alpha2 = 0
    sum_x = 0
    sum_y = 0
    for i in range(len(data)):
        alpha1_1 += i * data[i] * 1.0 / len(data)
        alpha2 += i * i * 1.0 / len(data)
        sum_x += i * 1.0 / len(data)
        sum_y += data[i] * 1.0 / len(data)
    a = (alpha1_1 - sum_x * sum_y) / (alpha2 - sum_x * sum_x)
    b = sum_y - a * sum_x
    return a, b


def quadratic_approximation(data):
    alpha2_1 = 0.
    alpha1_1 = 0.
    alpha0_1 = 0.
    alpha4 = 0.
    alpha3 = 0.
    alpha2 = 0.
    alpha1 = 0.
    for i in range(len(data)):
        alpha2_1 += data[i] * i ** 2 / len(data)
        alpha1_1 += data[i] * i / len(data)
        alpha0_1 += data[i] / len(data)
        alpha4 += i ** 4 / len(data)
        alpha3 += i ** 3 / len(data)
        alpha2 += i ** 2 / len(data)
        alpha1 += i / len(data)
    k = (alpha1_1 - alpha0_1 * alpha1) * (alpha3 - alpha2 * alpha1) / (alpha2 - alpha1 ** 2)
    a = (alpha2_1 - alpha0_1 * alpha2 - k) / (
            alpha4 - alpha2 ** 2 - ((alpha3 - alpha2 * alpha1) ** 2 / (alpha2 - alpha1 ** 2)))
    b = (alpha1_1 - alpha0_1 * alpha1 - a * (alpha3 - alpha2 * alpha1)) / (alpha2 - alpha1 ** 2)
    c = alpha0_1 - a * alpha2 - b * alpha1
    return a, b, c


def logarithmic_approximation(data):
    alpha1_1 = 0.
    alpha0_1 = 0.
    alpha2 = 0.
    alpha1 = 0.
    for i in range(len(data)):
        alpha1_1 += data[i] * math.log(i + 1) / len(data)
        alpha0_1 += data[i] / len(data)
        alpha2 += math.log(i + 1) ** 2 / len(data)
        alpha1 += math.log(i + 1) / len(data)
    a = (alpha1_1 - alpha0_1 * alpha1) / (alpha2 - alpha1 ** 2)
    b = alpha0_1 - a * alpha1
    return a, b


def exponential_approximation(data):
    alpha1_1 = 0.
    alpha0_1 = 0.
    alpha2 = 0.
    alpha1 = 0.
    for i in range(len(data)):
        alpha1_1 += data[i] * math.exp(i) / len(data)
        alpha0_1 += data[i] / len(data)
        alpha2 += math.exp(i) ** 2 / len(data)
        alpha1 += math.exp(i) / len(data)
    a = (alpha1_1 - alpha0_1 * alpha1) / (alpha2 - alpha1 ** 2)
    b = alpha0_1 - a * alpha1
    return a, b


def calculate_error(function, coefficients, data, start_index):
    error = 0.
    if function == algebraicFunctions.holt_win_fcast:
        for i in range(len(data)):
            error += (data[i] - coefficients[i]) ** 2
    elif function != algebraicFunctions.logarithmic:
        for i in range(len(data)):
            error += (data[i] - function(*coefficients, start_index)) ** 2
    else:
        for i in range(len(data)):
            error += (data[i] - function(*coefficients, start_index + 1)) ** 2
    return error


def choose_method(data, data_to_train, data_to_test, forecast_length):
    smooth_data = ExpSmooth.exp_smooth(data)
    min_error = sys.float_info.max
    method_type = ''
    method_coef = ()
    tmp_coef = linear_approximation(smooth_data)
    tmp_error = calculate_error(algebraicFunctions.linear, tmp_coef, data_to_test, len(data_to_train))
    if tmp_error < min_error:
        min_error = tmp_error
        method_type = algebraicFunctions.linear
        method_coef = tmp_coef

    tmp_coef = quadratic_approximation(smooth_data)
    tmp_error = calculate_error(algebraicFunctions.quadratic, tmp_coef, data_to_test, len(data_to_train))
    if tmp_error < min_error:
        min_error = tmp_error
        method_type = algebraicFunctions.quadratic
        method_coef = tmp_coef

    tmp_coef = logarithmic_approximation(smooth_data)
    tmp_error = calculate_error(algebraicFunctions.logarithmic, tmp_coef, data_to_test, len(data_to_train))
    if tmp_error < min_error:
        min_error = tmp_error
        method_type = algebraicFunctions.logarithmic
        method_coef = tmp_coef

    tmp_coef = exponential_approximation(smooth_data)
    tmp_error = calculate_error(algebraicFunctions.exponential, tmp_coef, data_to_test, len(data_to_train))
    if tmp_error < min_error:
        min_error = tmp_error
        method_type = algebraicFunctions.exponential
        method_coef = tmp_coef

    tmp_coef = algebraicFunctions.holt_win_fcast(data_to_train, [], len(data_to_test))
    tmp_error = calculate_error(algebraicFunctions.holt_win_fcast, tmp_coef, data_to_test, len(data_to_train))
    if tmp_error < min_error:
        min_error = tmp_error
        method_type = algebraicFunctions.holt_win_fcast
        method_coef = algebraicFunctions.holt_win_fcast(data, [], forecast_length)

    return method_type, method_coef, min_error


def extrapolate(data, period):
    train_index = math.floor(0.8 * len(data))
    data_to_train = data[:train_index]
    data_to_test = data[train_index:]

    method = choose_method(data, data_to_train, data_to_test, period)
    if method[0] == algebraicFunctions.holt_win_fcast:
        print(data)
        print(method[1])
        return [x for x in range(len(data) + period)], data + method[1].tolist()
    elif method[0] != algebraicFunctions.logarithmic:
        return [x for x in range(len(data) + period)], \
               [method[0](*method[1], x) for x in range(len(data) + period)]
    else:
        return [x for x in range(len(data) + period)], \
               [method[0](*method[1], x) for x in range(1, len(data) + period + 1)]
