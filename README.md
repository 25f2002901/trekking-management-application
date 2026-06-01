## Problem:
Adventure organizations require efficient systems to manage trekking activities involving trek organizers, staff, and participants. Currently, many trekking groups rely on spreadsheets, phone calls, or manual coordination, which makes it difficult to manage trek approvals, track bookings, avoid overbooking, and maintain trek history.

## Solution:
A Trekking Management Application web application that allows Admin, Trek Staff, and Users (Trekkers) to interact with the system based on their roles to help manage trekking activities in their respective areas of interest efficiently.

## Python Packages used for this web app:
* Flask for application back-end
* Jinja2 templating, HTML, CSS and Bootstrap for application front-end
* SQLite for database
* SQLAlchemy for database management and ORM (Object-Relational Mapping)
* Flask-Login for user authentication and session management
* Flask-WTF for form handling and validation
* JavaScript for richer user experience and interactivity

## Terminology of different roles:
1. **Admin:** A user with the highest level of access who manages the entire trekking system.
2. **Trek Staff:** A staff member responsible for managing and coordinating assigned treks.
3. **User (Trekker):** A participant who books and participates in trekking activities.

## Purpose of each sub-folder or file present in this repository:
1. *Models.py :* Programmatic representation of the underlying database structure and relationships.
2. *app.py :* The main application file that contains the Flask application and routes.
3. *static/ :* Contains static files such as CSS, JavaScript, and images used in the application.
4. *templates/ :* Contains HTML templates for rendering the web pages of the application.
5. *README.md :* This file, providing an overview of the project, its purpose, and instructions for setup and usage.
6. *requirements.txt :* A file listing the Python packages required to run the application, which can be installed using pip.
7. *instance/ :* Contains the SQLite database file and any instance-specific configuration files.
8. *.gitignore :* A file specifying which files and directories should be ignored by Git version control, such as the database file and virtual environment.
9. *venv/ :* A virtual environment directory that contains the isolated Python environment for the project, including installed packages.

