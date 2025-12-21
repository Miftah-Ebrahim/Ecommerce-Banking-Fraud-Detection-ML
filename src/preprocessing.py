import pandas as pd
from .feature_engineering import preprocess_features


def load_data(fraud_path, ip_path):
    """Load the fraud and IP datasets."""
    fraud_df = pd.read_csv(fraud_path)
    ip_df = pd.read_csv(ip_path)
    return fraud_df, ip_df


def fix_data_types(fraud_df, ip_df):
    """Fix IP addresses to integers and convert dates to datetime."""
    # Fix IPs
    fraud_df["ip_address"] = fraud_df["ip_address"].astype(int)
    ip_df["lower_bound_ip_address"] = ip_df["lower_bound_ip_address"].astype(int)
    ip_df["upper_bound_ip_address"] = ip_df["upper_bound_ip_address"].astype(int)

    # Fix dates
    fraud_df["signup_time"] = pd.to_datetime(fraud_df["signup_time"])
    fraud_df["purchase_time"] = pd.to_datetime(fraud_df["purchase_time"])

    return fraud_df, ip_df


def merge_geolocation(fraud_df, ip_df):
    """Merge fraud data with IP-to-country mapping using merge_asof."""
    # Sort for merge_asof
    fraud_df = fraud_df.sort_values("ip_address")
    ip_df = ip_df.sort_values("lower_bound_ip_address")

    # Perform merge
    merged_df = pd.merge_asof(
        fraud_df,
        ip_df,
        left_on="ip_address",
        right_on="lower_bound_ip_address",
        direction="backward",
    )

    # Validate: ensure IP <= upper_bound
    merged_df = merged_df[
        merged_df["ip_address"] <= merged_df["upper_bound_ip_address"]
    ]

    return merged_df


def clean_data(merged_df):
    """Handle missing values and duplicates."""
    # Fill missing countries
    merged_df["country"] = merged_df["country"].fillna("Unknown")

    # Remove duplicates
    merged_df = merged_df.drop_duplicates()

    return merged_df


def add_features(merged_df):
    """Add engineered features: time_since_signup, hour_of_day, day_of_week."""
    merged_df["time_since_signup"] = (
        merged_df["purchase_time"] - merged_df["signup_time"]
    ).dt.total_seconds()
    merged_df["hour_of_day"] = merged_df["purchase_time"].dt.hour
    merged_df["day_of_week"] = merged_df["purchase_time"].dt.dayofweek
    return merged_df


def preprocess_data(fraud_path, ip_path, creditcard_path=None):
    """Complete preprocessing pipeline, now including creditcard if provided."""
    fraud_df, ip_df = load_data(fraud_path, ip_path)
    fraud_df, ip_df = fix_data_types(fraud_df, ip_df)
    merged_df = merge_geolocation(fraud_df, ip_df)
    merged_df = clean_data(merged_df)
    merged_df = add_features(merged_df)

    if creditcard_path:
        creditcard_df = pd.read_csv(creditcard_path)
        creditcard_df = creditcard_df.drop_duplicates()
        merged_df, creditcard_df = preprocess_features(merged_df, creditcard_df)
        return merged_df, creditcard_df
    else:
        # For fraud only, no need to call preprocess_features
        return merged_df
