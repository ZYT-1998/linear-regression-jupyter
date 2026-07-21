import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import linregress
from sklearn.metrics import mean_squared_error


def main():
    if len(sys.argv) != 4:
        print(
            "Usage: python linear_model.py "
            "<filename> <x_column> <y_column>"
        )
        sys.exit(1)

    filename = sys.argv[1]
    x_column = sys.argv[2]
    y_column = sys.argv[3]

    # Read the dataset
    dataset = pd.read_csv(filename)

    # Check that the requested columns exist
    if x_column not in dataset.columns or y_column not in dataset.columns:
        print("Error: one or both column names were not found.")
        print("Available columns:", list(dataset.columns))
        sys.exit(1)

    # Keep only the selected columns and remove missing values
    analysis_data = dataset[[x_column, y_column]].dropna()

    x = analysis_data[x_column].to_numpy()
    y = analysis_data[y_column].to_numpy()

    # Fit the linear regression model
    slope, intercept, r_value, p_value, std_error = linregress(x, y)

    # Calculate predicted values and MSE
    y_pred = slope * x + intercept
    mse = mean_squared_error(y, y_pred)

    # Print the required statistics
    print("Linear Regression Results")
    print("-------------------------")
    print(f"Slope: {slope:.4f}")
    print(f"Intercept: {intercept:.4f}")
    print(f"Pearson correlation coefficient (r): {r_value:.4f}")
    print(f"Mean Squared Error (MSE): {mse:.4f}")

    # Sort values so the fitted line is drawn correctly
    order = np.argsort(x)

    # Create the enhanced regression plot
    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, label="Observed data")
    plt.plot(x[order], y_pred[order], label="Fitted line")

    annotation = (
        f"y = {slope:.2f}x + {intercept:.2f}\n"
        f"r = {r_value:.2f}\n"
        f"MSE = {mse:.2f}"
    )

    plt.text(
        0.05,
        0.95,
        annotation,
        transform=plt.gca().transAxes,
        verticalalignment="top",
        bbox={"boxstyle": "round", "alpha": 0.8},
    )

    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f"{y_column} vs. {x_column}")
    plt.legend()
    plt.tight_layout()

    # Use the exact filename required by the instructor
    plt.savefig("regression_plot_python.png", dpi=300)
    plt.close()

    print("Plot saved as regression_plot_python.png")


if __name__ == "__main__":
    main()