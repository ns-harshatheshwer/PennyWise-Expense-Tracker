# PennyWise — Personal Expense Tracker 🪙

> **Academic Object-Oriented Programming (OOP) Assignment Project**  
> A full-stack, personal finance management dashboard built with **Python 3.10+ (Flask)**, an **Object-Oriented architecture**, and a **persistent SQLite3 database**.

---

## 🌟 Overview

**PennyWise** is an intelligent personal financial tracking application designed to give users clarity over their expenditures and budget health. Built strictly to demonstrate core software engineering and Object-Oriented design principles, all domain validation, calculation algorithms, categorization logic, and database persistence are handled by pure Python OOP classes.

### Key Features
- **📊 Real-Time Financial Dashboard**: Instant visibility into total lifetime spending, current month expenses, remaining safe budget, and budget utilization progress.
- **💳 Transaction Management**: Full CRUD operations (Create, Read, Update, Delete) for expenses with titles, amounts, categories, dates, and optional notes.
- **🎯 Dynamic Monthly Budgeting**: Set monthly targets with customized warning thresholds (e.g. alert at 80% utilization, danger alert when exceeding 100%).
- **🏷️ Pre-Configured & Custom Categories**: Categorize spending across Food, Transport, Shopping, Education, Entertainment, Bills, Healthcare, and Others, with support for custom categories.
- **📈 Interactive Visualizations**:
  - 6-Month Expenditure Trend (curved area line chart with emerald gradient).
  - Monthly Category Breakdown (doughnut chart with utilization percentages).
  - 7-Day Spending Activity (interactive bar chart).
- **🔍 Search, Filtering & Sorting**: Instant client-side & server-side search by title or description, category filtering, and sorting by date, amount, or name.
- **💾 Persistent SQLite Database**: All data persists in local SQLite (`pennywise.db`) across server restarts.
- **📑 CSV Data Export**: One-click download of all transaction history in CSV format.
- **🔄 Sample Data Seeder**: Built-in seed engine for testing with realistic demo records, plus one-click data wipe.

---

## 🏗️ Object-Oriented Programming (OOP) Architecture

The backend is built around 6 core OOP classes located in the `models/` and `database/` modules. Each class exemplifies fundamental OOP principles:

```
┌────────────────────────────────────────────────────────┐
│                   BaseTransaction (ABC)                │
├────────────────────────────────────────────────────────┤
│ + to_dict() : dict                                     │
│ + calculate_monthly_impact(month) : float              │
│ + summary() : str                                      │
│ + validate() : bool                                    │
└──────────────────────────┬─────────────────────────────┘
                           │ inherits
┌──────────────────────────▼─────────────────────────────┐
│                      Transaction                       │
├────────────────────────────────────────────────────────┤
│ - _id, _title, _amount, _date, _description            │
│ + @property getters & setters with validation          │
└──────────────────────────┬─────────────────────────────┘
                           │ inherits
┌──────────────────────────▼─────────────────────────────┐
│                        Expense                         │
├────────────────────────────────────────────────────────┤
│ - _category : str                                      │
│ + summary() [Polymorphic override]                     │
│ + to_dict() [Polymorphic override]                     │
└──────────────────────────┬─────────────────────────────┘
                           │ inherits
┌──────────────────────────▼─────────────────────────────┐
│                   RecurringExpense                     │
├────────────────────────────────────────────────────────┤
│ - _frequency : str (daily/weekly/monthly/yearly)       │
│ + calculate_monthly_impact() [Polymorphic override]   │
└────────────────────────────────────────────────────────┘

┌──────────────────────────┐       ┌─────────────────────┐
│     DatabaseManager      │◄──────┤   ExpenseManager    │
│  (SQLite3 Data Layer)    │owns   │ (Domain Controller) │
└──────────────────────────┘       └──────────┬──────────┘
                                              │ composes
                                   ┌──────────▼──────────┐
                                   │  Budget & Category  │
                                   └─────────────────────┘
```

### 1. Abstraction (`models/transaction.py`)
- `BaseTransaction(ABC)` defines the abstract contract using Python's `abc.ABC` and `@abstractmethod`.
- Mandates that any financial transaction subclass must implement `to_dict()`, `calculate_monthly_impact()`, `summary()`, and `validate()`.

### 2. Encapsulation (`models/transaction.py`, `models/budget.py`)
- Internal attributes are protected using leading underscores (`_amount`, `_title`, `_date`, `_monthly_limit`).
- Access and modification are mediated exclusively via `@property` getters and setters that enforce strict validation rules:
  - `amount` must be a positive float greater than zero (`amount > 0`).
  - `title` must be a non-empty string between 2 and 100 characters.
  - `date` must strictly conform to ISO `YYYY-MM-DD` formatting.
  - `alert_threshold` must fall within the range `[1.0, 100.0]`.

### 3. Inheritance (`models/expense.py`)
- `Transaction` inherits from `BaseTransaction`.
- `Expense` inherits from `Transaction` using `super().__init__(...)`, augmenting the baseline transaction with category attributes and category validation.
- `RecurringExpense` extends `Expense`, adding recurrence frequencies (`daily`, `weekly`, `monthly`, `yearly`).

### 4. Polymorphism (`models/expense.py`, `models/expense_manager.py`)
- Method Overriding: `Expense` overrides `to_dict()` and `summary()` to inject category-specific representations.
- Subclass Polymorphism: `RecurringExpense.calculate_monthly_impact()` overrides the default calculation to normalize daily, weekly, or yearly commitments into equivalent monthly figures.
- `ExpenseManager` treats all transaction instances through polymorphic interfaces without needing to query their concrete types.

### 5. Composition (`models/expense_manager.py`)
- `ExpenseManager` does not inherit from `DatabaseManager`; instead, it **owns and composes** a `DatabaseManager` instance (`has-a` relationship).
- It orchestrates the lifecycle and interactions between `Expense`, `Budget`, and `Category` domain objects.

### 6. Database Separation (`database/db_manager.py`)
- `DatabaseManager` encapsulates low-level SQLite connection pooling, SQL statements, and transactions.
- Flask route handlers never issue SQL queries; they delegate all requests to `ExpenseManager`.

---

## 📁 Project Directory Structure

```
PennyWise/
├── app.py                      # Flask Application Factory & Server Entry Point
├── models/                     # OOP Domain Layer
│   ├── __init__.py             # Exports OOP Classes
│   ├── transaction.py          # BaseTransaction (ABC) and Transaction classes
│   ├── expense.py              # Expense and RecurringExpense subclasses
│   ├── category.py             # Category model
│   ├── budget.py               # Budget model with utilization calculations
│   └── expense_manager.py      # Core Domain Controller (Composition)
├── database/                   # Persistence Layer
│   ├── __init__.py
│   └── db_manager.py           # SQLite3 connection & CRUD manager
├── routes/                     # Delivery / Presentation Layer
│   ├── __init__.py
│   └── api.py                  # Flask REST API Endpoints
├── templates/                  # Frontend HTML Templates
│   └── index.html              # Main dashboard interface
├── static/                     # Frontend Static Assets
│   ├── css/
│   │   └── style.css           # Premium Dark Navy / Emerald theme
│   └── js/
│       └── script.js           # Client-side API caller & Chart.js charts
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── .gitignore                  # Git ignore rules
```

---

## 🚀 Getting Started & Local Installation

### Prerequisites
- **Python 3.10 or higher** installed (`python3 --version`)
- **pip** package manager installed

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/PennyWise.git
cd PennyWise
```

### 2. Create and Activate a Virtual Environment
```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows (Command Prompt)
python -m venv venv
venv\Scripts\activate.bat

# Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```
By default, the server will start on:
```
http://127.0.0.1:5000
```
Open your web browser and navigate to `http://127.0.0.1:5000` to interact with PennyWise.

---

## 📡 REST API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Service status and architecture metadata |
| `GET` | `/api/dashboard?month=YYYY-MM` | High-level metrics, trends, and recent expenses |
| `GET` | `/api/transactions` | Filter, search, and sort expense records |
| `GET` | `/api/transactions/<id>` | Fetch single expense details |
| `POST` | `/api/transactions` | Create a new expense (validated via `Expense`) |
| `PUT` | `/api/transactions/<id>` | Update an existing expense |
| `DELETE` | `/api/transactions/<id>` | Remove an expense record |
| `GET` | `/api/budget?month=YYYY-MM` | Retrieve monthly budget and utilization stats |
| `POST` | `/api/budget` | Set or update monthly budget limit and threshold |
| `GET` | `/api/categories` | Retrieve all category definitions |
| `POST` | `/api/categories` | Add a new custom category |
| `GET` | `/api/export/csv` | Export all transactions to CSV file |
| `POST` | `/api/demo-data` | Reload realistic sample transactions |
| `DELETE` | `/api/demo-data` | Wipe all user transaction and budget records |

---

## 🎨 Design System

- **Background**: Deep Navy & Charcoal (`#080C14`, `#0D131F`, `#121A2B`)
- **Accent**: Emerald Green (`#10B981`, `#059669`, `#34D399`)
- **Typography**: Plus Jakarta Sans & JetBrains Mono
- **Visuals**: Chart.js 4.4 interactive responsive charts with smooth tooltips and gradient fills
- **Responsiveness**: Fluid layout with mobile collapsible navigation sidebar

---

## 📝 License
This project is licensed under the Apache 2.0 License.
