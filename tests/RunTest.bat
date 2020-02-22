setlocal
cd %~dp0\..
set PYTHONPATH=.

tests\csharp.py

cd %~dp0\build

REM GenerateProjects_x64.bat

pause