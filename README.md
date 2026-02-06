# Library Management System (Python + Tkinter + MySQL)

एक **GUI-based Library Management System** जिसमें **Role-based login** (Super Admin / Admin / User), **Books management**, **Issue/Return + Fine**, और **Dashboard charts** (matplotlib) शामिल हैं। यह प्रोजेक्ट Tkinter GUI और MySQL database के साथ काम करता है।

---

## Visuals



![Login Screen]([login window.png](https://github.com/Ajeet2611/LibraryProject/blob/main/login%20window.png))
![Admin Dashboard](https://github.com/Ajeet2611/LibraryProject/blob/main/Admin%20Dashboard.png)


---

## Tech Stack

- **Language**: Python 3.x
- **GUI**: Tkinter (Python standard library)
- **Database**: MySQL
- **DB Connector**: `mysql-connector-python` (code में `mysql.connector`)
- **Security**: `bcrypt` (password hashing/verification)
- **Images/Icons**: `Pillow` (PIL)
- **Export**: `openpyxl` (Excel export)
- **Charts**: `matplotlib` (Tkinter embedding)
- **OS Notes**: `winsound` (Windows-only; code में import है)

---

## Running Process

### Prerequisites

- **Python 3.10+** (recommendation)
- **MySQL Server** (local)
- (Optional) **pip / venv**

### Installation

1) Repo clone / डाउनलोड करें और project folder में जाएँ:

```bash
cd "D:\FULL PYTHONE MATERIAL\LibraryProject"
```

2) Virtual environment (recommended):

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

3) Dependencies install करें:

```bash
pip install mysql-connector-python bcrypt pillow openpyxl matplotlib
```

> नोट: Tkinter आमतौर पर Python के साथ bundled होता है। अगर Tkinter missing है, तो Python re-install में “tcl/tk” enabled रखें।

### Environment / Database Setup

यह प्रोजेक्ट MySQL database `library_db` पर depend करता है और code में ये tables उपयोग हो रहे हैं:

- **Users** (login के लिए): `UserID, Username, Password, Role, InstitutionID`
- **Institutions**: `InstitutionID, InstitutionName, Address`
- **Books**: `BookID, Title, Author, ISBN, TotalCopies, AvailableCopies, Status, InstitutionID`
- **Members**: `MemberID, Name, Email, Contact, Gender, Address, UserID, Password, Role, InstitutionID, Status`
- **Transactions**: `IssueID, BookID, MemberID, IssueDate, DueDate, ReturnStatus, InstitutionID`
- **Messages**: `Username, Message, MessageDate, Status, InstitutionID`
- **RolePermissions / InstitutionRolePermissions** (permissions के लिए)
- **StudentDetails / TeacherDetails / StaffDetails** (role detail tables)

#### DB Credentials (Important)

Database connection `db.py` में hardcoded है:

- `host="localhost"`
- `user="root"`
- `database="library_db"`

आपको अपने system के अनुसार **`db.py` में credentials अपडेट** करने होंगे।

### Run Commands

#### 1) GUI App (Recommended)

Login window से पूरा GUI flow start होता है:

```bash
python gui_login.py
```

#### 2) CLI Mode (Optional)

Basic CLI flow:

```bash
python main.py
```

#### 3) One-time Password Migration (Optional)

अगर आपकी `Users` table में plain-text passwords हैं, तो उन्हें bcrypt hash में convert करने के लिए:

```bash
python fix_passwords.py
```

---

## Features

- **Secure Login** (bcrypt password verify)
- **Role Based Access**
  - **SUPER_ADMIN**: Institution create, Institution Admin create
  - **ADMIN**: Book add/list, student/user add, issue/return, user activity, export excel, restore users
  - **USER**: Available books view, issued books + fine view, admin messaging
- **Books Inventory**
  - Total / Available copies management
  - ISBN uniqueness check (GUI add flow)
- **Issue / Return Workflow**
  - Due date calculation
  - Late fine calculation (₹5 per day)
  - “Already issued” validation
- **Dashboard Charts**
  - Active vs inactive users (pie)
  - Role distribution (bar)
- **Excel Export** (Users list)

---

## Folder Structure

```text
LibraryProject/
├─ assets/
│  ├─ bg.jpg
│  ├─ add.png
│  ├─ edit.png
│  ├─ delete.png
│  ├─ show.png
│  ├─ issue.png
│  ├─ return.png
│  ├─ history.png
│  ├─ logout.png
│  └─ ... (other icons)
├─ admin_add_book.py
├─ admin_add_user.py
├─ admin_books_list.py
├─ admin_issue_book.py
├─ admin_return_book.py
├─ admin_user_activity.py
├─ admin_users_view.py
├─ auth.py
├─ dashboard_charts.py
├─ db.py
├─ fix_passwords.py
├─ gui_admin.py
├─ gui_login.py
├─ gui_permission_manager.py
├─ gui_super_admin.py
├─ gui_user.py
├─ main.py
├─ permissions.py
├─ security.py
└─ README.md
```

---

## Notes / Tips

- **Assets path**: GUI modules `assets/` folder से images load करते हैं, इसलिए project root से run करना safest है।
- **Database schema**: इस repo में SQL migration/schema file नहीं दिख रही। अगर आप चाहें तो मैं आपके existing code के queries के आधार पर एक `schema.sql` भी generate कर सकता हूँ।

