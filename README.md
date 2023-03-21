# Individual Assignment

This assignment is a web application that utilizes a database of students, instructors, and courses. The application allows the user to add, remove, and modify each of these entities, as well as keep track of how they are related. Finally, it includes a way to track the grades of students enrolled in each class.

This assignment utilizes Flask (python), SQLAlchemy, HTML, CSS, Jinja, and javascript

## File Structure

You can find the html file here: ./templates/index.html
You can find the database file here: ./instance/site.db
You can find the style sheet here: ./static/css/site.css

## Installation

In order to run this code, it is recommended to use a virtual environment and a package manager. These directions will be written according to the package manager pip.

1. Download the code to your desired location and navigate to the based of the directory

2. In your terminal, create a virtual environment using virtualenv and install the required packages

```
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
```

## Usage

In your terminal... 
```
# activate the virtual environment
source env/bin/activate
# reconfigure the database
python3 init_db.py
# run the application
python3 app.py
```

Copy and paste the http address into your browser to use the application.