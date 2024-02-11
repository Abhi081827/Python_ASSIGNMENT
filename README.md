# Project README

## Project Title: Python Assingment

### Organization: IU.ORG

---

### Description

This Python project is designed to fulfill the requirements of the written assignment for the course "DLMDSPWP01 – Programming with Python" at IU.ORG. The project involves developing a Python application to analyze training and test datasets, select ideal functions based on least-square deviation, and visualize the results.

### Folder Structure

- 📁 **Project**
    - 📁 **Data**
        - `train.csv`
        - `test.csv`
        - `ideal.csv`
    - 📁 **database**
        - `__init__.py`
        - `models.py`: Defines SQLAlchemy models.
        - `operations.py`: Handles data loading and session creation.
        -  `exceptions.py` : Custom Exception
    - 📁 **processing**
        - `__init__.py`
        - `calculations.py`: Performs deviation calculations.
        - `data_handler.py`: Processes data from the database.
        - `exceptions.py` : Custom Exception
    - 📁 **visualization**
        - `__init__.py`
        - `plots.py`: Generates Bokeh plots for data visualization.
        - `exceptions.py` : Custom Exception
    - 📁 **tests**
        - `test_database.py`
        - `test_processing.py`
    - 📁 **output**
        - 📁 **database**
            - `data_analysis.db`
        - 📁 **visualization**
            - `datdata_visualization.html`

    - `main.py`: Main application script.

### Project Features

- **Object-Oriented Design**: The project is structured in an object-oriented manner, including the use of inheritance.
- **Exception Handling**: Implements both standard and user-defined exception handling.
- **Data Handling**: Utilizes Pandas for data manipulation and SQLAlchemy for database operations.
- **Visualization**: Employs Bokeh for data visualization.
- **Unit Testing**: Includes unit tests for key components of the application.
- **Documentation**: Every module, class, and method includes docstrings for clear documentation.

### Installation and Setup

1. Clone the project repository.
2. Install required dependencies:
    ```
    pip install -r requirements.txt
    ```
3. Run `main.py` to start the application:
    ```
    python main.py
    ```

### Usage

1. Load the provided training and test datasets into the application.
2. The application will process the data, perform analysis, and select ideal functions based on the least-square deviation criterion.
3. The test data will be mapped to the selected ideal functions, with deviations calculated and recorded.
4. Visualization of the data and the analysis results can be viewed through the generated Bokeh plots.

---

*This README serves as a guide for the Python project. Modify as necessary to fit the specific requirements of your assignment and organization.*

