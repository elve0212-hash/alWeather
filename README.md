

[![CI](https://github.com/elve0212-hash/alWeather/actions/workflows/ci.yml/badge.svg)](https://github.com/elve0212-hash/alWeather/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

# Weather CLI

Simple CLI to fetch current weather for a city using wttr.in (no API key required).

Usage

PowerShell:

```powershell
python -m pip install -r requirements.txt
python weather_app.py --city "London"
# or interactive
python weather_app.py
```

Notes

- Uses `wttr.in` JSON endpoint: `https://wttr.in/<city>?format=j1`.
- No API key required. For production usage consider OpenWeatherMap or caching.

## Publishing to PyPI

This repository includes a GitHub Actions workflow that builds and publishes the package to PyPI when a GitHub **Release** is published.

Steps to publish:

1. Create a PyPI API token:
	- Sign in at https://pypi.org
	- Go to Account > API tokens > Add API token
	- Give it a short name (e.g. `allWeather-release`) and appropriate scope (project or account)
	- Copy the token (you will not be able to view it again)

2. Add the token as a GitHub Actions secret:
	- In your repository on GitHub, go to `Settings` → `Secrets and variables` → `Actions`
	- Click `New repository secret`
	- Name: `PYPI_API_TOKEN`
	- Value: paste the PyPI API token

3. Create a Release on GitHub:
	- In the repository, go to `Releases` → `Draft a new release`
	- Choose a tag name like `v0.1.0`, set the release title, and publish the release
	- When the release is published the workflow `.github/workflows/publish.yml` will run and publish the built distributions to PyPI.

You can also create a tag locally and then create the release on GitHub:

```powershell
git tag v0.1.0
git push origin v0.1.0
# Then create the release in the GitHub UI for that tag.
```

Note: The workflow expects a secret named `PYPI_API_TOKEN`. Do not commit tokens to the repository.
