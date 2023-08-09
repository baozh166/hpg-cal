import pandas as pd
import pickle
from flask import Flask, render_template, request, url_for

app = Flask(__name__)
model = pickle.load(open("models/model_rfr.pkl", "rb"))

@app.route("/", methods=["GET", "POST"])
def index():
    res = ""
    if request.method == "POST":
        features = [0]*10

        search_type = request.form["Search type"]
        if search_type == "blastn":
            features[0] = 1
            features[6] = 1
        elif search_type == "blastp":
            features[1] = 1
            features[5] = 1
        elif search_type == "blastx":
            features[2] = 1
            features[5] = 1
        elif search_type == "tblastn":
            features[3] = 1
            features[6] = 1
        elif search_type == "tblastx":
            features[4] = 1
            features[6] = 1

        features[7] = request.form["file_size"]
        features[8] = request.form["cpu"]
        features[9] = request.form["mem"]

        df = pd.DataFrame(features).T
        df.columns = ["search_blastn", "search_blastp", "search_blastx", "search_tblastn", "search_tblastx", "db_nr", "db_nt", "file_size", "cpu", "mem"]
        prediction = model.predict(df)
        res = int(prediction[0])
        if res < 0: 
            res = 0

    return render_template("index.html", result=res)

@app.route("/health")
def health():
    return "I am healthy"

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)




