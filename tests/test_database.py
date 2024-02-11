import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from database.operations import load_data_to_database
from database.exceptions import DataLoadError

class TestDatabaseOperations(unittest.TestCase):

    @patch('database.operations.pd.read_csv')
    @patch('database.operations.create_session')
    def test_load_data_to_database(self, mock_create_session, mock_read_csv):
        # Mock the session to avoid actual database operations
        mock_session = MagicMock()
        mock_create_session.return_value = mock_session

        # Setup mock data frames with required structure
        mock_ideal_functions_data = pd.DataFrame({f"y{i}": [1.0] for i in range(1, 51)})
        mock_ideal_functions_data['x'] = [1.0]
        mock_training_data = pd.DataFrame({'x': [1.0], 'y1': [1.0], 'y2': [2.0], 'y3': [3.0], 'y4': [4.0]})
        mock_test_data = pd.DataFrame({'x': [1.0], 'y': [1.0]})

        # Setup read_csv mock to return the correct DataFrame based on input
        def read_csv_side_effect(file_path):
            if 'train' in file_path:
                return mock_training_data
            elif 'ideal' in file_path:
                return mock_ideal_functions_data
            elif 'test' in file_path:
                return mock_test_data
            else:
                raise ValueError("Unexpected file path")

        mock_read_csv.side_effect = read_csv_side_effect

        # Call the function
        load_data_to_database('mock_train.csv', 'mock_ideal.csv', 'mock_test.csv')

        # Assert if the add and commit methods were called
        self.assertTrue(mock_session.add.called)
        self.assertTrue(mock_session.commit.called)

    @patch('database.operations.pd.read_csv')
    @patch('database.operations.create_session')
    def test_load_data_to_database_error(self, mock_create_session, mock_read_csv):
        # Mock the session to simulate a database error
        mock_session = MagicMock()
        mock_create_session.return_value = mock_session
        mock_session.add.side_effect = SQLAlchemyError("DB Error")

        # Setup mock data frames
        mock_read_csv.return_value = pd.DataFrame({'x': [1.0], 'y1': [1.0], 'y2': [2.0], 'y3': [3.0], 'y4': [4.0]})

        # Assert if DataLoadError is raised on database error
        with self.assertRaises(DataLoadError):
            load_data_to_database('mock_train.csv', 'mock_ideal.csv', 'mock_test.csv')

if __name__ == '__main__':
    unittest.main()
