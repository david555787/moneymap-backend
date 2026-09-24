"""
MoneyMap - Simple Expense Tracker Backend
-------------------------------------------
A minimal Flask API that stores expenses in memory (a Python list).
No database is used - data resets every time the server restarts.

Endpoints:
    GET    /                  -> serves the frontend page
    POST   /add_expense       -> add a new expense
    GET    /expenses          -> list all expenses
    DELETE /expense/<id>      -> delete an expense by id
    GET    /summary           -> total spending grouped by category
"""

from flask import Flask, render_template, request, jsonify
import itertools

app = Flask(__name__)

# -----------------------------------------------------------------
# In-memory "database"
# -----------------------------------------------------------------
# Each expense looks like:
# { "id": 1, "amount": 12.5, "category": "Food", "note": "Lunch", "date": "2026-09-20" }
expenses = []

# A simple counter to generate unique IDs (itertools.count gives 1, 2, 3, ...)
id_counter = itertools.count(1)


# -----------------------------------------------------------------
# Frontend route
# -----------------------------------------------------------------
@app.route("/")
def index():
    """Serve the main HTML page."""
    return render_template("index.html")


# -----------------------------------------------------------------
# API: Add a new expense
# -----------------------------------------------------------------
@app.route("/add_expense", methods=["POST"])
def add_expense():
    """
    Expects JSON body:
        { "amount": 12.5, "category": "Food", "note": "Lunch", "date": "2026-09-20" }
    Returns the newly created expense (with its assigned id).
    """
    data = request.get_json(silent=True) or {}

    amount = data.get("amount")
    category = data.get("category")
    note = data.get("note", "")
    date = data.get("date")

    # --- Basic validation ---
    if amount is None or category is None or date is None:
        return jsonify({"error": "amount, category, and date are required"}), 400

    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return jsonify({"error": "amount must be a number"}), 400

    new_expense = {
        "id": next(id_counter),
        "amount": amount,
        "category": category,
        "note": note,
        "date": date,
    }
    expenses.append(new_expense)

    return jsonify(new_expense), 201


# -----------------------------------------------------------------
# API: Get all expenses
# -----------------------------------------------------------------
@app.route("/expenses", methods=["GET"])
def get_expenses():
    """Return all expenses, most recently added first."""
    return jsonify(list(reversed(expenses)))


# -----------------------------------------------------------------
# API: Delete an expense by id
# -----------------------------------------------------------------
@app.route("/expense/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    """Remove the expense with the given id, if it exists."""
    global expenses
    before_count = len(expenses)
    expenses = [e for e in expenses if e["id"] != expense_id]

    if len(expenses) == before_count:
        return jsonify({"error": f"No expense found with id {expense_id}"}), 404

    return jsonify({"message": f"Expense {expense_id} deleted"}), 200


# -----------------------------------------------------------------
# API: Summary of spending grouped by category
# -----------------------------------------------------------------
@app.route("/summary", methods=["GET"])
def get_summary():
    """Return total spending per category, e.g. { "Food": 45.5, "Transport": 12.0 }"""
    totals = {}
    for e in expenses:
        totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]

    # Round totals to 2 decimal places for clean display
    totals = {category: round(total, 2) for category, total in totals.items()}

    return jsonify(totals)


if __name__ == "__main__":
    # debug=True gives auto-reload + helpful error pages during development
    app.run(debug=True)
