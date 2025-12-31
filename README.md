# Software Engineering Portfolio | Abdulazeez Abdulakeem

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org)
[![Framework](https://img.shields.io/badge/Framework-Flask-black.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A full-stack professional portfolio designed to showcase backend architecture, database management, and responsive frontend design. Built with a modular Flask Factory Pattern.

**🚀 Live Demo:** [Your-Link-Here.com]

---

## 🛠️ Tech Stack

- **Backend:** Python / Flask
- **Database:** PostgreSQL (Production), SQLite (Development) / SQLAlchemy ORM
- **Frontend:** Bootstrap 5, Jinja2 Templates
- **Auth:** Flask-Login (Secure Admin Dashboard)
- **Communication:** Flask-Mail (SMTP Integration)

## ✨ Key Features

- **Dynamic Content Management:** Custom admin dashboard to manage projects, skills, and professional experience without touching the code.
- **Automated Analytics:** Custom-built visitor tracking system to monitor site engagement.
- **SMTP Contact System:** Integrated contact form with automated email notifications using Google App Passwords.
- **Responsive Architecture:** Mobile-first design optimized for all devices and screen sizes.
- **Factory Pattern:** Scalable code structure using Flask Blueprints and Application Factories.

## 📦 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone [https://github.com/aramydcd/abdulakeem-portfolio.git](https://github.com/aramydcd/abdulakeem-portfolio.git)
   cd abdulakeem-portfolio

```

2. **Set up Virtual Environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

```


3. **Install Dependencies**
```bash
pip install -r requirements.txt

```


4. **Environment Variables**
Create a `.env` file in the root directory:
```env
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///portfolio.db
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-google-app-password

```


5. **Run Application**
```bash
python main.py

```



## 🗺️ Project Structure

```text
├── app/
│   ├── models.py          # SQLAlchemy Models (User, Project, Visitor)
├── ├── _init_.py              # Configuration settings
│   ├── routes.py          # Main application logic & Blueprints
│   ├── static/            # CSS, JS, and Images
│   └── templates/         # Jinja2 HTML templates
├── main.py                 # Application entry point
└── requirements.txt       # Project dependencies

```

---

## 👤 Contact

**Abdulazeez Abdulakeem** - [abdulakeem606@gmail.com]

*Software Engineer | Computer Science Graduate*

```