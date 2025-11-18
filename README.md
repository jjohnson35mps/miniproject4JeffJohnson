### INF601 - Advanced Programming in Python
### Jeff Johnson
### Mini Project 4
 
## Mini Project 4 — CFP / Polls Web App (Django)
 
A small Django web app where users can participate in trivia and CFP-style polls, register/login, vote, and view results. The project uses Django’s built-in authentication, Bootstrap 5 styling, and includes a required modal.

## Description
 
What this app does

- **Pages (8):** Home, About, Trivia, Poll List, Poll Detail (Vote), Results, Register, Login  
- **Auth:** Register, login, logout (Django’s built-in authentication system)  
- **Polls:** Users can vote on poll questions and view the results in real time  
- **Data:** Models include `Question` and `Choice` with a ForeignKey relationship  
- **Admin:** Django admin interface to manage questions and choices  
- **UI:** Bootstrap 5 with a required modal (“View Info”), consistent base template, and custom CSS  
- **Database:** SQLite using Django ORM and migrations



```
├─ manage.py
├─ requirements.txt
├─ README.md (this file)
├─ mysite/
│  ├─ __init__.py
│  ├─ asgi.py
│  ├─ settings.py   # Installed apps, templates, static config
│  ├─ urls.py       # Includes polls.urls and authentication routes
│  └─ wsgi.py
├─ polls/
│  ├─ __init__.py
│  ├─ admin.py      # ModelAdmin for Question and Choice
│  ├─ models.py     # Question and Choice models
│  ├─ views.py      # home, about, trivia, register, logout_then_home, etc.
│  ├─ urls.py       # App-specific routes
│  ├─ fixtures/
│  │  └─ cfp_questions_with_choices.json
│  ├─ migrations/
│  │  └─ 0001_initial.py
│  ├─ static/
│  │  └─ polls/
│  │     ├─ cfp_trophy.png
│  │     └─ style.css
│  └─ templates/
│     ├─ polls/
│     │  ├─ about.html
│     │  ├─ base.html
│     │  ├─ cfp_results.html
│     │  ├─ cfp_vote.html
│     │  ├─ detail.html
│     │  ├─ home.html
│     │  ├─ index.html
│     │  ├─ question_list.html
│     │  ├─ results.html
│     │  └─ trivia.html
│     └─ registration/
│        ├─ login.html
│        └─ register.html
└─ db.sqlite3        # Created at runtime
```


### Database Schema:
- **Question:** id, question_text, pub_date  
- **Choice:** id, question (FK), choice_text, votes  

Foreign keys and relationships are managed automatically through Django’s ORM and migrations.

---

## Using The App

1. **Create your database**
   - Run the Django commands below to initialize your database:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     python manage.py createsuperuser
     python manage.py loaddata cfp_questions_with_choices.json
     ```

2. **Start the development server**
   ```bash
   python manage.py runserver
   
3. Access the application
    - App: http://127.0.0.1:8000/    
    - Admin: http://127.0.0.1:8000/admin/

4. Register a user
    - Go to /accounts/register/ and create a new user account.    
    - Then login through /accounts/login/.    
    - Logout via /accounts/logout/.

5. Vote in a poll
    - Visit /polls/ to view available polls.
    - Click a question to open its detail page, select a choice, and submit your vote.
    - After voting, you’ll see the updated results page.

6. Check results
    - View results directly after voting or by visiting /polls/<id>/results/.
    - The page shows each choice and its current vote count.

7. Use the admin interface
    - Log into /admin/ with your superuser credentials to manage Question and Choice models.

Quick Info:
Click the “View Info” button on the home page to open the required Bootstrap modal.
All templates extend from base.html for consistent site styling.

 
### Dependencies
 
- Python 3.13.7
- Django 5.2.7
- Operating System: 
    - Windows

- Required libraries (install with pip):
```bash
pip install -r requirements.txt
```

## Installing
 
1. Clone or download this project to your local machine.
2. Go to the project root.
3. Ensure you have the required dependencies listed above installed
   - pip install -r requirements.txt
4. Initialize the database.
   - python manage.py makemigrations
   - python manage.py migrate
   - python manage.py createsuperuser
5. Start the development server.
   - python manage.py runserver
 
## Executing program

Run the server
```bash
python manage.py runserver
```
The server will run on http://127.0.0.1:8000

## Help
 
If you encounter issues, re-run pip installs and re-seed the app settings:
```bash
pip install -r requirements.txt
python manage.py runserver
```
 
## Authors
 
Jeff Johnson
 
## Version History
 
- 0.1
  - Initial Release
 
## License
 
This project is licensed under the MIT License - see the LICENSE.md file for details
 
## Acknowledgments
 
Inspiration, code snippets, etc.
- [Django Tutorial](https://docs.djangoproject.com/en/5.2/intro/tutorial01/)
- [ChatGPT](https://chatgpt.com/g/g-p-690132306a9c8191b70435990b8efb62-mini-project-four/project)
*** I use a ChatGPT paid acct, so I cannot share ***

