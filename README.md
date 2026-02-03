# HRMS Lite - Human Resource Management System

A production-ready, lightweight HR Management System built with Django 6.0 and MySQL. Features employee management and attendance tracking with a modern, professional UI.

## 📋 Features

- **Dashboard**: Overview with employee count, attendance stats, and quick actions
- **Employee Management**: Add, view, and delete employees with unique IDs
- **Attendance Tracking**: Mark daily attendance (Present/Absent) with date filtering
- **Employee Attendance View**: Individual attendance history with statistics
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **AJAX Operations**: Smooth delete confirmations without page reload

## 🛠️ Tech Stack

- **Backend**: Django 6.0 (Class-Based Views)
- **Database**: MySQL 8.0+
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Styling**: Custom CSS with CSS Variables, Flexbox, Grid
- **Production**: Gunicorn + WhiteNoise

## 📁 Project Structure

```
HRMS_lite_project/             # Git Root
├── HRMS/                      # Main application
│   ├── static/
│   │   ├── css/main.css
│   │   └── js/main.js
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── HRMS_lite/                 # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/                 # HTML templates
├── .env                       # Environment variables
├── manage.py                  # Django entry point
├── requirements.txt           # Listed dependencies
├── Procfile                   # Render/Railway deployment
└── README.md
```

## 🚀 Local Development Setup

### Prerequisites

- Python 3.10+
- MySQL 8.0+
- pip (Python package manager)

### Step 1: Clone and Navigate

```bash
cd HRMS_lite
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Create MySQL Database

```sql
-- Connect to MySQL
mysql -u root -p

-- Create database
CREATE DATABASE HRMS_lite CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Exit
EXIT;
```

### Step 5: Configure Environment Variables

Create or update the `.env` file:

```env
# Database Configuration
DB_NAME=HRMS_lite
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306

# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Step 6: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 7: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### Step 8: Run Development Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

## 🌐 URLs

| URL | Description |
|-----|-------------|
| `/` | Dashboard |
| `/employees/` | Employee List |
| `/employees/add/` | Add New Employee |
| `/employees/<id>/delete/` | Delete Employee |
| `/employees/<id>/attendance/` | View Employee Attendance |
| `/attendance/` | All Attendance Records |
| `/attendance/add/` | Mark Attendance |
| `/admin/` | Django Admin Panel |

## 📦 Deployment (Render/Heroku)

### Environment Variables (Production)

```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=your-domain.com
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=3306
```

### Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Procfile (already included)

```
web: gunicorn HRMS_lite.wsgi --log-file -
```

## 🎨 Design Features

- **Color Scheme**: Professional blue/gray palette
- **Typography**: Inter font (Google Fonts)
- **Responsive**: Mobile-first design with breakpoints
- **Animations**: Subtle hover effects and transitions
- **Accessibility**: Proper labels, focus states, and contrast

## 📝 Models

### Employee
| Field | Type | Description |
|-------|------|-------------|
| employee_id | CharField | Unique identifier |
| full_name | CharField | Employee's full name |
| email | EmailField | Unique email address |
| department | CharField | Department name (optional) |
| created_at | DateTimeField | Record creation time |

### Attendance
| Field | Type | Description |
|-------|------|-------------|
| employee | ForeignKey | Reference to Employee |
| date | DateField | Attendance date |
| status | CharField | 'present' or 'absent' |
| created_at | DateTimeField | Record creation time |

## 🐛 Troubleshooting

### MySQL Connection Error
- Ensure MySQL service is running
- Verify credentials in `.env`
- Check if database exists

### Static Files Not Loading
- Run `python manage.py collectstatic`
- Check `STATIC_URL` and `STATICFILES_DIRS` in settings

### Migration Issues
```bash
python manage.py makemigrations HRMS
python manage.py migrate
```

## 📄 License

MIT License - Feel free to use for personal or commercial projects.

---

Built with ❤️ using Django
