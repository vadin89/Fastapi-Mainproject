
import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


# پیدا کردن فایل .env در پوشه اصلی پروژه
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)

# خواندن تنظیمات اتصال
DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
DB_DRIVER = os.getenv("DB_DRIVER")

if not all([DB_SERVER, DB_NAME, DB_DRIVER]):
    raise RuntimeError(
        "تنظیمات اتصال دیتابیس در فایل .env کامل نیست."
    )

# ساخت رشته اتصال با Windows Authentication
connection_string = (
    f"DRIVER={{{DB_DRIVER}}};"
    f"SERVER={DB_SERVER};"
    f"DATABASE={DB_NAME};"
    "Trusted_Connection=yes;"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
    "Connection Timeout=10;"
)

# تبدیل رشته اتصال به فرم قابل استفاده توسط SQLAlchemy
connection_url = (
    "mssql+pyodbc:///?odbc_connect="
    + quote_plus(connection_string)
)

# ساخت موتور اتصال
engine = create_engine(
    connection_url,
    pool_pre_ping=True,
    pool_recycle=1800,
)


def test_connection():
    """بررسی اتصال و دریافت نام سرور و دیتابیس."""

    try:
        with engine.connect() as connection:
            result = connection.execute(
                text(
                    "SELECT @@SERVERNAME AS server_name, "
                    "DB_NAME() AS database_name"
                )
            )

            row = result.mappings().one()

            return {
                "success": True,
                "server": row["server_name"],
                "database": row["database_name"],
            }

    except SQLAlchemyError:
        return {
            "success": False,
            "message": (
                "اتصال برقرار نشد. تنظیمات و مجوزهای SQL Server "
                "را بررسی کنید."
            ),
        }

def get_employee_by_code(p_code: str):
    """دریافت اطلاعات پرسنل بر اساس کد پرسنلی."""

    query = text("""
        SELECT
            ID,
            P_Code,
            F_Name,
            L_Name,
            Sex,
            NID,
            B_Date
        FROM dbo.Employees
        WHERE P_Code = :p_code
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"p_code": p_code}
        )

        employee = result.mappings().first()

        if employee is None:
            return None

        return dict(employee)

