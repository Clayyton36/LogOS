@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\activate.bat" (
    echo Ambiente nao encontrado nesta pasta.
    echo Siga as instrucoes de instalacao antes de usar este atalho:
    echo   python -m venv .venv
    echo   .venv\Scripts\activate
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat
python main.py

if errorlevel 1 (
    echo.
    echo O LogOS foi fechado com um erro. Veja a mensagem acima.
    pause
)
