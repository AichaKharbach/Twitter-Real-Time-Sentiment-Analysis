from flask import Flask, render_template, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Connection to MongoDB
client = MongoClient("mongodb://host.docker.internal:27017")
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
def index():
    return render_template('index.html')

@app.route('/predictions')
def get_predictions():
    predictions = list(collection.find({}, {'_id': False}))
    for prediction in predictions:
        prediction["prediction"] = map_prediction(prediction["prediction"])
    return jsonify(predictions)

if __name__ == "__main__":
    app.run(debug=True)
