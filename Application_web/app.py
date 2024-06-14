from flask import Flask, render_template, jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["twitter_sentiment_db"]
collection = db["predictions"]

# Mapping function for predictions
def map_prediction(prediction):
    mapping = {
        0: "Negative",
        1: "Positive",
        2: "Neutral",
        3: "Irrelevant"
    }
    return mapping.get(prediction, "Unknown")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/predictions')
def get_predictions():
    predictions = list(collection.find({}, {"_id": 0}))
    for prediction in predictions:
        prediction["prediction"] = map_prediction(prediction["prediction"])
    return jsonify(predictions)

@app.route('/chart-data')
def get_chart_data():
    pipeline = [
        {"$group": {"_id": "$prediction", "count": {"$sum": 1}}}
    ]
    results = list(collection.aggregate(pipeline))
    sentiment_data = {map_prediction(item["_id"]): item["count"] for item in results}

    chart_data = {
        "labels": list(sentiment_data.keys()),
        "data": list(sentiment_data.values())
    }
    return jsonify(chart_data)

if __name__ == '__main__':
    app.run(debug=True)
