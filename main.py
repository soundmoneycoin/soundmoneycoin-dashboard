from flask import Flask, render_template, request, jsonify
from backend.ethapi import init_sov_24_hours,update_sov_24_hours,total_sov,percent_mined,latest_avg,gasAndNoOfTransactions,get_number_of_holders
from decimal import Decimal


app = Flask(__name__)    

def getValues():
    total = total_sov()
    latest = latest_avg()
    holders = get_number_of_holders()

    uPercent = Decimal(percent_mined()) * Decimal(100)
    percent = round(uPercent, 2)

    x = gasAndNoOfTransactions(init_sov_24_hours())
    gasAvg = x[0]
    noOfTransactions = x[1]
    sovMined = x[2]

    valueList = [total, latest, percent, gasAvg, noOfTransactions, sovMined, holders]
    return valueList
    

@app.route("/")
def home():
    values = getValues()
    
    return render_template("dashboard.html", total = values[0], latest=values[1], 
            percent=values[2],gasAvg=values[3], noOfTransactions = values[4], sovMined=values[5],
            holders = values[6])

@app.route('/update', methods=['POST'])
def update_values():
    func = getValues()
    
    return jsonify(
        {"total" : func[0],
        "latest" : func[1],
        "percent":func[2],
        "gasAvg":func[3],
        "noOfTransactions":func[4],
        "sovMined" : func[5]
        }
    )

if __name__ == "__main__":
    app.run(debug=True)

