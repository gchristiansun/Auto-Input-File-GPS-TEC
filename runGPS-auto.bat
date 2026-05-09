@echo off
setlocal EnableDelayedExpansion

set "APP=C:\Users\Gregorius Christian\Videos\GPS_Gopi_v3.0\GPS_Gopi_v3.5\GPS_TEC.exe"
@REM Folder ZIP
set "ROOT=E:\rinex"
@REM Folder kerja
set "FOLDER=E:\rinex\gps"
@REM Folder output GPS_TEC.exe
set "OUTROOT=%FOLDER%\output"
@REM Log aplikasi
set "LOG=%FOLDER%\processed.txt"
@REM Log ZIP
set "ZIPLOG=%ROOT%\processed_zip.txt"
@REM Folder extract sementara
set "TEMP_EXTRACT=%ROOT%\temp_extract"

if not exist "%LOG%" type nul > "%LOG%"
if not exist "%ZIPLOG%" type nul > "%ZIPLOG"
if not exist "%TEMP_EXTRACT%" mkdir "%TEMP_EXTRACT%"

:LOOP

@REM Ekstrak ZIP
for %%z in ("%ROOT%\*.zip") do (
    findstr /x /c:"%%~nxz" "%ZIPLOG%" >nul

    if errorlevel 1 (
        echo Extracting %%~nxz ...

        rmdir /s /q "%TEMP_EXTRACT%" 2>nul
        mkdir "%TEMP_EXTRACT%"
        attrib +h "%TEMP_EXTRACT%"

        powershell -command ^
        "Expand-Archive -LiteralPath '%%z' -DestinationPath '%TEMP_EXTRACT%' -Force"

        @REM Ambil file dari folder rinex
        for /r "%TEMP_EXTRACT%" %%r in (*.??o) do (
            if /i "%%~pr" neq "" (
                echo Copying %%~nxr ...
                copy /y "%%r" "%FOLDER%\" >nul
            )
        )

        echo %%~nxz>>"%ZIPLOG%"
    )
)

@REM Proses file rinex
for %%f in ("%FOLDER%\*.??o") do (

    findstr /x /c:"%%~nxf" "%LOG%" >nul

    if errorlevel 1 (

        set "filename=%%~nxf"
        set "name=%%~nf"

        @REM Ambil lokasi
        set "loc=!name:~0,4!"

        @REM Ambil tahun berdasarkan ekstensi
        set "ext=%%~xf"
        set "year=20!ext:~1,2!"

        @REM Buat folder output
        set "outdir=%OUTROOT%\!year!\!loc!"

        if not exist "!outdir!" mkdir "!outdir!"

        echo Processing %%f → !outdir!

        @REM start "" /min /wait "%APP%" %%f auto

        call "%APP%" %%f auto

        timeout /t 2 >nul

        @REM Pindahkan file output ke folder yang sesuai
        move /y "%FOLDER%\*.std" "!outdir!\" >nul 2>&1
        move /y "%FOLDER%\*.cmn" "!outdir!\" >nul 2>&1

        echo %%~nxf>>"%LOG%"
    )
)

timeout /t 60 /nobreak 
cls

goto LOOP