from flask import Flask, request, jsonify
import pyodbc
from datetime import datetime, timedelta

app = Flask(__name__)

# Database connection setup using pyodbc
cnxn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=Angel\MSSQLSERVER04;DATABASE=loans;')
cursor = cnxn.cursor()

def execute_query(query, params=None):
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        cnxn.commit()
    except pyodbc.Error as ex:
        return jsonify({"error": str(ex)}), 500

# Customer Routes
@app.route("/customer/create_loan", methods=["POST"])
def create_loan():
    try:
        data = request.json
        customer_id = data["customer_id"]
        amount = data["amount"]
        term = data["term"]

        # Sample validation
        if amount <= 0 or term <= 0:
            return jsonify({"error": "Invalid loan parameters"}), 400

        # Create the loan
        execute_query("INSERT INTO Loan (customer_id, amount, term, status) VALUES (?, ?, ?, ?)",
                      (customer_id, amount, term, "PENDING"))

        # Get the loan_id for the newly created loan
        # Retrieve the last row from the 'loan' table
        cursor.execute("SELECT TOP 1 loan_id FROM Loan ORDER BY loan_id DESC")
        result = cursor.fetchone()
        loan_id = result.loan_id
        

# Assuming 'last_row' is a tuple representing the last row from the 'Loan' table


        # Insert repayment records
        current_date = datetime.now().date()
        arr=[]
        due_dates = [current_date + timedelta(days=(7 * i)) for i in range(1, term + 1)]
        for due_date in due_dates:
            query = f"INSERT INTO Repay (loan_id, amount, due_date, status) VALUES ({loan_id}, {round(amount / term, 2)}, '{due_date}', 'PENDING')"
            cursor.execute(query)
            cnxn.commit()
        return jsonify({"Successfull":"Loan created"})
            
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500


@app.route("/customer/view_loans/<int:customer_id>", methods=["GET"])
def view_loans(customer_id):
    try:
    
        cursor.execute("SELECT * FROM Loan WHERE customer_id = ?", (customer_id,))
        loans = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]

        return jsonify({"loans": loans})
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

# Admin Routes
@app.route("/admin/approve_loan/<int:loan_id>", methods=["PUT"])
def approve_loan(loan_id):
    execute_query("UPDATE Loan SET status = 'APPROVED' WHERE loan_id = ?", (loan_id,))

    return jsonify({"message": "Loan approved successfully"}), 200


# Repayment Routes
@app.route("/customer/add_repayment/<int:loan_id>", methods=["POST"])
def add_repayment(loan_id):
    try:
        data = request.json
        amount_paid = data["amount_paid"]

        # Sample validation
        if amount_paid <= 0:
            return jsonify({"error": "Invalid repayment amount"}), 400

        # Add the repayment and update status
        execute_query("UPDATE Repay SET status = 'PAID' WHERE loan_id = ? AND amount = ?", (loan_id, amount_paid))

        return jsonify({"message": "Repayment added successfully"}), 201
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500
