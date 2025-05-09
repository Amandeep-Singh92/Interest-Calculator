from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    interest = None
    total_amount = None

    if request.method == "POST":
        amount = float(request.form["amount"])
        rate = float(request.form["rate"])              # Monthly rate per ₹100
        months = int(request.form["months"])
        days = int(request.form["days"])
        interest_type = request.form["interest_type"]

        time_in_months = months + (days / 30)
        monthly_rate = rate / 100

        if interest_type == "simple":
            interest = amount * monthly_rate * time_in_months
            total_amount = amount + interest

        elif interest_type == "compound":
            total_amount = amount * ((1 + monthly_rate) ** time_in_months)
            interest = total_amount - amount

        elif interest_type == "hybrid":
            current_principal = amount
            interest = 0
            remaining_months = time_in_months

            while remaining_months > 0:
                period = min(6, remaining_months)
                simple_interest = current_principal * monthly_rate * period
                interest += simple_interest
                current_principal += simple_interest
                remaining_months -= period

            total_amount = current_principal

    return render_template("index.html", interest=interest, total_amount=total_amount)

if __name__ == "__main__":
    app.run(debug=True)
