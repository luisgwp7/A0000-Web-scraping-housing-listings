@echo off
set ruta=C:\Users\luisG\AppData\Local\Temp
set log_file=%ruta%\eliminacion_log.txt
set total_archivos=0
set total_peso=0

echo Eliminando archivos en %ruta%...
for /r %ruta% %%i in (*) do (
    set /a total_archivos+=1
    set /a total_peso+=%%~zi
    del /q "%%i"
)

echo Eliminando carpetas en %ruta%...
rd /s /q %ruta% > nul 2>&1

echo Archivos y carpetas eliminados exitosamente.
echo Numero total de archivos eliminados: %total_archivos% > %log_file%
echo Peso total de archivos eliminados: %total_peso% bytes >> %log_file%
