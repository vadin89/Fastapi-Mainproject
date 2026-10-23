
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import SQLAlchemyError

from app.database import test_connection, get_employee_by_code


app = FastAPI(
    title="Employees API",
    description="سامانه جست‌وجو و نمایش اطلاعات پرسنل",
    version="1.0.0",
)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static",
)



@app.get("/", include_in_schema=False)
def home():
    return FileResponse(STATIC_DIR / "index.html")



@app.get("/db-test")
def database_test():
    result = test_connection()

    if not result["success"]:
        raise HTTPException(
            status_code=503,
            detail=result["message"],
        )

    return result


@app.get("/employees/{p_code}")
def find_employee(p_code: str):
    try:
        employee = get_employee_by_code(p_code)

        if employee is None:
            raise HTTPException(
                status_code=404,
                detail="پرسنلی با این کد پیدا نشد.",
            )

        return employee

    except HTTPException:
        raise

    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="خطا در ارتباط با دیتابیس.",
        )
