# CSE Department Portal

A comprehensive web application built with Python and Django to manage a university's department. This portal provides different views and capabilities based on user roles (Admin, Teacher, Student, and Guest).

---

## 🚀 Core Features

This project implements a full CRUD (Create, Read, Update, Delete) and role-based permission system.

* **Public Portal:** Guests can view a list of all teachers and browse students organized by their batch (e.g., "BSc 10th").
* **Role-Based Access Control:** The site has 5 distinct user roles:
    * **Admin:** Full control. Manages user creation, batches, and rooms via the Django Admin Panel.
    * **Teacher:** Can update their profile, book classrooms, and manage their own bookings (update/delete).
    * **Student:** Can update their profile and view classroom availability.
    * **CR (Class Representative):** A special student who can also edit the notice board for their specific batch.
    * **Guest:** Can only view public-facing pages.
* **Authentication System:** Secure login, logout, and password management.
* **Profile Management:** Logged-in users can edit their own profiles (name, email, bio, phone, and profile photo).
* **Classroom Booking System:**
    * Teachers can book available classrooms for specific time slots.
    * The system automatically prevents booking conflicts and bookings in the past.
    * A public page displays the *current* status ("Vacant" or "In Use") and a full schedule for all rooms.
* **Dynamic Notice Board:**
    * The dashboard notice board changes based on the logged-in user.
    * Teachers and Admins see (and can edit) the "Teacher Notice".
    * Students see the notice for their *specific batch*.
    * CRs can edit the notice for their batch.

---

## 🛠️ Tech Stack

* **Backend:** Python, Django
* **Database:** SQLite (for development)
* **Frontend:** HTML, CSS, Bootstrap 5
* **Image Handling:** Pillow

---

## ⚙️ Setup and Installation

To run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)
    cd YOUR_REPOSITORY_NAME
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply the database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser (Admin) account:**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

7.  Open `http://127.0.0.1:8000/` in your browser.

---

## 📖 Usage

1.  Log in to the admin panel at `http://127.0.0.1:8000/admin/`.
2.  Use the admin panel to:
    * Create **Batches** (e.g., "BSc 10th").
    * Create **Classrooms** (e.g., "Room 201").
    * Create **Users** (Teachers and Students), setting their password, role, and batch.
3.  Log out and log in as a Teacher or Student to use the portal.
