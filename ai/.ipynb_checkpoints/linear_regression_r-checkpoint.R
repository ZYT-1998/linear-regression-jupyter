#!/usr/bin/env Rscript

output_filename <- "linear_regression_r_output.png"

args <- commandArgs(trailingOnly = TRUE)

if (length(args) != 3) {
  cat(
    paste0(
      "Usage: Rscript linear_regression_r.R ",
      "<filename> <x_column> <y_column>\n"
    ),
    file = stderr()
  )

  quit(status = 1)
}

filename <- args[1]
x_column <- args[2]
y_column <- args[3]

if (!file.exists(filename)) {
  cat(
    paste(
      "Error: Input file not found:",
      filename,
      "\n"
    ),
    file = stderr()
  )

  quit(status = 1)
}

data <- tryCatch(
  read.csv(
    filename,
    check.names = FALSE
  ),
  error = function(error) {
    cat(
      paste(
        "Error reading CSV file:",
        error$message,
        "\n"
      ),
      file = stderr()
    )

    quit(status = 1)
  }
)

missing_columns <- setdiff(
  c(x_column, y_column),
  names(data)
)

if (length(missing_columns) > 0) {
  cat(
    paste(
      "Error: Missing column(s):",
      paste(missing_columns, collapse = ", "),
      "\n"
    ),
    file = stderr()
  )

  cat(
    paste(
      "Available columns:",
      paste(names(data), collapse = ", "),
      "\n"
    ),
    file = stderr()
  )

  quit(status = 1)
}

x_values <- suppressWarnings(
  as.numeric(data[[x_column]])
)

y_values <- suppressWarnings(
  as.numeric(data[[y_column]])
)

valid_rows <- complete.cases(
  x_values,
  y_values
)

regression_data <- data.frame(
  x = x_values[valid_rows],
  y = y_values[valid_rows]
)

if (nrow(regression_data) < 2) {
  cat(
    paste(
      "Error: At least two complete numeric",
      "observations are required.\n"
    ),
    file = stderr()
  )

  quit(status = 1)
}

model <- lm(
  y ~ x,
  data = regression_data
)

model_summary <- summary(model)

r_squared <- model_summary$r.squared

rmse <- sqrt(
  mean(residuals(model)^2)
)

png(
  filename = output_filename,
  width = 1200,
  height = 750,
  res = 150
)

plot(
  regression_data$x,
  regression_data$y,
  pch = 19,
  main = paste(y_column, "vs", x_column),
  xlab = x_column,
  ylab = y_column
)

abline(
  model,
  lwd = 3
)

grid()

legend(
  "topleft",
  legend = c(
    "Observed data",
    "Regression line"
  ),
  pch = c(19, NA),
  lty = c(NA, 1),
  lwd = c(NA, 3),
  bty = "n"
)

dev.off()

cat("R linear regression completed.\n")

cat(
  "Observations used:",
  nrow(regression_data),
  "\n"
)

cat(
  "Intercept:",
  coef(model)[1],
  "\n"
)

cat(
  "Slope:",
  coef(model)[2],
  "\n"
)

cat(
  "R-squared:",
  r_squared,
  "\n"
)

cat(
  "RMSE:",
  rmse,
  "\n"
)

cat(
  "Plot saved as:",
  output_filename,
  "\n"
)