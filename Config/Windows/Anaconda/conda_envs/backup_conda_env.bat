@echo off
ECHO;
ECHO This script will allow you to package an existing conda environment into a suitable environment.yml file
ECHO in the correct folder and the correct format.
ECHO;
ECHO NOTE: This requires the FS_PATH to be set (yours %FS_PATH%)
ECHO;

:ASK
SET /P INPUT="Do you wish to export an environment (Y/N)? "
IF /I %INPUT%==y GOTO YES 
IF /I %INPUT%==Y GOTO YES 
IF /I %INPUT%==n GOTO NO
IF /I %INPUT%==N GOTO NO
ECHO Incorrect input & GOTO ASK

:YES
ECHO;
IF %FS_PATH% == "" GOTO NO_REPO
CALL conda-env list
GOTO GET_ENV_NAME

:GET_ENV_NAME
SET /P ENV_NAME="Which environment do you wish to backup?: "
ECHO;
:: Create the file paths - requires an environment variable named FS_PATH
SET TEMPLATE_DIR=%FS_PATH%\Config\Windows\Anaconda\conda_envs\envs
SET FILE_NAME=%ENV_NAME%.yml
SET FILE_PATH=%TEMPLATE_DIR%\%FILE_NAME%

:: Create the environment files with all info
ECHO Environment File will be available @ %TEMPLATE_DIR%

:: Create the environment file
ECHO Exporting %ENV_NAME% environment file
CALL conda-env export -n %ENV_NAME% --from-history | findstr -v "prefix" > %FILE_PATH%

ECHO;
ECHO Export complete. You may wish to add %FILE_NAME% file
ECHO to version control if not already done.
ECHO;
GOTO END

:NO
ECHO No export at this time
GOTO END

:NO_REPO
ECHO;
ECHO Unable to complete - have you got an FS_PATH Env Variable set? (see fe_envs.bat)
ECHO Currently your env variable for FS_PATH is %FS_PATH%
GOTO END

:END
:: Pause to keep command prompt open to read
ECHO;
PAUSE