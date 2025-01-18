# Sudhir-Varu-Full_Stack. 
## CrickScore - Real-Time Cricket Score Management System

CrickScore is a web-based real-time cricket score management and viewing application. The application allows the admin to update live scores and statistics, while the users can view the live scores in real time. The project is built using Python Flask, MySQL, HTML, CSS, JavaScript, and WebSockets.

## Features
Admin Dashboard: Allows the admin to update the score, track overs, and manage ball-by-ball updates.
User Interface: Users can view live scores and match details in real time.
Real-Time Updates: Live updates are pushed via WebSocket technology.
Separate Roles: Clear distinction between admin and user functionalities.

## Technologies Used
Frontend: HTML, CSS, JavaScript
Backend: Python Flask
Database: MySQL
Real-Time Communication: Flask-SocketIO (WebSockets)
Server: Flask development server

## Getting Started
Follow the instructions below to set up and run the project on your local machine.

## Prerequisites
Make sure you have the following installed on your system:
Python (3.8 or higher)
MySQL Server
A text editor or IDE (e.g., Visual Studio Code, PyCharm)

## Installation

### Clone the Repository:
git clone https://github.com/your-username/CrickScore.git cd CrickScore


### Set Up Python Virtual Environment:
Create a virtual environment:
python -m venv venv


## Activate the virtual environment
### On Windows:
venv\Scripts\activate

### On macOS/Linux:
source venv/bin/activate


## Install Python Dependencies:
pip install -r requirements.txt


## Set Up MySQL Database:
Open your MySQL server and create a database:


## Update your MySQL credentials in the main.py file:
  host='localhost',
  database='crickscore',
  user='your_username',
  password='your_password'


## Run the Application:
python main.py

Access the application in your browser:
Admin View: http://127.0.0.1:5000/ or http://localhost:5000/ (or adjust the port if different)
User View: http://127.0.0.1:5000/user or http://localhost:5000/user (or adjust the port if different)


## File Structure
crickscore/
│
├── static/
│   ├── css/
│   │   ├── style.css       # Common CSS for user and admin views
│   └── js/
│       ├── app.js          # JavaScript file for handling user and admin interactions
│
├── templates/
│   ├── index.html          # Admin view for managing scores and settings
│   ├── user.html           # User view for displaying live score updates
│
├── app.py                 # Flask backend application
├── requirements.txt        # List of Python dependencies
└── README.md               # Project documentation



## Troubleshooting
Database Connection Error: Ensure MySQL is running and credentials in app.py are correct.
WebSocket Issues: Ensure Flask-SocketIO is installed and running without network restrictions.
Port Conflict: If port 5000 is already in use, change the port in app.py:
