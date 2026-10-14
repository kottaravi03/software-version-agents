import csv
from pathlib import Path

from packaging.version import InvalidVersion, Version

from version_checker import (
    get_latest_git_version,
    get_latest_python_version,
    get_latest_vscode_version,
)

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "requiredsoftwares.csv"
OUTPUT_FILE = BASE_DIR / "software_version_report.csv"

VERSION_CHECKERS = {
    "python": get_latest_python_version,
    "git": get_latest_git_version,
    "visual studio code": get_latest_vscode_version,
}


def read_required_software(csv_file: Path) -> list[dict[str, str]]:
    """Read and validate software details from the CSV file."""

    with csv_file.open(
        mode="r",
        newline="",
        encoding="utf-8-sig",
    ) as file:
        # Ignore blank lines, including blank lines before the header.
        lines = (line for line in file if line.strip())

        reader = csv.DictReader(lines, skipinitialspace=True)

        if not reader.fieldnames:
            raise ValueError("The CSV file is empty or has no header.")

        # Remove spaces around column names.
        reader.fieldnames = [
            column.strip().lower() for column in reader.fieldnames
        ]

        required_columns = {"sno", "name", "version", "url"}

        if not required_columns.issubset(reader.fieldnames):
            raise ValueError(
                "CSV must contain these columns: "
                "sno, name, version, url"
            )

        software_list = []

        for row in reader:
            # Skip malformed or incomplete rows.
            if any(
                not isinstance(row.get(column), str)
                or not row[column].strip()
                for column in required_columns
            ):
                print(f"Skipping incomplete CSV row: {row}")
                continue

            software_list.append(
                {
                    column: row[column].strip()
                    for column in required_columns
                }
            )

        return software_list


def check_software(software: dict[str, str]) -> dict[str, str]:
    """Check the installed or recorded version against the latest version."""

    name = software["name"]
    current_version = software["version"]
    checker = VERSION_CHECKERS.get(name.lower())

    latest_version = ""
    status = ""

    try:
        if checker is None:
            status = "Unsupported software"
        else:
            latest_version = checker()

            if Version(current_version) < Version(latest_version):
                status = "Update available"
            else:
                status = "Up to date"

    except (InvalidVersion, ValueError) as error:
        status = f"Version error: {error}"

    except Exception as error:
        status = f"Check failed: {error}"

    return {
        "sno": software["sno"],
        "name": name,
        "current_version": current_version,
        "latest_version": latest_version,
        "status": status,
        "url": software["url"],
    }


def main() -> None:
    """Check all listed software and save a CSV report."""

    if not INPUT_FILE.exists():
        print(f"Error: CSV file not found: {INPUT_FILE}")
        return

    try:
        software_list = read_required_software(INPUT_FILE)
    except (OSError, ValueError, csv.Error) as error:
        print(f"Error reading CSV: {error}")
        return

    if not software_list:
        print("No valid software records found in the CSV file.")
        return

    report = []

    print("Checking software versions...\n")

    for software in software_list:
        result = check_software(software)
        report.append(result)

        print(
            f"{result['name']}: "
            f"{result['current_version']} -> "
            f"{result['latest_version'] or 'Unavailable'} "
            f"({result['status']})"
        )

    fieldnames = [
        "sno",
        "name",
        "current_version",
        "latest_version",
        "status",
        "url",
    ]

    try:
        with OUTPUT_FILE.open(
            mode="w",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(report)

        print(f"\nReport saved to: {OUTPUT_FILE}")

    except OSError as error:
        print(f"Error saving report: {error}")


if __name__ == "__main__":
    main()
