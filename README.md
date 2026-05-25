# Notes Web App

(IN this app , i am adding many tools to learn how they work)

A simple Flask-based notes application with user signup/login, note creation, editing, and deletion.
webhook test
## Project Structure

- `backend/`
  - `app.py` - Flask application and route handlers
  - `templates/` - HTML templates for home, signup, login, note list, and edit pages
  - `static/` - CSS styles and background image assets
- `requirements.txt` - Python dependencies

## Features

- Home page with background styling
- Signup and login functionality
- Create new notes
- View all notes for logged-in users
- Edit and delete existing notes

## Setup

1. Install Python 3.10+ if needed.
2. Create and activate a virtual environment:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

3. Install required packages:

```powershell
pip install flask mysql-connector-python
```

If you want, you can also use the package names in `requirements.txt` once the file encoding is fixed.

## Database

The app expects a MySQL database named `notes_app`.

Create the database and tables, for example:

```sql
CREATE DATABASE notes_app;
USE notes_app;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL
);

CREATE TABLE notes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  content TEXT NOT NULL,
  user_id INT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

Update the database credentials in `backend/app.py` if needed.

## Run

From the `backend` folder:

```powershell
python app.py
```

Open `http://127.0.0.1:5000/` in your browser.

## Notes
web notes app
- The home page background image is loaded from `backend/static/background_image.png`.
- If the background does not appear, try refreshing your browser cache (`Ctrl+F5`).
