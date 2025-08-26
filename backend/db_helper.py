import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger
from datetime import datetime

logger = setup_logger('db_helper')


@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_manager"
    )

    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()


def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {type(expense_date)}")
    if isinstance(expense_date, str):
        expense_date = datetime.strptime(expense_date, "%Y-%m-%d").date()
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()
        return expenses


def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))


def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )


def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start: {start_date} end: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT category, SUM(amount) as total
               FROM expenses WHERE expense_date
               BETWEEN %s and %s
               GROUP BY category;''',
            (start_date, end_date)
        )
        data = cursor.fetchall()
        return data



def fetch_monthly_expense_summary():
    query = """
        SELECT
            MONTH(expense_date) AS expense_month,
            MONTHNAME(expense_date) AS month_name,
            SUM(amount) AS total
        FROM expenses
        GROUP BY expense_month, month_name
        ORDER BY expense_month;
    """
    with get_db_cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()



if __name__ == "__main__":
   
    pass

