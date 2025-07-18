from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("funeralhome.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/funeral/<int:funeral_id>/forms/form_info")
def form_info(funeral_id):
    return render_template("forms/form_info.html", funeral_id=funeral_id)

@app.route("/funeral/<int:funeral_id>/forms/form_booking")
def form_booking(funeral_id):
    return render_template("forms/form_booking.html", funeral_id=funeral_id)

@app.route("/funeral/<int:funeral_id>/forms/form_service")
def form_service(funeral_id):
    return render_template("forms/form_service.html", funeral_id=funeral_id)

@app.route("/funeral/<int:funeral_id>/forms/form_papers")
def form_papers(funeral_id):
    return render_template("forms/form_papers.html", funeral_id=funeral_id)

@app.route("/funeral/<int:funeral_id>/forms/form_finances")
def form_finances(funeral_id):
    return render_template("forms/form_finances.html", funeral_id=funeral_id)

@app.route("/")
def index():
    db = get_db()
    rows = db.execute("""
        SELECT
            Funeral.FuneralId,
            Client.Name AS ClientName,
            Client.RelationToDeceased,
            Deceased.FirstName || ' ' || Deceased.LastName AS DeceasedName,
            Deceased.DateOfBirth,
            Deceased.DateOfDeath,
            Funeral.Date
        FROM Funeral
        JOIN Client ON Funeral.ClientId = Client.ClientId
        JOIN Deceased ON Funeral.DeceasedId = Deceased.DeceasedId
        ORDER BY Funeral.Date DESC
    """).fetchall()

    from datetime import datetime

    funerals = []
    for row in rows:
        dob = row["DateOfBirth"]
        dod = row["DateOfDeath"]

        # Format dates as DD/MM/YYYY
        try:
            dob_dt = datetime.strptime(dob, "%Y-%m-%d")
            dob_fmt = dob_dt.strftime("%d/%m/%Y")
        except:
            dob_fmt = "-"
            dob_dt = None

        try:
            dod_dt = datetime.strptime(dod, "%Y-%m-%d")
            dod_fmt = dod_dt.strftime("%d/%m/%Y")
        except:
            dod_fmt = "-"
            dod_dt = None

        # Age calculation
        try:
            if dob_dt and dod_dt:
                age = dod_dt.year - dob_dt.year - ((dod_dt.month, dod_dt.day) < (dob_dt.month, dob_dt.day))
                date_summary = f"{dob_fmt} - {dod_fmt} ({age}yrs)"
            else:
                date_summary = f"{dob_fmt} - {dod_fmt}"
        except:
            date_summary = f"{dob_fmt} - {dod_fmt}"

        # Combine client name and relation
        client_display = f"{row['ClientName']} ({row['RelationToDeceased']})" if row["RelationToDeceased"] else row["ClientName"]

        funerals.append({
            "FuneralId": row["FuneralId"],
            "ClientDisplay": client_display,
            "DeceasedName": row["DeceasedName"],
            "DateSummary": date_summary,
            "FuneralDate": row["Date"] or "-"
        })

    return render_template("index.html", funerals=funerals)

@app.route("/add/funeral_record", methods=["GET", "POST"])
def add_funeral_record():
    db = get_db()
    staff_list = db.execute("SELECT StaffId, Name FROM Staff").fetchall()

    if request.method == "POST":
        # 1. Insert Client
        client_name = request.form["client_name"]
        client_contact = request.form.get("client_contact", "")
        relation = request.form.get("relation", "")
        db.execute("INSERT INTO Client (Name, Contact, RelationToDeceased) VALUES (?, ?, ?)",
                   (client_name, client_contact, relation))
        client_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]

        # 2. Insert Deceased
        first = request.form["deceased_first"]
        last = request.form["deceased_last"]
        dob = request.form.get("dob")
        dod = request.form.get("dod")
        db.execute("""
            INSERT INTO Deceased (FirstName, LastName, DateOfBirth, DateOfDeath, ClientId)
            VALUES (?, ?, ?, ?, ?)
        """, (first, last, dob, dod, client_id))
        deceased_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]

        # 3. Insert Funeral
        location = request.form.get("location")
        date = request.form.get("funeral_date")
        staff_id = request.form.get("staff_id")
        db.execute("""
            INSERT INTO Funeral (ClientId, DeceasedId, Location, Date, StaffId)
            VALUES (?, ?, ?, ?, ?)
        """, (client_id, deceased_id, location, date, staff_id))

        db.commit()
        return redirect(url_for("index"))

    return render_template("add_funeral_record.html", staff_list=staff_list)

@app.route("/funeral/<int:id>")
def funeral_detail(id):
    db = get_db()
    data = db.execute("""
        SELECT 
            Funeral.FuneralId,
            Funeral.Location,
            Funeral.Date AS FuneralDate,
            Client.Name AS ClientName,
            Client.Contact AS ClientContact,
            Client.RelationToDeceased,
            Deceased.FirstName || ' ' || Deceased.LastName AS DeceasedName,
            Deceased.DateOfBirth,
            Deceased.DateOfDeath,
            Staff.Name AS StaffName,
            Staff.Contact AS StaffContact,
            Staff.JobTitle,
            Invoice.Details AS InvoiceDetails,
            Invoice.Status AS InvoiceStatus
        FROM Funeral
        LEFT JOIN Client ON Funeral.ClientId = Client.ClientId
        LEFT JOIN Deceased ON Funeral.DeceasedId = Deceased.DeceasedId
        LEFT JOIN Staff ON Funeral.StaffId = Staff.StaffId
        LEFT JOIN Invoice ON Funeral.InvoiceId = Invoice.InvoiceId
        WHERE Funeral.FuneralId = ?
    """, (id,)).fetchone()

    if not data:
        return "Record not found", 404

    return render_template("funeral_detail.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)