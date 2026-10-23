
const searchForm = document.getElementById("search-form");
const codeInput = document.getElementById("p-code");
const searchButton = document.getElementById("search-button");
const buttonText = document.getElementById("button-text");
const messageBox = document.getElementById("message");
const employeeSection = document.getElementById("employee-section");
const clearButton = document.getElementById("clear-button");

function showMessage(message, type = "error") {
    messageBox.textContent = message;
    messageBox.className = `message ${type}`;
    messageBox.hidden = false;
}

function hideMessage() {
    messageBox.hidden = true;
    messageBox.textContent = "";
}

function setText(id, value) {
    document.getElementById(id).textContent =
        value === null || value === undefined || value === ""
            ? "ثبت نشده"
            : String(value);
}

function displayEmployee(employee) {
    const fullName =
        `${employee.F_Name || ""} ${employee.L_Name || ""}`.trim();

    setText("full-name", fullName || "بدون نام");
    setText("employee-code", employee.P_Code);
    setText("employee-id", employee.ID);
    setText("first-name", employee.F_Name);
    setText("last-name", employee.L_Name);
    setText("sex", employee.Sex);
    setText("nid", employee.NID);
    setText("birth-date", employee.B_Date);

    document.getElementById("avatar").textContent =
        (employee.F_Name || "پ").charAt(0);

    employeeSection.hidden = false;
}

searchForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const pCode = codeInput.value.trim();

    if (!pCode) {
        showMessage("لطفاً کد پرسنلی را وارد کنید.");
        return;
    }

    hideMessage();
    employeeSection.hidden = true;
    searchButton.disabled = true;
    buttonText.textContent = "در حال جست‌وجو...";

    try {
        const response = await fetch(
            `/employees/${encodeURIComponent(pCode)}`
        );

        if (response.status === 404) {
            showMessage("پرسنلی با این کد پیدا نشد.");
            return;
        }

        if (response.status === 503) {
            showMessage("ارتباط با دیتابیس برقرار نیست. لطفاً بعداً تلاش کنید.");
            return;
        }

        if (!response.ok) {
            showMessage("در دریافت اطلاعات خطایی رخ داد.");
            return;
        }

        const employee = await response.json();

        displayEmployee(employee);
        showMessage("اطلاعات پرسنل با موفقیت دریافت شد.", "success");

    } catch (error) {
        showMessage(
            "ارتباط با سرور برقرار نشد. از اجرای برنامه مطمئن شوید."
        );
    } finally {
        searchButton.disabled = false;
        buttonText.textContent = "جست‌وجو";
    }
});

clearButton.addEventListener("click", function () {
    employeeSection.hidden = true;
    hideMessage();
    codeInput.value = "";
    codeInput.focus();
});
