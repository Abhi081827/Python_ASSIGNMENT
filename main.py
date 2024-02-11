from database.models import create_session, TrainingData, IdealFunctions, TestData
from database.operations import load_data_to_database
from processing.data_handler import process_training_data, map_test_data
from visualization.plots import create_plots
import pandas as pd
import sys

def main():
    """
    Main function to run the application.
    """
    try:
        # Database Initialization
        session = create_session()

        # Data Loading
        print("Loading data into database...")
        load_data_to_database('Data/train.csv', 'Data/ideal.csv', 'Data/test.csv')

        # Fetching data from database
        print("Fetching data for processing and visualization...")
        training_data = pd.read_sql(session.query(TrainingData).statement, session.bind)
        ideal_functions = pd.read_sql(session.query(IdealFunctions).statement, session.bind)

        # Data Processing
        print("Processing training data...")
        ideal_function_selection, max_deviation = process_training_data()

        print("Mapping test data...")
        test_data_results = map_test_data(ideal_function_selection,max_deviation)
        print(test_data_results)

        # Data Visualization
        print("Creating visualizations...")
        create_plots(training_data, ideal_functions, test_data_results, ideal_function_selection)

        session.close()

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
