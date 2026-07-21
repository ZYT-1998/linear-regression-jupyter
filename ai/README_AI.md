# AI-Assisted Linear Regression Analysis

This folder contains AI-assisted Python and R analyses of the relationship between years of experience and salary.

## Analysis

YearsExperience is used as the predictor variable, and Salary is used as the response variable. Both versions calculate:

- Slope
- Intercept
- Pearson correlation coefficient
- Mean Squared Error
- Fitted regression equation

Each version also creates an annotated regression plot.

## Files

- linear_model_python.ipynb: Python notebook
- linear_model_r.ipynb: R notebook
- linear_model.py: Python command-line script
- linear_model.R: R command-line script
- regression_data-1.csv: Input dataset
- regression_plot_python.png: Python output plot
- regression_plot_r.png: R output plot
- environment.yml: Environment specification
- setupenv.sh: Environment setup script
- PROMPTS.md: AI prompts used
- CODE_REVIEW.md: AI code review

## Environment Setup

Run:

    bash setupenv.sh
    conda activate linear-regression

## Python Script

Run:

    python linear_model.py regression_data-1.csv YearsExperience Salary

The output plot is saved as regression_plot_python.png.

## R Script

Run:

    Rscript linear_model.R regression_data-1.csv YearsExperience Salary

The output plot is saved as regression_plot_r.png.

## Interpretation

A positive slope indicates that predicted salary increases as years of experience increases. Pearson's correlation coefficient describes the strength and direction of the linear relationship. MSE measures the average squared difference between the observed and predicted salaries.
