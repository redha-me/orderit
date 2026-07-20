# 🛵 OrderIt

> A B2B food delivery platform built with **Python Django** and **Tailwind CSS**.

[![Django](https://img.shields.io/badge/Django-4.0.3-092E20?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.x-38B2AC?style=flat&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**OrderIt** is a business-to-business (B2B) delivery management application that connects restaurants with delivery personnel. It provides a complete workflow for managing orders, tracking deliveries, and coordinating between restaurant partners and delivery agents.

🔗 **Live Demo:** [redha.pythonanywhere.com](https://redha.pythonanywhere.com/)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## ✨ Features

- 🍽️ **Restaurant Partner Management** – Onboard and manage restaurant partners
- 🛒 **Smart Cart System** – Add, update, and manage orders with a dynamic cart
- 🚴 **Delivery Agent Module** – Assign and track delivery personnel
- 👤 **User Authentication** – Secure registration and login system
- 🌍 **Multi-language Support** – Arabic (AR) and English localization
- 📍 **Geolocation Services** – Location tracking via Mapbox & Geocoder
- 📁 **File Uploads** – Image handling with Pillow & AWS S3 (Boto3)
- 📱 **Responsive UI** – Built with Tailwind CSS for a seamless experience

---

## 🛠 Tech Stack

| Layer        | Technology                          |
|--------------|-------------------------------------|
| Backend      | Python 3.8+ / Django 4.0.3         |
| Frontend     | HTML5 / Tailwind CSS                |
| Database     | SQLite (dev) / PostgreSQL (prod)    |
| Maps         | Mapbox / Geocoder                   |
| Storage      | AWS S3 (Boto3)                      |
| Deployment   | Heroku / PythonAnywhere             |
| Server       | Gunicorn + WhiteNoise               |

---

## 📁 Project Structure

```
orderit/
├── cart/                   # Shopping cart & order management
├── config/                 # Django project settings & URLs
├── core/                   # Core application logic
├── delivery_man/           # Delivery agent management
├── locale/
│   └── ar/LC_MESSAGES/     # Arabic translations
├── partner_restaurent/     # Restaurant partner module
├── static/                 # Static assets (CSS, JS, images)
├── templates/              # HTML templates
├── uploads/                # User-uploaded files
├── users/                  # User authentication & profiles
├── .env                    # Environment variables
├── data.json               # Seed / fixture data
├── db.sqlite3              # SQLite database (development)
├── manage.py               # Django management script
├── Procfile                # Heroku deployment config
├── requirements.txt        # Python dependencies
└── runtime.txt             # Python runtime version
```

---

## 🚀 Getting Started

### Prerequisites

- Python **3.8+**
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/redha-me/orderit.git
   cd orderit
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

8. Open your browser and navigate to `http://127.0.0.1:8000/`

---

## 🔐 Environment Variables

Create a `.env` file in the project root with the following variables:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
DATABASE_URL=your-database-url
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
MAPBOX_ACCESS_TOKEN=your-mapbox-token
```

---

## ☁️ Deployment

### Heroku

This project is configured for Heroku deployment via the included `Procfile`:

```bash
heroku create your-app-name
git push heroku main
heroku run python manage.py migrate
```

### PythonAnywhere

The app is also deployed on [PythonAnywhere](https://redha.pythonanywhere.com/).

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Redha Mechekak** – [GitHub](https://github.com/redha-me)

---

> ⭐ If you find this project useful, please consider giving it a star!
```

---
