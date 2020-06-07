setlocal
cd %~dp0\..
set PYTHONPATH=.

tests\csharp.py
tests\scripts\GenerateProjects_x64.bat


pause