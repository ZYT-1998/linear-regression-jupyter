#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path

import matplotlib

# Use a non-interactive backend when running from the terminal.
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


OUTPUT_FILENAME = "linear_regression_python_output.png"


def parse_arguments() -> argparse.Namespace:
    """Read command-line arguments."""

    parser = argparse.ArgumentParser(
        description=(
            "Fit a simple linear regression model "
            "and save a regression plot."
        )
    )

    parser.add_argument(
        "filename",
        help="Path to the input CSV file."
    )

    parser.add_argument(
        "x_column",
        help="Name of the predictor column."
    )

    parser.add_argument(
        "y_column",
        help="Name of the response column."
    )

    return parser.parse_args()


def load_and_prepare_data(
    filename: str,
    x_column: str,
    y_column: str
) -> pd.DataFrame:
    """Load the CSV file and validate the requested columns."""

    file_path = Path(filename)

    if not file_path.is_file():
        raise FileNotFoundError(
            f"Input file not found: {filename}"
        )

    data = pd.read_csv(file_path)

    missing_columns = [
        column
        for column in (x_column, y_column)
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing column(s): "
            + ", ".join(missing_columns)
            + ". Available columns: "
            + ", ".join(data.columns.astype(str))
        )

    clean_data = data[
        [x_column, y_column]
    ].copy()

    clean_data[x_column] = pd.to_numeric(
        clean_data[x_column],
        errors="coerce"
    )

    clean_data[y_column] = pd.to_numeric(
        clean_data[y_column],
        errors="coerce"
    )

    clean_data = clean_data.dropna()

    if len(clean_data) < 2:
        raise ValueError(
            "At least two complete numeric observations are required."
        )

    return clean_data


def run_regression(
    data: pd.DataFrame,
    x_column: str,
    y_column: str
) -> None:
    """Fit the model, report metrics, and save the plot."""

    X = data[[x_column]]
    y = data[y_column]

    model = LinearRegression()
    model.fit(X, y)

    predictions = model.predict(X)

    r_squared = model.score(X, y)

    rmse = np.sqrt(
        mean_squared_error(y, predictions)
    )

    plot_data = data.copy()
    plot_data["PredictedValue"] = predictions
    plot_data = plot_data.sort_values(x_column)

    plt.figure(figsize=(8, 5))

    plt.scatter(
        data[x_column],
        data[y_column],
        alpha=0.75,
        label="Observed data"
    )

    plt.plot(
        plot_data[x_column],
        plot_data["PredictedValue"],
        linewidth=2,
        label="Regression line"
    )

    plt.title(f"{y_column} vs {x_column}")
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.legend()
    plt.grid(alpha=0.25)
    plt.tight_layout()

    plt.savefig(
        OUTPUT_FILENAME,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("Python linear regression completed.")
    print(f"Observations used: {len(data)}")
    print(f"Intercept: {model.intercept_:.4f}")
    print(f"Slope: {model.coef_[0]:.4f}")
    print(f"R-squared: {r_squared:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"Plot saved as: {OUTPUT_FILENAME}")


def main() -> int:
    """Main program entry point."""

    args = parse_arguments()

    try:
        data = load_and_prepare_data(
            args.filename,
            args.x_column,
            args.y_column
        )

        run_regression(
            data,
            args.x_column,
            args.y_column
        )

    except (
        FileNotFoundError,
        ValueError,
        pd.errors.ParserError
    ) as error:
        print(
            f"Error: {error}",
            file=sys.stderr
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())