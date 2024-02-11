from .calculations import sum_of_squared_deviations, calculate_deviation
from database.models import TrainingData, IdealFunctions, TestData, create_session
import numpy as np
import pandas as pd
from .exceptions import DataProcessingError

def process_training_data():
    """
    Processes the training data to find the ideal functions with the minimum deviation.
    """
    try:
        session = create_session()

        # Fetch data from database
        training_data = pd.read_sql(session.query(TrainingData).statement, session.bind)
        ideal_functions = pd.read_sql(session.query(IdealFunctions).statement, session.bind)

        # Logic to select ideal functions based on minimum deviation
        ideal_function_selection = {}
        max_deviation = {}
        for training_column in ['y1', 'y2', 'y3', 'y4']:
            min_deviation = float('inf')
            best_function = None

            for ideal_column in ideal_functions.columns[1:]:  # Skip 'X' column
                deviation = sum_of_squared_deviations(training_data[training_column], ideal_functions[ideal_column])
                if deviation < min_deviation:
                    min_deviation = deviation
                    best_function = ideal_column

            ideal_function_selection[training_column] = best_function
            max_deviation[training_column] = min_deviation

        session.close()
    except Exception as e:
        raise DataProcessingError(f"Data processing error process training data: {e}")
    return ideal_function_selection, max_deviation

def map_test_data(ideal_function_selection,max_deviation):
    """
    Maps test data to the selected ideal functions and calculates the deviations.
    """
    try:
        session = create_session()

        # Fetch test data and ideal functions from database
        test_data = pd.read_sql(session.query(TestData).statement, session.bind)
        ideal_functions = pd.read_sql(session.query(IdealFunctions).statement, session.bind)
        max_deviation_factor = np.sqrt(2)
        # Logic for mapping test data to ideal functions and calculating deviation
        # Iterate over each row in test data
        test_data_results = pd.DataFrame(columns=['x', 'y', 'DeltaY', 'IdealFunctionNumber'])
        for index, row in test_data.iterrows():
            x_value = row['x']
            y_value = row['y']
            best_match = None
            min_deviation = float('inf')

            # Compare with each selected ideal function
            for train_col, ideal_col in ideal_function_selection.items():
                ideal_y_value = ideal_functions.loc[ideal_functions['x'] == x_value, ideal_col].values[0]
                deviation = calculate_deviation(y_value, ideal_y_value)

                # Check if the deviation is within the allowed range and is the minimum so far
                if deviation < max_deviation[train_col] * max_deviation_factor and deviation < min_deviation:
                    best_match = ideal_col
                    min_deviation = deviation

            # Add the result to the DataFrame
            if best_match:
                test_data_results.loc[len(test_data_results)] = [x_value, y_value, min_deviation, best_match]
        


        session.close()
    except Exception as e:
        raise DataProcessingError(f"Data processing error map test data: {e}")
    return test_data_results


