# Project Overview

This project is a simple Flask web application designed as a "Dual Vacation Planner". It allows two users, "Franz" and "Polina", to plan their vacations for the year 2026 in Zurich. The application displays a table of vacation blocks, calculates the end dates of vacations based on the start date and number of days used, and shows the remaining vacation days for each person. The frontend is interactive, updating the vacation plan in real-time as the users modify the inputs.

## Main Technologies

*   **Backend:** Python with Flask
*   **Frontend:** HTML, CSS, JavaScript
*   **WSGI Server:** gunicorn (for production)

## Architecture

*   `app.py`: The main Flask application file. It defines the routes, handles the business logic for calculating vacation dates, and renders the HTML template.
*   `templates/index.html`: The main and only HTML page, which uses Jinja2 templating to display the vacation planner.
*   `static/style.css`: Contains the styles for the HTML page.
*   `static/script.js`:  Contains the client-side logic to handle user input and dynamically update the vacation plan by making AJAX calls to the Flask backend.
*   `requirements.txt`: Lists the Python dependencies.

# Building and Running

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Development Server:**
    ```bash
    python app.py
    ```
    The application will be available at `http://127.0.0.1:5000`.

3.  **Run in Production (with gunicorn):**
    ```bash
    gunicorn --bind 0.0.0.0:8000 app:app
    ```

# Development Conventions

*   The application follows a standard Flask project structure.
*   Business logic is contained within the `app.py` file.
*   Frontend files are separated into `static` and `templates` directories.
*   The application uses a predefined list of holidays for Zurich in 2026 to accurately calculate workdays.
