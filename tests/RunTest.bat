setlocal
cd %~dp0\..
set PYTHONPATH=.

python tests\cplusplus.py
python tests\csharp.py
python tests\rust.py
tests\scripts\GenerateProjects_x64.bat

pause