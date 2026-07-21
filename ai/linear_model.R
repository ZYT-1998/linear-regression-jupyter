args <- commandArgs(trailingOnly = TRUE)

if (length(args) != 3) {
  stop(
    paste(
      "Usage: Rscript linear_model.R",
      "<filename> <x_column> <y_column>"
    )
  )
}

filename <- args[1]
x_column <- args[2]
y_column <- args[3]

# Read the dataset
dataset <- read.csv(filename)

# Check that the requested columns exist
missing_columns <- setdiff(
  c(x_column, y_column),
  names(dataset)
)

if (length(missing_columns) > 0) {
  stop(
    paste(
      "Missing column(s):",
      paste(missing_columns, collapse = ", ")
    )
  )
}

# Create a simple data frame using x and y
df <- data.frame(
  x = dataset[[x_column]],
  y = dataset[[y_column]]
)

df <- na.omit(df)

# Fit the linear regression model
model <- lm(y ~ x, data = df)

slope <- coef(model)[2]
intercept <- coef(model)[1]
r <- cor(df$x, df$y)

predicted <- predict(model)
mse <- mean((df$y - predicted)^2)

# Print the required statistics
cat("Linear Regression Results\n")
cat("-------------------------\n")
cat("Slope:", round(slope, 4), "\n")
cat("Intercept:", round(intercept, 4), "\n")
cat("Pearson correlation coefficient (r):", round(r, 4), "\n")
cat("Mean Squared Error (MSE):", round(mse, 4), "\n")

library(ggplot2)

annotation_text <- paste0(
  "y = ",
  round(slope, 2),
  "x + ",
  round(intercept, 2),
  "\nr = ",
  round(r, 2),
  "\nMSE = ",
  round(mse, 2)
)

regression_plot <- ggplot(df, aes(x = x, y = y)) +
  geom_point() +
  geom_smooth(method = "lm", se = FALSE) +
  annotate(
    "text",
    x = min(df$x),
    y = max(df$y),
    label = annotation_text,
    hjust = 0,
    vjust = 1
  ) +
  labs(
    title = paste(y_column, "vs.", x_column),
    x = x_column,
    y = y_column
  ) +
  theme_minimal()

# Use the exact filename required by the instructor
ggsave(
  "regression_plot_r.png",
  plot = regression_plot,
  width = 8,
  height = 6,
  dpi = 300
)

cat("Plot saved as regression_plot_r.png\n")