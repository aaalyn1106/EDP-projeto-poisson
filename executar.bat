@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Criando o ambiente Python...
    py -3 -m venv .venv
    if errorlevel 1 goto erro
)

echo Conferindo as bibliotecas do projeto...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto erro

echo Executando o projeto...
".venv\Scripts\python.exe" main.py
if errorlevel 1 goto erro

pause
exit /b 0

:erro
echo.
echo A execucao falhou. Confira a mensagem acima.
pause
exit /b 1