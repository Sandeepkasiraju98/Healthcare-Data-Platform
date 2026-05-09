# ============================================================
# Healthcare Data Platform - R Statistical Analysis
# ============================================================

# Install packages if needed
# install.packages(c("tidyverse", "ggplot2", "reticulate", "jsonlite"))

library(tidyverse)
library(ggplot2)
library(jsonlite)

# ─────────────────────────────────────────────
# 1. Load Data
# ─────────────────────────────────────────────
df <- read.csv("healthcare_dataset.csv", stringsAsFactors = FALSE)

# Clean names
df$Name <- tools::toTitleCase(tolower(df$Name))

# Parse dates
df$Date.of.Admission <- as.Date(df$Date.of.Admission)
df$Discharge.Date    <- as.Date(df$Discharge.Date)
df$Length.of.Stay    <- as.numeric(df$Discharge.Date - df$Date.of.Admission)

cat("Dataset loaded:", nrow(df), "records\n")

# ─────────────────────────────────────────────
# 2. Descriptive Statistics
# ─────────────────────────────────────────────
cat("\n=== Billing Amount Summary ===\n")
print(summary(df$Billing.Amount))

cat("\n=== Length of Stay Summary ===\n")
print(summary(df$Length.of.Stay))

cat("\n=== Patients by Medical Condition ===\n")
print(table(df$Medical.Condition))

cat("\n=== Admission Type Breakdown ===\n")
print(table(df$Admission.Type))

# ─────────────────────────────────────────────
# 3. Hypothesis Test: Billing by Admission Type
# ─────────────────────────────────────────────
cat("\n=== ANOVA: Billing Amount ~ Admission Type ===\n")
anova_result <- aov(Billing.Amount ~ Admission.Type, data = df)
print(summary(anova_result))

# ─────────────────────────────────────────────
# 4. Correlation: Age vs Billing Amount
# ─────────────────────────────────────────────
cat("\n=== Pearson Correlation: Age vs Billing Amount ===\n")
cor_result <- cor.test(df$Age, df$Billing.Amount, method = "pearson")
print(cor_result)

# ─────────────────────────────────────────────
# 5. Chi-Square: Medical Condition vs Test Results
# ─────────────────────────────────────────────
cat("\n=== Chi-Square: Medical Condition vs Test Results ===\n")
chi_result <- chisq.test(table(df$Medical.Condition, df$Test.Results))
print(chi_result)

# ─────────────────────────────────────────────
# 6. Visualizations
# ─────────────────────────────────────────────

# Billing by condition
p1 <- ggplot(df, aes(x = Medical.Condition, y = Billing.Amount, fill = Medical.Condition)) +
  geom_boxplot() +
  labs(title = "Billing Amount by Medical Condition",
       x = "Condition", y = "Billing Amount ($)") +
  theme_minimal() +
  theme(legend.position = "none")
ggsave("billing_by_condition.png", p1, width = 10, height = 6)

# Length of stay by admission type
p2 <- ggplot(df, aes(x = Admission.Type, y = Length.of.Stay, fill = Admission.Type)) +
  geom_violin() +
  labs(title = "Length of Stay by Admission Type",
       x = "Admission Type", y = "Days") +
  theme_minimal() +
  theme(legend.position = "none")
ggsave("stay_by_admission.png", p2, width = 8, height = 6)

# Age distribution by gender
p3 <- ggplot(df, aes(x = Age, fill = Gender)) +
  geom_histogram(binwidth = 5, alpha = 0.6, position = "identity") +
  labs(title = "Age Distribution by Gender", x = "Age", y = "Count") +
  theme_minimal()
ggsave("age_distribution.png", p3, width = 8, height = 6)

cat("\n[R] Statistical analysis complete. Charts saved.\n")

# ─────────────────────────────────────────────
# 7. Export Summary for Python/Power BI
# ─────────────────────────────────────────────
summary_data <- df %>%
  group_by(Medical.Condition) %>%
  summarise(
    Count       = n(),
    Avg_Billing = round(mean(Billing.Amount), 2),
    Avg_Stay    = round(mean(Length.of.Stay), 2),
    .groups     = "drop"
  )

write_json(summary_data, "r_summary_output.json")
cat("[R] Summary exported to r_summary_output.json\n")
