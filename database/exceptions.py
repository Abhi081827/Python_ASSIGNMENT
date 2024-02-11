class DataLoadError(Exception):
    """Exception raised for errors in the data loading process."""

    def __init__(self, message="Error occurred while loading data to the database"):
        self.message = message
        super().__init__(self.message)