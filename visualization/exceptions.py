class VisualizationError(Exception):
    """Exception raised for errors in the data visualization."""

    def __init__(self, message="Error occurred during data visualization"):
        self.message = message
        super().__init__(self.message)
