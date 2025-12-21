import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder


def encode_categorical(df):
    """One-hot encode categorical features: source, browser, sex."""
    categorical_cols = ["source", "browser", "sex"]
    encoder = OneHotEncoder(drop="first", sparse_output=False)
    encoded = encoder.fit_transform(df[categorical_cols])
    encoded_df = pd.DataFrame(
        encoded, columns=encoder.get_feature_names_out(categorical_cols)
    )
    df = df.drop(categorical_cols, axis=1)
    df = pd.concat([df, encoded_df], axis=1)
    return df


def scale_features(df, features_to_scale):
    """Apply StandardScaler to specified features."""
    scaler = StandardScaler()
    df[features_to_scale] = scaler.fit_transform(df[features_to_scale])
    return df


def preprocess_features(fraud_df, creditcard_df):
    """Full feature engineering pipeline."""
    # Encode Fraud_Data
    fraud_df = encode_categorical(fraud_df)
    fraud_df = scale_features(fraud_df, ["purchase_value", "time_since_signup", "age"])

    # Scale Creditcard_Data
    creditcard_df = scale_features(creditcard_df, ["Amount"])

    return fraud_df, creditcard_df
