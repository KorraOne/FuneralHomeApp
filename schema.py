import sqlite3

conn = sqlite3.connect("funeralhome.db")
cursor = conn.cursor()

# Staff
cursor.execute("""
CREATE TABLE IF NOT EXISTS Staff (
    StaffId INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Contact TEXT,
    JobTitle TEXT
);
""")

# Client
cursor.execute("""
CREATE TABLE IF NOT EXISTS Client (
    ClientId INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Contact TEXT,
    RelationToDeceased TEXT
);
""")

# Deceased
cursor.execute("""
CREATE TABLE IF NOT EXISTS Deceased (
    DeceasedId INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    DateOfBirth TEXT,
    DateOfDeath TEXT,
    ClientId INTEGER,
    FOREIGN KEY (ClientId) REFERENCES Client(ClientId)
);
""")

# Invoice
cursor.execute("""
CREATE TABLE IF NOT EXISTS Invoice (
    InvoiceId INTEGER PRIMARY KEY AUTOINCREMENT,
    Details TEXT,
    Status TEXT DEFAULT 'Pending'
);
""")

# Funeral
cursor.execute("""
CREATE TABLE IF NOT EXISTS Funeral (
    FuneralId INTEGER PRIMARY KEY AUTOINCREMENT,
    ClientId INTEGER,
    DeceasedId INTEGER,
    Location TEXT,
    Date TEXT,
    StaffId INTEGER,
    InvoiceId INTEGER,
    FOREIGN KEY (ClientId) REFERENCES Client(ClientId),
    FOREIGN KEY (DeceasedId) REFERENCES Deceased(DeceasedId),
    FOREIGN KEY (StaffId) REFERENCES Staff(StaffId),
    FOREIGN KEY (InvoiceId) REFERENCES Invoice(InvoiceId)
);
""")

# FormInfo
cursor.execute("""
CREATE TABLE IF NOT EXISTS FormInfo (
    InfoId INTEGER PRIMARY KEY AUTOINCREMENT,
    FuneralId INTEGER UNIQUE,
    DeceasedAddress TEXT,
    ExecutorName TEXT,
    ExecutorContact TEXT,
    ViewingType TEXT,
    CollectionDate TEXT,
    ConsultationDate TEXT,
    FOREIGN KEY (FuneralId) REFERENCES Funeral(FuneralId)
);
""")

# FormBooking
cursor.execute("""
CREATE TABLE IF NOT EXISTS FormBooking (
    BookingId INTEGER PRIMARY KEY AUTOINCREMENT,
    FuneralId INTEGER UNIQUE,
    ViewingBooked TEXT,
    ViewingDate TEXT,
    ViewingAddress TEXT,
    ViewingContact TEXT,
    ViewingPhone TEXT,
    ViewingTime TEXT,
    JumperCount INTEGER,
    CollectorName TEXT,
    NewspaperNotes TEXT,
    ChapelBooking TEXT,
    CemeteryBooking TEXT,
    CelebrantName TEXT,
    CelebrantPhone TEXT,
    CelebrantEmail TEXT,
    ServiceType TEXT,
    FOREIGN KEY (FuneralId) REFERENCES Funeral(FuneralId)
);
""")

# FormService
cursor.execute("""
CREATE TABLE IF NOT EXISTS FormService (
    ServiceId INTEGER PRIMARY KEY AUTOINCREMENT,
    FuneralId INTEGER UNIQUE,
    ViewingAddress TEXT,
    ViewingDate TEXT,
    ViewingTime TEXT,
    ViewingContact TEXT,
    VAD TEXT, Cremation TEXT, NC TEXT, Burial TEXT, Viewing TEXT,
    LimoTransport TEXT, Coffin TEXT, Urn TEXT, Livestream TEXT,
    Florist TEXT, Marquee TEXT, DVD TEXT, Embalm TEXT,
    Catering TEXT, Printing TEXT, OtherFlag TEXT,
    CateringAddress TEXT, CateringContact TEXT, CateringMobile TEXT, CateringEmail TEXT,
    TransportAddress TEXT, TransportContact TEXT, TransportMobile TEXT, TransportEmail TEXT,
    LivestreamAddress TEXT, LivestreamContact TEXT, LivestreamMobile TEXT, LivestreamEmail TEXT,
    FloristAddress TEXT, FloristContact TEXT, FloristMobile TEXT, FloristEmail TEXT,
    DVDAddress TEXT, DVDContact TEXT, DVDMobile TEXT, DVDEmail TEXT,
    EmbalmAddress TEXT, EmbalmContact TEXT, EmbalmMobile TEXT, EmbalmEmail TEXT,
    CoffinAddress TEXT, CoffinContact TEXT, CoffinMobile TEXT, CoffinEmail TEXT,
    UrnAddress TEXT, UrnContact TEXT, UrnMobile TEXT, UrnEmail TEXT,
    MarqueeAddress TEXT, MarqueeContact TEXT, MarqueeMobile TEXT, MarqueeEmail TEXT,
    PrintingAddress TEXT, PrintingContact TEXT, PrintingMobile TEXT, PrintingEmail TEXT,
    OtherAddress TEXT, OtherContact TEXT, OtherMobile TEXT, OtherEmail TEXT,
    FOREIGN KEY (FuneralId) REFERENCES Funeral(FuneralId)
);
""")

# FormPapers
cursor.execute("""
CREATE TABLE IF NOT EXISTS FormPapers (
    PapersId INTEGER PRIMARY KEY AUTOINCREMENT,
    FuneralId INTEGER UNIQUE,
    DeceasedName TEXT,
    PickupAddress TEXT,
    DOB TEXT,
    DOD TEXT,
    Age INTEGER,
    ExecutorName TEXT,
    ExecutorContact TEXT,
    ExecutorEmail TEXT,
    CertDeath TEXT,
    CremPermit TEXT,
    DoctorForm TEXT,
    NDA TEXT,
    Notes TEXT,
    FOREIGN KEY (FuneralId) REFERENCES Funeral(FuneralId)
);
""")

# FormFinance (Line Items)
cursor.execute("""
CREATE TABLE IF NOT EXISTS FormFinance (
    FinanceId INTEGER PRIMARY KEY AUTOINCREMENT,
    FuneralId INTEGER,
    Category TEXT,
    Description TEXT,
    Quantity INTEGER,
    UnitCost REAL,
    FOREIGN KEY (FuneralId) REFERENCES Funeral(FuneralId)
);
""")

conn.commit()
conn.close()
print("Funeral database schema setup complete.")