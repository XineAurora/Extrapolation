import minimalSquare
import algebraicFunctions
import ExpSmooth
import matplotlib.pyplot as plt

tests = [
    [2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2.3, 2.8, 4.1, 5.1, 5.9, 6.9, 8],
    [algebraicFunctions.quadratic(-4, 0.2, 3, k) + (5 if k % 2 == 0 else -5) for k in range(0, 10)],
    [algebraicFunctions.logarithmic(10, 4, k) + (0.2 if (k % 2 == 0) else -0.2) for k in range(1, 15)],
    [algebraicFunctions.exponential(0.02, 5, k) + (0.2 if (k % 2 == 0) else -0.2) for k in range(0, 15)]
]

"""Можно не использовать ExpSmooth.py"""
""""""

# for test in tests:
#     plt.plot(test)
#     plt.plot(*minimalSquare.extrapolate(test, 15))
#     plt.show()

bitcoin_data = ExpSmooth.parse_csv('bitcoin3.csv')
smooth_data = ExpSmooth.exp_smooth(ExpSmooth.parse_csv('bitcoin3.csv'))
research_length = 50
forecast_length = 15
for i in range(int(len(bitcoin_data) / research_length) - 1):
    plt.plot(bitcoin_data[i * research_length:(i + 1) * research_length + forecast_length])
    tmp = minimalSquare.extrapolate(smooth_data[i * research_length:(i + 1) * research_length], forecast_length)
    plt.plot(tmp[0][:research_length], tmp[1][:research_length])
    plt.plot(tmp[0][research_length - 1:], tmp[1][research_length - 1:])
    plt.show()
