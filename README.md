
# HealthAid-backend
HealthAid-backend is an API developed using Django Rest Framework. It provides an API for MRMC College in Kalaburagi, which allows staff in hospitals to manage patients via a website or application. This repository serves as the backend for the project.

## Features
1. Two types of users: Superadmin and Staff
2. Superadmin can create, read, and delete Staff and Patients
3. Staff can create, read, and delete Patients
4. Both Superadmin and Staff can login via access token


## Installation
1. Clone the repository: git clone https://github.com/yaseen5748/healthaid-backend.git
2. Create and activate a virtual environment
3. Install the dependencies: pip install -r requirements.txt
4. Migrate the database: python manage.py migrate
5. Run the server: python manage.py runserver
  
## Usage
1. Open the browser and go to http://localhost:8000/
2. Login using your access token
3. Use the API endpoints to create, read, update or delete Staff and Patients
  
 
## Contributors
Yaseen <br>
Md Musaib Ali @mdmusaibali <br>
Venkatesh Patil @ven-p1 <br>
