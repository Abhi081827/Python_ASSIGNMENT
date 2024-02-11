import pandas as pd
from .models import TrainingData, IdealFunctions, TestData, create_session
from .exceptions import DataLoadError

def load_data_to_database(training_data_path, ideal_functions_path, test_data_path):
    """
    Loads data from CSV files into the database.
    """
    try:
        session = create_session()

        # Read data from CSV files
        training_data_df = pd.read_csv(training_data_path)
        ideal_functions_df = pd.read_csv(ideal_functions_path)
        test_data_df = pd.read_csv(test_data_path)

        # Load TrainingData
        for index, row in training_data_df.iterrows():
            record = TrainingData(x=row['x'], y1=row['y1'], y2=row['y2'], y3=row['y3'], y4=row['y4'])
            session.add(record)

        # Load IdealFunctions
        for index, row in ideal_functions_df.iterrows():
            record = IdealFunctions(x=row['x'])
            for i in range(1, 51):
                setattr(record, f"y{i}", row[f"y{i}"])
            session.add(record)

        # Load TestData
        for index, row in test_data_df.iterrows():
            record = TestData(x=row['x'], y=row['y'])
            session.add(record)

        # Commit changes and close the session
        session.commit()
        session.close()
    except Exception as e:
        raise DataLoadError(f"Failed to load data: {e}")


