import sqlite3
from datetime import datetime
from tkinter import *
from tkinter import messagebox, ttk

# Connect to the database (creates the file if it doesn't exist)
def connect_db():
    conn = sqlite3.connect("ambulance_booking_system.db")
    cur = conn.cursor()
    
    #  ambulances table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ambulances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ambulance_id TEXT UNIQUE,
            location TEXT,
            status TEXT DEFAULT 'Available'
        )
    """)
    
   # Booking Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ambulance_id TEXT,
            user_name TEXT,
            booking_time TEXT,
            FOREIGN KEY (ambulance_id) REFERENCES ambulances (ambulance_id)
        )
    """)
    
    conn.commit()
    conn.close()

def add_sample_data():
    conn = sqlite3.connect("ambulance_booking_system.db")
    cur = conn.cursor()
    
   
    ambulances = [
        ("A101", "Delhi"),
        ("A102", "Jaipur"),
        ("A103", "Nims"),
        ("A104", "Gurugram"),
        ("A105", "Chennai"),
        ("A106", "Banglore"),
        ("A107", "Mumbai"),
        ("A108", "Goa"),
        ("A109", "Lucknow"),
        ("A110", "Noida")
    ]
    
    for ambulance in ambulances:
        try:
            cur.execute("INSERT INTO ambulances (ambulance_id, location) VALUES (?, ?)", ambulance)
        except sqlite3.IntegrityError:
            pass  # Ambulance already exists
    
    conn.commit()
    conn.close()

# Function to book an ambulance
def book_ambulance(ambulance_id, user_name):
    conn = sqlite3.connect("ambulance_booking_system.db")
    cur = conn.cursor()
    
    # Check if the ambulance is available
    cur.execute("SELECT status FROM ambulances WHERE ambulance_id = ?", (ambulance_id,))
    result = cur.fetchone()
    
    if result and result[0] == "Available":
        # Update ambulance status to 'Booked'
        cur.execute("UPDATE ambulances SET status = 'Booked' WHERE ambulance_id = ?", (ambulance_id,))
        
        # Insert a booking record
        cur.execute("INSERT INTO bookings (ambulance_id, user_name, booking_time) VALUES (?, ?, ?)",
                    (ambulance_id, user_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        
        conn.commit()
        messagebox.showinfo("Success", f"Ambulance {ambulance_id} has been successfully booked by {user_name}.")
    elif result:
        messagebox.showwarning("Error", f"Ambulance {ambulance_id} is already booked.")
    else:
        messagebox.showerror("Error", f"Ambulance {ambulance_id} not found.")
    
    conn.close()

# Function to cancel a booking
def cancel_booking(ambulance_id):
    conn = sqlite3.connect("ambulance_booking_system.db")
    cur = conn.cursor()
    
    # Check if the ambulance is booked
    cur.execute("SELECT status FROM ambulances WHERE ambulance_id = ?", (ambulance_id,))
    result = cur.fetchone()
    
    if result and result[0] == "Booked":
        # Update ambulance status to 'Available'
        cur.execute("UPDATE ambulances SET status = 'Available' WHERE ambulance_id = ?", (ambulance_id,))
        
        # Delete the booking record
        cur.execute("DELETE FROM bookings WHERE ambulance_id = ?", (ambulance_id,))
        
        conn.commit()
        messagebox.showinfo("Success", f"Booking for Ambulance {ambulance_id} has been canceled.")
    elif result:
        messagebox.showwarning("Error", f"Ambulance {ambulance_id} is not booked.")
    else:
        messagebox.showerror("Error", f"Ambulance {ambulance_id} not found.")
    
    conn.close()

# Function to view available ambulances
def view_available_ambulances():
    conn = sqlite3.connect("ambulance_booking_system.db")
    cur = conn.cursor()
    
    cur.execute("SELECT ambulance_id, location FROM ambulances WHERE status = 'Available'")
    ambulances = cur.fetchall()
    
    if ambulances:
        available_list = "\n".join([f"Ambulance ID: {amb[0]}, Location: {amb[1]}" for amb in ambulances])
        messagebox.showinfo("Available Ambulances", available_list)
    else:
        messagebox.showinfo("Available Ambulances", "No ambulances available at the moment.")
    
    conn.close()

# Function to view all bookings
def view_all_bookings():
    conn = sqlite3.connect("ambulance_booking_system.db")
    cur = conn.cursor()
    
    cur.execute("SELECT booking_id, ambulance_id, user_name, booking_time FROM bookings")
    bookings = cur.fetchall()
    
    if bookings:
        booking_list = "\n".join([f"Booking ID: {booking[0]}, Ambulance ID: {booking[1]}, User: {booking[2]}, Time: {booking[3]}" for booking in bookings])
        messagebox.showinfo("Booking Records", booking_list)
    else:
        messagebox.showinfo("Booking Records", "No bookings available.")
    
    conn.close()

# GUI Setup
def setup_gui():
    root = Tk()
    root.title("Ambulance Booking System")
    root.geometry("500x400")
    root.configure(bg="#f4f4f4")

    # Title Frame
    title_frame = Frame(root, bg="#4CAF50")
    title_frame.pack(fill=X)
    
    title_label = Label(title_frame, text="Ambulance Booking System", font=("Helvetica", 20, "bold"), bg="#4CAF50", fg="white")
    title_label.pack(pady=10)

    # Main Frame
    main_frame = Frame(root, bg="#f4f4f4")
    main_frame.pack(pady=10)

    # View Available Ambulances Button
    Button(main_frame, text="View Available Ambulances", command=view_available_ambulances, width=30, bg="#2196F3", fg="white").pack(pady=10)

    # Book Ambulance Section
    book_frame = LabelFrame(main_frame, text="Book Ambulance", bg="#f4f4f4", font=("Helvetica", 12, "bold"))
    book_frame.pack(pady=10, padx=10, fill="both")

    Label(book_frame, text="Enter Ambulance ID:", bg="#f4f4f4").pack(pady=5)
    ambulance_id_entry = Entry(book_frame)
    ambulance_id_entry.pack(pady=5)

    Label(book_frame, text="Enter Your Name:", bg="#f4f4f4").pack(pady=5)
    user_name_entry = Entry(book_frame)
    user_name_entry.pack(pady=5)

    Button(book_frame, text="Book Ambulance", command=lambda: book_ambulance(ambulance_id_entry.get(), user_name_entry.get()), width=30, bg="#4CAF50", fg="white").pack(pady=10)

    # Cancel Booking Section
    cancel_frame = LabelFrame(main_frame, text="Cancel Booking", bg="#f4f4f4", font=("Helvetica", 12, "bold"))
    cancel_frame.pack(pady=10, padx=10, fill="both")

    Label(cancel_frame, text="Enter Ambulance ID to Cancel:", bg="#f4f4f4").pack(pady=5)
    cancel_ambulance_id_entry = Entry(cancel_frame)
    cancel_ambulance_id_entry.pack(pady=5)

    Button(cancel_frame, text="Cancel Booking", command=lambda: cancel_booking(cancel_ambulance_id_entry.get()), width=30, bg="#F44336", fg="white").pack(pady=10)

    # View All Bookings Button
    Button(main_frame, text="View All Bookings", command=view_all_bookings, width=30, bg="#FF9800", fg="white").pack(pady=10)

    # Exit Button
    Button(main_frame, text="Exit", command=root.quit, width=30, bg="#9E9E9E", fg="white").pack(pady=20)

    root.mainloop()

# Initialize Database and GUI
if __name__ == "__main__":
    connect_db()
    add_sample_data()
    setup_gui()
