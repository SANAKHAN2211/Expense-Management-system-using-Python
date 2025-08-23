# Expense-Management-system-using-Python

A full‑stack web application to simplify expense tracking, management, and analysis. With a clean Streamlit UI, FastAPI backend, and MySQL storage, it helps you stay on top of your spending with confidence.

<p align="center">
  <img src="assets/cover.png" alt="Expense-Management-system – cover" width="800"/>
</p>

---

## Table of Contents

* [Features](#features)
* [Tech Stack](#tech-stack)
* [Screens & Demo](#screens--demo)
* [Project Structure](#project-structure)
* [Getting Started](#getting-started)

  * [Prerequisites](#prerequisites)
  * [Environment Variables](#environment-variables)
  * [Setup & Run](#setup--run)
* [How It Works](#how-it-works)
* [App Tabs](#app-tabs)
* [API Overview](#api-overview)
* [Data Model](#data-model)
* [Testing](#testing)
* [Logging & Monitoring](#logging--monitoring)
* [Troubleshooting](#troubleshooting)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)

---

## Features

* ✅ **Expense Tracking**: Seamlessly add, edit, and delete expense records.
* 📄 **Paginated Views**: Browse expenses by date with **5 entries per page**.
* 🗂️ **Category Insights**: Analyze spend by category across custom date ranges with charts & tables.
* 📅 **Monthly Breakdowns**: View monthly trends for selected categories & years.
* 🧪 **Test Data Generator**: Populate the DB with realistic sample data for quick testing.
* 🧰 **Data Integrity**: Input validation, duplicate prevention, and category restrictions.
* 🧾 **Operation Logging**: Backend activity logs for debugging & monitoring.
* 🧷 **Unit Testing**: Pytest coverage for core backend functions.

---

## Tech Stack

* **Frontend**: [Streamlit](https://streamlit.io)
* **Backend**: [FastAPI](https://fastapi.tiangolo.com)
* **Database**: MySQL
* **HTTP Testing**: Postman
* **Testing**: Pytest
* **ORM/Driver**: `mysql-connector-python` 
* **Charts**: Streamlit 

> *Why FastAPI?* Auto-generated docs (Swagger & ReDoc), type hints, and async-ready performance.

---

## Screens & Demo

* **My Streamlit App** <img src="assets/screen-main.png" width="800" alt="Streamlit main screen"/>

* **Project Structure** <img src="assets/screen-structure.png" width="800" alt="Project structure"/>

* **Demo Video**
  ▶️ Watch here: **[Demo Video](https://your-demo-link.example)**

> Replace image paths and the demo link with your own.

---

## Project Structure

```text
Expense_Management_System/
│
├── backend/
│   ├── server.py              # FastAPI server logic (APIs for CRUD operations)
│   └── db_helper.py           # SQL database interactions and helpers
│
├── frontend/
│   ├── app.py                  # Core Streamlit app (entry point)
│   ├── add_update_ui.py        # Tab 1: Add / Edit / Delete expenses
│   ├── analytics_category.py   # Tab 2: Category-wise analytics
│   └── analytics_months.py     # Tab 3: Monthly expense trends
│
├── tests/
│   ├── conftest.py             # Pytest setup for imports
│   ├── requirements.txt        # Testing dependencies
│   └── backend/
│       └── test_db_helper.py   # Unit tests for database functions
│
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Project dependencies
└── README.md                   # Project overview
```

---

## Getting Started

### Prerequisites

* Python 3.10+
* MySQL 8+
* pip 

### Environment Variables

Create a `.env` file in the project root (or `backend/` if you prefer) from `.env.example`:

```env
# MySQL
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=expense_manger

# App
API_HOST=127.0.0.1
API_PORT=8000
PAGE_SIZE=5
ALLOWED_CATEGORIES=Food,Rent,Shopping,Entertainment,Other
```

### Setup & Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Initialize the database (table creation):

```sql
CREATE TABLE IF NOT EXISTS expenses (
  id INT AUTO_INCREMENT PRIMARY KEY,
  date DATE NOT NULL,
  category VARCHAR(50) NOT NULL,
  item VARCHAR(255) NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  notes VARCHAR(255),
  UNIQUE KEY uniq_expense (date, category, item, amount)
);
```

#### Launch the Backend

```bash
cd backend
uvicorn api_server:app --reload
```

#### Launch the Frontend (new terminal)

```bash
cd frontend
streamlit run main.py
```

#### Access the App

* Open: [http://localhost:8501](http://localhost:8501)
* API Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## How It Works

1. **MySQL + Python Integration**: Reusable CRUD functions encapsulate DB access.
2. **API Endpoints with FastAPI**: Chosen over Flask for built‑in docs and robust request validation.
3. **Logging**: File + console handlers record all critical operations and errors.
4. **Verification via Postman**: Requests (GET/POST/PUT/DELETE) verified prior to UI wiring.
5. **Streamlit Frontend**: Calls FastAPI endpoints, renders tables and charts.

---

## App Tabs

### 1) Add/Update expense

* View expenses for a chosen date, **5 per page**.
* Shows total entries and total pages.
* **Add**: Enable *Add New Expense* → fill form → submit. Duplicates are blocked.
* **Edit**: Update a record and confirm.
* **Delete**: Select via checkboxes and confirm deletion.

### 2)Analytics by Category 

* Visualize spend by category for a selected **date range**.
* Bar charts + breakdown table (totals & percentages).

### 3) Analytics by Months

* Analyze monthly totals for a chosen **year** and **categories**.
* Charts plus a detailed table view.

---

## 🚀 API Endpoints

| Method | Path                     | Description                         |
|--------|--------------------------|-------------------------------------|
| GET    | `/expenses/{expense_date}` | Get expenses for a specific date     |
| POST   | `/expenses/{expense_date}` | Add or update an expense             |
| POST   | `/analytics/`            | Get category-wise expense analytics |
| GET    | `/monthly_summary/`      | Get monthly expense summary         |

---


**Query params examples**

```http
GET /expenses?date=2024-08-05&page=1&page_size=5
GET /insights/category?start_date=2024-08-01&end_date=2024-08-31
GET /insights/monthly?year=2024&categories=Food,Shopping
```

**Response shape (example)**

```json
{
  "data": [
    {"id": 1, "date": "2024-08-05", "category": "Food", "item": "Lunch", "amount": 250.00, "notes": "-"}
  ],
  "page": 1,
  "page_size": 5,
  "total": 23,
  "total_pages": 5
}
```

---

## Data Model

```python
class Expense(BaseModel):
    date: date
    category: Literal["Food", "Rent", "Shopping", "Entertainment", "Other"]
    item: constr(min_length=1, max_length=255)
    amount: condecimal(max_digits=10, decimal_places=2, gt=0)
    notes: Optional[constr(max_length=255)] = None
```

**Constraints & Integrity**

* Categories restricted to predefined options.
* Duplicate guard on `(date, category, item, amount)`.
* Input validation enforced via Pydantic.

---

## Testing

Run unit tests with Pytest:

```bash
cd backend
pytest -q
```

Seed the database with sample data:

```bash
python seed_test_data.py --start 2024-01-01 --end 2024-12-31 --rows 500
```

---

## Logging & Monitoring

* Central log file at `backend/logs/app.log` (rotating file handler recommended).
* Logs include request metadata, SQL execution, validation errors, and exceptions.

---

## Troubleshooting

* **Swagger UI not showing endpoints**: Ensure you are running `uvicorn api_server:app --reload` from the **backend** folder and `app` is the FastAPI instance name.
* **MySQL connection errors**: Verify host/port/user/password in `.env` and MySQL is running. Test with `mysql -h 127.0.0.1 -u user -p`.
* **CORS / 4xx errors from Streamlit**: Check API base URL in the frontend client and enable CORS in FastAPI middleware.
* **Pagination looks off**: Confirm `PAGE_SIZE=5` and the total count query.

---

## Contributing

Contributions are welcome! Please:

1. Open an issue for bugs/ideas.
2. Fork the repo & create a feature branch.
3. Add/adjust tests where relevant.
4. Open a PR with a clear description and screenshots.

---

## License

This project is licensed under the **MIT License**. See `LICENSE` for details.

---

## Contact

* 📧 **Email**: [Sanakhan23861@gmail.com](mailto:your.email@example.com)
* 🔗 **LinkedIn**: [www.linkedin.com/in/sana-khan23861](https://www.linkedin.com/in/your-handle)

> *Built with ❤️ using Streamlit, FastAPI, and MySQL.*

