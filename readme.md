# Course Management GUI

This repository contains a basic Python program for managing program courses using a graphical user interface (GUI) built with Tkinter library. The program allows users to create and view course subjects stored in a MySQL database.

## Requirements
- Python 3.x
- `tkinter` library
- `ttkbootstrap` library
- MySQL Connector/Python library
- MySQL database (configure connection details in `DATABASE_CONFIG.py`)

## Installation
1. Clone the repository: `git clone https://github.com/your-username/program-courses.git`
2. Install the required libraries: `pip install ttkbootstrap mysql-connector-python`
3. Configure the MySQL database connection details in `DATABASE_CONFIG.py`.

## Usage
1. Run the program: `python program_courses.py`
2. The program window will appear with two tabs: "Create Course Subject" and "View Course Subject".

### Create Course Subject Tab
- Enter the subject code, subject name, and subject units in the respective fields.
- Click the "Create Course Subject" button to add the course subject to the database.
- The result of the operation will be displayed below the button.

### View Course Subject Tab
- Click the "Refresh" button to retrieve the list of all course subjects from the database.
- The course subjects will be displayed in the listbox.
- Select a course subject from the listbox to view its details (subject name and units) below.

## Planned Features
- Add a "Delete Course Subject" button in the "View Course Subject" tab.
- Add a "Update Course Subject" button in the "View Course Subject" tab.