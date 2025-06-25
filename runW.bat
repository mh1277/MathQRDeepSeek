@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8

echo.
echo ***************************************
echo * mathword - تدقيق الوثائق الرياضية *
echo ***************************************
echo.

:: التحقق من تثبيت بايثون
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo خطأ: بايثون غير مثبت!
    pause
    exit
)

:: تثبيت المكتبات المطلوبة
pip install python-docx requests python-dotenv > nul 2>&1

:: تشغيل البرنامج
python mathword.py %*

:: إذا حدث خطأ
if %errorlevel% neq 0 (
    echo.
    echo حدث خطأ أثناء التشغيل
    echo تأكد من وجود الملفات التالية:
    echo   - mathword.py
    echo   - input.docx (أو حدد ملف آخر)
    echo.
    pause
)