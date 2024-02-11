import numpy as np
def sum_of_squared_deviations(y_actual, y_predicted):
    """
    Calculates the sum of squared deviations between actual and predicted values.

    :param y_actual: Array of actual values.
    :param y_predicted: Array of predicted values.
    :return: Sum of squared deviations.
    """
    return sum((y_actual - y_predicted) ** 2)


def calculate_deviation(y_actual, y_predicted):
    return np.abs(y_actual - y_predicted)

