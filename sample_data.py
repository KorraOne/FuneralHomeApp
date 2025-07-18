import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect("funeralhome.db")
cursor = conn.cursor()

def insert_and_get_id(sql, params):
    cursor.execute(sql, params)
    return cursor.lastrowid

# Seed 3 staff members
staff_ids = []
staff_data = [
    ("Alice Morton", "0400 123 456", "Funeral Director"),
    ("Brian Shaw", "0400 987 654", "Mortician"),
    ("Catherine Lee", "0401 555 888", "Chapel Coordinator")
]
for name, contact, title in staff_data:
    staff_ids.append(insert_and_get_id(
        "INSERT INTO Staff (Name, Contact, JobTitle) VALUES (?, ?, ?)",
        (name, contact, title)
    ))

# Seed 3 funeral records
funerals = [
    {
        "client": ("John Riley", "john@example.com", "Brother"),
        "deceased": ("Michael", "Riley", "1965-04-15", "2025-07-01"),
        "location": "Starlight Chapel",
        "funeral_date": "2025-07-10",
        "staff": staff_ids[0],
        "invoice": "Standard cremation"
    },
    {
        "client": ("Karen Finch", "karen@example.com", "Mother"),
        "deceased": ("Emily", "Finch", "2003-06-21", "2025-07-03"),
        "location": "Sunrise Gardens",
        "funeral_date": "2025-07-12",
        "staff": staff_ids[1],
        "invoice": "Youth memorial package"
    },
    {
        "client": ("Derek Nguyen", "derek@example.com", "Son"),
        "deceased": ("Lan", "Nguyen", "1940-01-12", "2025-06-29"),
        "location": "Peaceful River Chapel",
        "funeral_date": "2025-07-05",
        "staff": staff_ids[2],
        "invoice": "Traditional Buddhist rites"
    }
]

for entry in funerals:
    client_id = insert_and_get_id(
        "INSERT INTO Client (Name, Contact, RelationToDeceased) VALUES (?, ?, ?)",
        entry["client"]
    )

    deceased_id = insert_and_get_id(
        "INSERT INTO Deceased (FirstName, LastName, DateOfBirth, DateOfDeath, ClientId) VALUES (?, ?, ?, ?, ?)",
        (*entry["deceased"], client_id)
    )

    invoice_id = insert_and_get_id(
        "INSERT INTO Invoice (Details, Status) VALUES (?, ?)",
        (entry["invoice"], "Pending")
    )

    cursor.execute(
        "INSERT INTO Funeral (ClientId, DeceasedId, Location, Date, StaffId, InvoiceId) VALUES (?, ?, ?, ?, ?, ?)",
        (client_id, deceased_id, entry["location"], entry["funeral_date"], entry["staff"], invoice_id)
    )

conn.commit()
conn.close()
print("Multiple funeral records seeded successfully.")