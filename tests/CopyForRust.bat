setlocal
cd %~dp0
cd ..

mkdir target

mkdir target\debug
cp tests\results\Build\DEBUG\CoreLib.dll .\target\debug\.

mkdir target\release
cp tests\results\Build\RELEASE\CoreLib.dll .\target\release\.

pause
