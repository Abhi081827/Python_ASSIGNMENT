class DataProcessingError(Exception):
    """Exception raised for errors in the data processing."""

    def __init__(self, message="Error occurred during data processing"):
        self.message = message
        super().__init__(self.message)