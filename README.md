# Software Version Finder Agent

A Python tool that checks the latest versions of supported software and generates a CSV report showing whether updates are available.

## Features

- Reads software details from `requiredsoftwares.csv`.
- Checks the latest versions of Python, Git, and Visual Studio Code.
- Compares current and latest versions.
- Identifies available updates.
- Generates `software_version_report.csv`.
- Uses Python, `uv`, and public version endpoints. No paid AI API key required.

## Requirements

- Python 3.13 or newer
- `uv`
- Internet connection

## Project Structure

```text
software-version-agent/
├── main.py
├── version_checker.py
├── requiredsoftwares.csv
├── software_version_report.csv
├── pyproject.toml
├── uv.lock
├── README.md
└── .gitignore
```

`software_version_report.csv` is generated when the program runs.

## Input CSV Format

The `requiredsoftwares.csv` file must contain these columns:

```csv
sno,name,version,url
1,Python,3.13.0,https://www.python.org/
2,Git,2.40.0,https://git-scm.com/
3,Visual Studio Code,1.90.0,https://code.visualstudio.com/
```

## Setup

Install Python and `uv` on your computer.

Clone or download this repository, then open a terminal in the project directory.

Install the project dependencies:

```powershell
uv sync
```

## Run

```powershell
uv run main.py
```

The program checks the listed software and generates `software_version_report.csv`.

## Supported Software

- Python
- Git
- Visual Studio Code

## Notes

- An internet connection is required.
- Public endpoints may occasionally be unavailable or rate-limited.
- The version in the input CSV is the recorded version you want to compare; it is not automatically detected from the installed software.
- This project does not require an Anthropic API key.