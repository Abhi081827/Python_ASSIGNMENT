import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from processing.data_handler import process_training_data, map_test_data

class TestProcessing(unittest.TestCase):

    def setUp(self):
        # Setup an in-memory SQLite database for testing
        self.engine = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool)
        self.mock_session = sessionmaker(bind=self.engine)()

    @patch('processing.data_handler.create_session')
    @patch('processing.data_handler.pd.read_sql')
    def test_process_training_data(self, mock_read_sql, mock_create_session):
        # Configure the mock session and mock_read_sql
        mock_create_session.return_value = self.mock_session
        mock_training_data = pd.DataFrame({'x': [1, 2], 'y1': [1, 2], 'y2': [2, 3], 'y3': [3, 4], 'y4': [4, 5]})
        mock_ideal_functions = pd.DataFrame({'x': [1, 2], **{f'y{i}': [i, i+1] for i in range(1, 51)}})
        mock_read_sql.side_effect = [mock_training_data, mock_ideal_functions]

        # Call the function under test
        selection, max_deviation = process_training_data()

        # Asserts to validate the results
        self.assertIsInstance(selection, dict)
        self.assertIsInstance(max_deviation, dict)

    @patch('processing.data_handler.create_session')
    @patch('processing.data_handler.pd.read_sql')
    def test_map_test_data(self, mock_read_sql, mock_create_session):
        # Configure the mock session and mock_read_sql
        mock_create_session.return_value = self.mock_session
        mock_test_data = pd.DataFrame({'x': [1], 'y': [2]})
        mock_ideal_functions = pd.DataFrame({'x': [1, 2], **{f'y{i}': [i, i+1] for i in range(1, 51)}})
        mock_read_sql.side_effect = [mock_test_data, mock_ideal_functions]

        ideal_function_selection = {'y1': 'y1', 'y2': 'y2', 'y3': 'y3', 'y4': 'y4'}
        max_deviation = {'y1': 1, 'y2': 1, 'y3': 1, 'y4': 1}

        # Call the function under test
        results = map_test_data(ideal_function_selection, max_deviation)

        # Asserts to validate the results
        self.assertIsInstance(results, pd.DataFrame)

if __name__ == '__main__':
    unittest.main()
