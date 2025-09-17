from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import pickle
import RecommendationModel  # Import the model with the preprocessed data

# Load pre-trained KMeans model and preprocessor
with open("kmeans_model.pkl", "rb") as model_file:
    kmeans_model = pickle.load(model_file)

with open("preprocessor.pkl", "rb") as preprocessor_file:
    preprocessor = pickle.load(preprocessor_file)

# Load stock data with clusters
data = RecommendationModel.df  # Assuming RecommendationModel.df contains the stock data with clusters

# Initialize FastAPI app
app = FastAPI()

# Define input data model
class StockData(BaseModel):
    user_exp: str
    user_cost: float
    user_plan: str
    user_sector: str

@app.post("/")
def recommend(stock_data: StockData):
    # Convert user input to a DataFrame
    user_data = pd.DataFrame([stock_data.dict()])
    user_data = user_data.rename(columns={
        "user_exp": "Experience",
        "user_cost": "Price",
        "user_plan": "Investment",
        "user_sector": "Sector"
    })

    # Preprocess the input data
    processed_data = preprocessor.transform(user_data)

    # Predict the cluster for the user input
    cluster_label = kmeans_model.predict(processed_data)[0]

    # Filter the stock data based on cluster and user input criteria
    filtered_stocks = data[data['Cluster'] == cluster_label]

    # Filter the stocks based on the user's criteria
    filtered_stocks = filtered_stocks[
        (filtered_stocks['Experience'] == stock_data.user_exp)&
        (filtered_stocks['Investment'] == stock_data.user_plan)&
        (filtered_stocks['Price'] <= stock_data.user_cost)&
        (filtered_stocks['Sector'] == stock_data.user_sector)
        ]

    # Check if any stocks match the criteria
    if not filtered_stocks.empty:
        # Prepare the output with the relevant columns
        recommendations = filtered_stocks[['Name', 'Ticker', 'Sector', 'Price']].to_dict(orient='records')
        return {"Recommended Stocks": recommendations}
    else:
        return {"message": "No stocks match your criteria."}

