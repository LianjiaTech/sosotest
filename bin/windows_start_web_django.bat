@echo off
for /f "tokens=1,2 delims==" %%i in (windows.ini) do (
if "%%i"=="pythonroot" set pythonroot=%%j
if "%%i"=="pythonroot_test" set pythonroot_test=%%j
if "%%i"=="releaseSubDIR" set releaseSubDIR=%%j
)
%pythonroot% ../AutotestWebD/manage.py runserver 0.0.0.0:80
pause