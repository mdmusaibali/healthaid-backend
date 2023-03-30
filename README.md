
# HealthAid-backend
HealthAid-backend is an API developed using Django Rest Framework. It provides an API for MRMC College in Kalaburagi, which allows staff in hospitals to manage patients via a website or application. This repository serves as the backend for the project.

## Features
Two types of users: Superadmin and Staff
Superadmin can create, read, and delete Staff and Patients
Staff can create, read, and delete Patients
Both Superadmin and Staff can login via access token


## Installation
Clone the repository: git clone https://github.com/yaseen5748/healthaid-backend.git
Create and activate a virtual environment
Install the dependencies: pip install -r requirements.txt
Migrate the database: python manage.py migrate
Run the server: python manage.py runserver
  
## Usage
Open the browser and go to http://localhost:8000/
Login using your access token
Use the API endpoints to create, read, update or delete Staff and Patients
  
 
## Contributors
Yaseen
Md Musaib Ali @mdmusaibali
Venkatesh Patil @ven-p1
