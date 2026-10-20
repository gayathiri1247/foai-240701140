import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
import secrets
from backend.database import init_db, get_db
from backend.loan_rules import LOANS, RULES
from backend.inference_engine import evaluate_application
from backend.calculations import calculate_emi

app = Flask(__name__, template_folder="frontend", static_folder="frontend/static")
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "change-this-demo-secret-before-deployment")

def login_required(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            if request.path.startswith("/api/"):
                return jsonify({"error": "Please log in first."}), 401
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapped

@app.before_request
def startup():
    init_db()

@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", user=session.get("name", "User"), loans=LOANS)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not name or len(name) > 80 or "@" not in email or len(password) < 8:
            flash("Enter a name, valid email, and password with at least 8 characters.", "danger")
            return render_template("register.html")
        with get_db() as db:
            try:
                cur = db.execute("INSERT INTO users(name,email,password_hash,created_at) VALUES(?,?,?,?)",
                                 (name, email, generate_password_hash(password), datetime.now().isoformat(timespec="seconds")))
                session.clear()
                session["user_id"] = cur.lastrowid
                session["name"] = name
                return redirect(url_for("home"))
            except Exception:
                flash("That email may already be registered. Please log in or use another email.", "danger")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        with get_db() as db:
            user = db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["id"]
            session["name"] = user["name"]
            return redirect(url_for("home"))
        flash("Email or password is incorrect.", "danger")
    return render_template("login.html")

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/apply/<loan_type>")
@login_required
def apply(loan_type):
    loan = LOANS.get(loan_type)
    if not loan:
        return redirect(url_for("home"))
    return render_template("application.html", loan=loan, loan_type=loan_type)

@app.route("/result/<reference_id>")
@login_required
def result(reference_id):
    with get_db() as db:
        row = db.execute("SELECT * FROM applications WHERE reference_id=? AND user_id=?",
                         (reference_id, session["user_id"])).fetchone()
        if not row:
            flash("Application was not found.", "warning")
            return redirect(url_for("history"))
        rule_rows = db.execute("SELECT * FROM rule_results WHERE application_id=? ORDER BY id",
                               (row["id"],)).fetchall()
    import json
    application = dict(row)
    application["applicant_data"] = json.loads(application.pop("applicant_data_json"))
    application["rule_results"] = [dict(r) for r in rule_rows]
    return render_template("result.html", application=application, loans=LOANS)

@app.route("/history")
@login_required
def history():
    with get_db() as db:
        rows = db.execute("""SELECT reference_id, loan_type, submitted_at, decision, explanation_summary
                             FROM applications WHERE user_id=? ORDER BY id DESC""",
                          (session["user_id"],)).fetchall()
    return render_template("history.html", rows=rows, loans=LOANS)

@app.route("/rules")
@login_required
def rules_page():
    return render_template("rules.html", rules=RULES, loans=LOANS)

@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "message": "SBI pre-screening demo backend is running."})

@app.route("/api/evaluate", methods=["POST"])
@login_required
def api_evaluate():
    payload = request.get_json(silent=True) or {}
    loan_type = payload.get("loan_type", "")
    if loan_type not in LOANS:
        return jsonify({"error": "Please select a supported loan type."}), 400
    decision_data = evaluate_application(loan_type, payload)
    reference_id = "SBI-DEMO-" + secrets.token_hex(4).upper()
    submitted_at = datetime.now().isoformat(timespec="seconds")
    emi = None
    try:
        principal = float(payload.get("requested_amount", 0))
        rate = float(payload.get("demo_annual_interest_rate", 0))
        tenure = int(payload.get("tenure_months", 0))
        if principal > 0 and tenure > 0 and rate >= 0:
            emi = round(calculate_emi(principal, rate, tenure), 2)
    except (ValueError, TypeError, ZeroDivisionError):
        emi = None
    summary = decision_data["summary"]
    import json
    with get_db() as db:
        cur = db.execute("""INSERT INTO applications
            (reference_id,user_id,loan_type,submitted_at,applicant_data_json,decision,explanation_summary,emi)
            VALUES(?,?,?,?,?,?,?,?)""",
            (reference_id, session["user_id"], loan_type, submitted_at,
             json.dumps(payload, ensure_ascii=False), decision_data["decision"], summary, emi))
        app_id = cur.lastrowid
        for rr in decision_data["rule_results"]:
            db.execute("""INSERT INTO rule_results(application_id,rule_id,status,explanation,verification_status,source_url)
                          VALUES(?,?,?,?,?,?)""",
                       (app_id, rr["rule_id"], rr["status"], rr["explanation"],
                        rr["verification_status"], rr["source_url"]))
    return jsonify({"reference_id": reference_id, "redirect_url": url_for("result", reference_id=reference_id)})

@app.route("/api/applications")
@login_required
def api_applications():
    with get_db() as db:
        rows = db.execute("SELECT reference_id,loan_type,submitted_at,decision FROM applications WHERE user_id=? ORDER BY id DESC",
                          (session["user_id"],)).fetchall()
    return jsonify([dict(r) for r in rows])

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
