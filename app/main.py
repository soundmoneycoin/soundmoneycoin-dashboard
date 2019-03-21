from flask import Flask, render_template, request
from ethapi

app = Flask(__name__)

@app.route("/")
def home():

    total = total_sov()
    latest = latest_avg()
    sov24 = gasAndTransactions
    percent = percent_mined()
    minted = sovMinted24Hours
    gasAvg = gasAndTransactions[0]

    return render_template("dashboard.html", total = total, latest=latest, sov24=sov24, percent=percent, minted=minted, gasAvg=gasAvg)

if __name__ == "__main__":
    app.run(debug=True)