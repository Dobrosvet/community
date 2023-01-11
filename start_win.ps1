Write-Output "Скрипт предназанчен для Windows PowerShell"

Set-Location .\backend

Write-Output "Создание виртуального окружения"
python -m venv .venv

Write-Output "Активация окружения $pwd\backend\.venv\Scripts\activate.ps1"
.\.venv\Scripts\activate.ps1

Write-Output "Установка зависимостей"
pip install -r requirements.txt

Write-Output "Сборка"
python build.py

Write-Output "Запуск скрипта"
python index.py

Write-Host "Для выхода нажмите любую клавишу"
$host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") | out-null