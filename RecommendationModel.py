import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
import pickle

def calculate_risk(ticker):
    try:
        # Fetch 1 year of historical data
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")

        # Calculate daily returns
        hist['Daily Return'] = hist['Close'].pct_change()

        # Calculate standard deviation of returns (volatility)
        std_dev = hist['Daily Return'].std()

        # Assess experience needed based on standard deviation
        if std_dev < 0.015:
            return "Beginner"
        elif std_dev < 0.03:
            return "Intermediate"
        else:
            return "Advanced"
    except Exception as e:
        print(f"Error analyzing {ticker}: {e}")
        return "Unknown"

def calculate_investplan(ticker):
    try:
        # Fetch 1 year of historical data
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")
        # Calculate daily returns
        hist['Daily Return'] = hist['Close'].pct_change()

        # Calculate standard deviation of returns (volatility)
        std_dev = hist['Daily Return'].std()

        # Determine investment plan based on volatility
        if std_dev < 0.015:
            return "Long Term"
        else:
            return "Short Term"
    except Exception as e:
        print(f"Error analyzing {ticker}: {e}")
        return "Unknown"

#List of Stock Tickers
tickers = ["IBM", "AAPL","MSFT", "INTC", "CSCO", "TXN", "JPM", "BAC", "WFC", "GS", "MS", "C",
           "JNJ", "PFE", "MRK", "ABBV", "BMY", "MDT", "PG", "KO", "PEP", "UL", "CL", "KMB", "MCD",
           "HD", "LOW", "SBUX", "CVX", "XOM"]

stock_data = []

#Iterate over every ticker to get stock information
for ticker in tickers:
    stock = yf.Ticker(ticker)
    info = stock.info
    stock_data.append({
        "Name": info.get("shortName"),
        "Ticker": ticker,
        "Price": info.get("open"),
        "Experience": calculate_risk(ticker),
        "Investment": calculate_investplan(ticker),
        "Sector": info.get("sector"),
        })

#Convert to pandas dataframe
df = pd.DataFrame(stock_data)

print(df)

#Defines features needed for clustering
features = ["Price", "Experience", "Investment", "Sector"]

# Separate numerical and categorical columns
numerical_features = ["Price"]
categorical_features = ["Experience", "Investment", "Sector"]

# Preprocessor: Encode only categorical columns
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(), categorical_features),  # Encode categorical features
        ("num", StandardScaler(), numerical_features)       # Keep numerical features as
    ]
)

# Transform the features
X = df[features]
X_transformed = preprocessor.fit_transform(X)

#Train the model using Kmeans clustering
kmeans = KMeans(n_clusters=13, random_state=1)
kmeans.fit_predict(X_transformed)

#Get Cluster labels and add to dataframe
labels = kmeans.labels_
df['Cluster'] = labels

# Calculate the silhouette score to evaluate the quality of the clustering
silhouette_avg = silhouette_score(X_transformed, labels)
print(f'Silhouette Score: {silhouette_avg}')


# Save the KMeans model to disk using pickle for future use
with open("kmeans_model.pkl", "wb") as model_file:
    pickle.dump(kmeans, model_file)


# Save the preprocessor to disk using pickle for future use
with open("preprocessor.pkl", "wb") as preprocessor_file:
    pickle.dump(preprocessor,preprocessor_file)

