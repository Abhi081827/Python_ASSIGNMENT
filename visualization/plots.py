from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.layouts import gridplot
from bokeh.palettes import Category20
import pandas as pd
import numpy as np
from bokeh.layouts import column
from bokeh.models import Slider, CustomJS
from bokeh.models import HoverTool, BoxZoomTool, BoxSelectTool, TapTool, Slider, CustomJS
from .exceptions import VisualizationError

def create_plots(training_data, ideal_functions, test_data_results, ideal_function_selection):
    """
    Creates and displays plots for training data, ideal functions, and test data results.

    :param training_data: DataFrame containing training data.
    :param ideal_functions: DataFrame containing ideal functions data.
    :param test_data_results: DataFrame containing test data results.
    :param ideal_function_selection: Dictionary mapping training columns to ideal functions.
    """
    # Data sources
    try:
        training_source = ColumnDataSource(training_data)
        ideal_source = ColumnDataSource(ideal_functions)
        test_source = ColumnDataSource(test_data_results)


        p_deviations = figure(title="Deviations in Test Data", x_axis_label='X', y_axis_label='Delta Y', tools="pan,wheel_zoom,box_zoom,reset")
        p_test_and_ideal = figure(title="Test Data and Ideal Functions", x_axis_label='X', y_axis_label='Y', tools="pan,wheel_zoom,box_zoom,reset")
        p_training_and_ideal = figure(title="Training Data and Ideal Functions", x_axis_label='X', y_axis_label='Y', tools="pan,wheel_zoom,box_zoom,reset")



        # Add Hover Tool for more info
        hover = HoverTool()
        hover.tooltips = [("X", "@x"), ("Y", "@y")]
        p_test_and_ideal.add_tools(hover)
        p_deviations.add_tools(hover)

        # Plot Deviations
        p_deviations.circle('x', 'DeltaY', size=10, color="red", alpha=0.5, source=test_source)

            # Plot Test Data and Ideal Functions
        p_test_and_ideal.circle('x', 'y', size=10, color="navy", alpha=0.5, source=test_source)
        for ideal_col in ideal_function_selection.values():
            p_test_and_ideal.line('x', ideal_col, source=ideal_source, line_width=2)

        

        colors = Category20[20]
        for i, col in enumerate(['y1', 'y2', 'y3', 'y4']):
            p_training_and_ideal.line('x', col, source=training_source, legend_label=f"Training {col}", line_width=2, color=colors[i])
            ideal_col = ideal_function_selection[col]
            p_training_and_ideal.line('x', ideal_col, source=ideal_source, legend_label=f"Ideal {ideal_col}", line_width=2, line_dash='dashed', color=colors[i + 10])

        p_histogram = figure(title="Histogram of Deviations", x_axis_label='Deviation', y_axis_label='Frequency', tools="pan,wheel_zoom,box_zoom,reset")
        hist, edges = np.histogram(test_data_results['DeltaY'], bins=15)
        p_histogram.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color="navy", line_color="white", alpha=0.7)
        grid = gridplot([[p_deviations],[p_test_and_ideal],[p_training_and_ideal],[p_histogram]])
        output_file("output/visualization/data_visualization.html")
        show(grid)
    except Exception as e:
        raise VisualizationError(f"Error in visualization: {e}")
