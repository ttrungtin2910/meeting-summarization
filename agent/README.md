# AI Agent

## 1. Requirements
- Python 3.10.11:
    - Download python: [Window Installer (64-bit)](https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe)
    - Run the installer and check "**Add Python to PATH**" before clicking **Install Now**.
- **.env**:
    - Before running the module, ensure that the correct **.env** file is available. If the file does not exist, download it from the confluence.
## 2. Navigate to the Project Folder
Before setting up the environment, navigate to the project directory where the llm_engine is located
```bash
cd E:\path\to\ai_agent
```
## 3. Setup Instructions
### 3.1. Install poetry package:
```bash
pip install poetry
```
### 3.2. Install Dependencies:
```bash
poetry install
```
## 4. Running the Module
```bash
poetry run uvicorn main:app --reload
```
# If use postgresql locally, install PGVector for postgreSQL server (Windows)

## 1. Install C/C++ Extension for VS Code

First you need to install the C/C++ extension for VS Code.

Open a new window in VS Code and select **Get started with C++**. On the right side of VS Code, you will see a command. Copy that command and run it in **Command Prompt (as Administrator)** — without quotes — like this:

```bash
winget install Microsoft.VisualStudio.2022.BuildTools --force --override "--wait --passive --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Component.VC.Tools.x86.x64 --add Microsoft.VisualStudio.Component.Windows11SDK.22000"
```

## 2. Make Sure Developer Command Prompt is Installed

Open the Developer Command Prompt for Visual Studio by typing `developer` in the Windows Start menu.

Check your MSVC installation by typing:

```
cl
```

in the Developer Command Prompt for VS. You should see a copyright message with version and usage.

You can also refer to the official site for installing the MSVC C++ toolset.

## 3. Clone and Build `pgvector`

To install `pgvector`, run this command in Git Bash:

```
git clone https://github.com/pgvector/pgvector.git
```

Then, open **Command Prompt as Administrator**, change directory to the `pgvector` folder:

```
cd pgvector
```

Run the following command to configure the Visual Studio build environment:

```
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
```

**NOTE**: The exact path may vary depending on your Visual Studio version and edition.

Next, set the PostgreSQL installation root:

```
set "PGROOT=C:\Program Files\PostgreSQL\15"
```

**NOTE**: This path may differ depending on where PostgreSQL is installed on your system.

Then run the build commands:

```
nmake /F Makefile.win
nmake /F Makefile.win install
```

## 4. Enable the Extension in PostgreSQL

Run the following command inside your PostgreSQL database:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Check the function directory to ensure the extension exists.


# Postgresql migration
```bash
poetry run alembic upgrade heads
```
If there are errors with existed enum, drop the enum in sql query, see the error message
```sql
drop type if exists [enum_name]
```