@echo off
ECHO;
ECHO This script will setup a new python conda environment with the default packages as described by the ENV.yml file
ECHO These files are located in the conda_envs folder in the config in Orestis' Funspace
ECHO;
ECHO Script can be executed without command line arguments, then user will be prompted for inputs.
ECHO Alternatively, provide arguments as (arguments order is important):
ECHO "install_conda_env.bat
ECHO    - environment name, e.g. py38

:: Fetch env name
:: This allows calling with parameters provided in command line
SET "ENV_NAME=%~1"
IF NOT "%ENV_NAME%"=="" GOTO YES
GOTO :YES_CHECK

:YES_PROMPT
SET /P INPUT="Do you wish to install a new environment (Y/N)?: "
:YES_CHECK
IF "%INPUT%" == "" GOTO YES_PROMPT

IF /I %INPUT%==y GOTO YES
IF /I %INPUT%==n GOTO NO
ECHO Incorrect input & GOTO YES_PROMPT

:YES
ECHO;
IF %FS_PATH% == "" GOTO NO_CODE_ENV_VARS_SET
GOTO GET_ENV_NAME

:GET_ENV_NAME
SET TEMPLATE_DIR=%FS_PATH%\Config\Windows\Anaconda\conda_envs\envs
ECHO Available templates:
CALL DIR /B %TEMPLATE_DIR%\*yml /A-D
ECHO;
ECHO Existing environments:
CALL conda-env list

:: Fetch env name if missing
GOTO ENV_CHECK
:ENV_PROMPT
SET /P ENV_NAME="Which environment do you want to install (N to quit)? : "
:ENV_CHECK
if "%ENV_NAME%"=="" goto :ENV_PROMPT

:: Exit if N or n
IF /I %ENV_NAME%==n GOTO NO

:: Get the environment yml from the config folder
SET ENV_YML=%TEMPLATE_DIR%\%ENV_NAME%.yml
IF NOT EXIST %ENV_YML% GOTO NO_YML

:: Remove existing one if it exists first
ECHO;
ECHO Remove existing %ENV_NAME% if it exists first
ECHO;
CALL conda-env remove -n %ENV_NAME%

:: Create the conda environment
ECHO;
ECHO Asking Conda to create the %ENV_YML% environment
CALL conda-env create --file %ENV_YML% --prefix C:\Anaconda3\envs\%ENV_NAME%
CALL conda install conda-build --y

:: Retrieve python version from yml file and use it to map to the Numpy version
:: Note - this is python=3.10 => python310, python=3.6 => python36 etc and only works with 3.* environments
SETLOCAL EnableDelayedExpansion
FOR /F "tokens=2 delims=." %%a in ('FINDSTR /I "python=3" %ENV_YML%') DO (
    SET NUMPY_VERSION=python3%%a
    ECHO Parsed the environment yml file to arrive at a numpy onetick dependency of %NUMPY_VERSION%
    SET NUMPY_PATH=C:\omd\one_tick\bin\numpy\!NUMPY_VERSION!
)
ECHO;
IF EXIST !NUMPY_PATH! (
    ECHO Adding the Onetick Numpy API to %ENV_NAME%
    CALL conda develop !NUMPY_PATH! -n %ENV_NAME%
) ELSE (
    ECHO !NUMPY_PATH! does not exist. Check if installed Onetick library supports
    ECHO python version hard-coded in %ENV_YML% file.
)
ECHO;
SETLOCAL DisableDelayedExpansion

ECHO;
ECHO Adding the FinancialEngineering Python folder to %ENV_NAME%
ECHO;
CALL conda develop %FS_PATH%\Python -n %ENV_NAME%

ECHO;
ECHO This script no longer attempts to update all modules after install
ECHO If you wish to update all of the environment (using conda dependency management)
ECHO call conda update --all --yes --name %ENV_NAME%
ECHO;

GOTO ENV_CREATED

:NO_YML
ECHO No environment.%ENV_NAME%.yml file found.
GOTO GET_ENV_NAME

:ENV_CREATED
ECHO;
ECHO Finished creating %ENV_NAME%
ECHO;
GOTO END

:NO
:: Chose no install
ECHO;
ECHO You have chosen not to install a new environment
GOTO END

:NO_CODE_ENV_VARS_SET
ECHO;
ECHO Unable to complete, this requires a
ECHO FS_PATH environment variable (yours %FS_PATH%).
ECHO see fe_envs.bat
GOTO END

:END
:: Pause to keep command prompt open to read
:: Skip pause if nopause argument has been provided
ECHO;
IF "%~1"=="" PAUSE