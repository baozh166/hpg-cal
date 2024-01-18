import pandas as pd
import pickle
from flask import Flask, render_template, request, url_for

app = Flask(__name__)
model = pickle.load(open("models/best_model_xgbr.pkl", "rb"))

@app.route("/", methods=["GET", "POST"])
def index():
    res = ""
    if request.method == "POST":
        features = [0]*12

        search_type = request.form["Search type"]
        if search_type == "blastn":
            features[0] = 1
            features[8] = 1
        elif search_type == "blastp":
            features[1] = 1
            features[7] = 1
        elif search_type == "blastx":
            features[2] = 1
            features[7] = 1
        elif search_type == "tblastn":
            features[3] = 1
            features[8] = 1
        elif search_type == "tblastx":
            features[4] = 1
            features[8] = 1
        elif search_type == "diam_blastp":
            features[5] = 1
            features[7] = 1
        elif search_type == "diam_blastx":
            features[6] = 1
            features[7] = 1

        features[9] = request.form["file_size"]
        features[10] = request.form["cpu"]
        features[11] = request.form["mem"]

        df = pd.DataFrame(features).T
        df.columns = ["search_blastn", "search_blastp", "search_blastx", "search_tblastn", "search_tblastx", "search_diam_blastp", "search_diam_blastx", "db_nr", "db_nt", "file_size", "cpu", "mem"]
        prediction = model.predict(df)
        res = round(float(prediction[0]), 1)
        if res < 0:
            res = 0

    return render_template("index.html", result=res)

@app.route("/health")
def health():
    return "I am healthy"

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)




