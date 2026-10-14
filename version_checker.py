
import re

import requests
from packaging.version import Version


def get_latest_python_version() -> str:
    """Get the latest stable Python release version."""
    url = "https://www.python.org/api/v2/downloads/release/"

    response = requests.get(
        url,
        params={"is_published": "true"},
        timeout=30,
    )
    response.raise_for_status()

    versions = []

    for release in response.json():
        name = release.get("name", "")
        match = re.fullmatch(r"Python (\d+\.\d+\.\d+)", name)

        if match:
            versions.append(Version(match.group(1)))

    if not versions:
        raise ValueError("No stable Python releases were found.")

    return str(max(versions))


def get_latest_git_version() -> str:
    """Get the latest stable Git release version."""
    url = "https://mirrors.edge.kernel.org/pub/software/scm/git/"

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    versions = re.findall(
        r'href="git-(\d+\.\d+\.\d+)\.tar\.gz"',
        response.text,
    )

    if not versions:
        raise ValueError("No Git release versions were found.")

    return str(max(Version(version) for version in versions))


def get_latest_vscode_version() -> str:
    """Get the latest stable Visual Studio Code version."""
    url = (
        "https://update.code.visualstudio.com/api/update/"
        "win32-x64-user/stable/latest"
    )

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    data = response.json()
    version = data.get("productVersion")

    if not version:
        raise ValueError("VS Code version was not found in the API response.")

    return version


def main() -> None:
    """Display the latest stable versions of supported software."""
    checkers = {
        "Python": get_latest_python_version,
        "Git": get_latest_git_version,
        "Visual Studio Code": get_latest_vscode_version,
    }

    for software_name, checker in checkers.items():
        try:
            version = checker()
            print(f"{software_name}: {version}")
        except (requests.RequestException, ValueError) as error:
            print(f"{software_name}: Failed to check version ({error})")


if __name__ == "__main__":
    main()
