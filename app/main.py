import pandas as pd
import pickle
from flask import Flask, render_template, request, url_for

app = Flask(__name__)
model = pickle.load(open("models/model_lr.pkl", "rb"))

@app.route("/", methods=["GET", "POST"])
def index():
    res = ""
    if request.method == "POST":
        features = [0]*7

        search_type = request.form["Search type"]
        if search_type == "blastn":
            features[1] = 1
            features[3] = 1
        elif search_type == "blastp":
            features[0] = 1
            features[2] = 1

        features[4] = request.form["file_size"]
        features[5] = request.form["cpu"]
        features[6] = request.form["mem"]

        df = pd.DataFrame(features).T
        df.columns = ["search_blastp", "search_tblastn", "db_nr", "db_nt", "file_size", "cpu", "mem"]
        prediction = model.predict(df)
        res = int(prediction[0])

    return render_template("index.html", result=res)

@app.route("/health")
def health():
    return "I am healthy"

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)




