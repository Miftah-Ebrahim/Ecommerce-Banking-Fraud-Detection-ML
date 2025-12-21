# Ecommerce Banking Fraud Detection ML Project

## Project Overview
This project aims to develop a machine learning model to detect fraudulent transactions in an ecommerce banking system. The dataset includes user transaction data with features such as signup and purchase times, IP addresses, and geolocation information. Task 1 focuses on data preprocessing, feature engineering, and exploratory data analysis (EDA) to prepare the data for modeling.

## Data Cleaning & Preprocessing
- Loaded raw fraud data and IP-to-country mapping datasets.
- Converted IP addresses from float to integer for accurate matching.
- Converted signup_time and purchase_time to datetime objects for time-based analysis.
- Performed geolocation merge using `pd.merge_asof` to map user IPs to countries, with backward direction to find the closest lower bound.
- Validated merges by ensuring IP addresses fall within the upper and lower bounds.
- Filled missing country values with "Unknown".
- Removed duplicate rows to ensure data integrity.

## Feature Engineering
We created three key features to capture temporal patterns in user behavior:
- `time_since_signup`: The time difference in seconds between purchase and signup, calculated as `(purchase_time - signup_time).dt.total_seconds()`. This helps identify suspicious rapid transactions after account creation.
- `hour_of_day`: The hour of the purchase (0-23), extracted from `purchase_time.dt.hour`. This captures daily patterns in fraudulent activity.
- `day_of_week`: The day of the week (0=Monday, 6=Sunday), extracted from `purchase_time.dt.dayofweek`. This reveals weekly trends in fraud.

## Key EDA Insights
- **Class Distribution**: The dataset shows a significant class imbalance, with a majority of non-fraudulent transactions (class 0) and a minority of fraudulent ones (class 1).
- **Fraud by Country**: The top countries with the highest fraud cases include [list based on data, e.g., United States, China, etc.]. This suggests geographic patterns in fraudulent behavior.
- **Time Analysis**: Fraudulent transactions tend to occur shortly after signup, as evidenced by the histogram of `time_since_signup` showing higher fraud rates for smaller time differences. This indicates that fraudsters may create accounts and immediately attempt purchases.

## Class Imbalance Strategy
The dataset exhibits a clear class imbalance, with fraudulent transactions being underrepresented. In Task 2, we will address this by applying Synthetic Minority Oversampling Technique (SMOTE) to generate synthetic samples for the minority class, or alternatively use undersampling of the majority class. This will ensure the model can learn effectively from both classes without bias towards the majority.