# Log Analyser

A modern desktop application for analysing web server log files.

## Quick Start

### Option 1: Download Release

1. Go to the [Releases](https://github.com/JackHughes03/Log-analyser/releases) page
2. Download the zip
3. Install requirements
4. Run gui.py

### Option 2: Install from Source

```bash
# Clone the repository
git clone https://github.com/JackHughes03/Log-analyser.git

# Install dependencies in requirements.txt
pip install -r requirements.txt
```

## Features

- 🚀 Modern, animated UI built with PySide6
- 📊 Comprehensive log analysis including:
  - Response code distribution
  - IP address tracking with geolocation
  - Most requested files
  - Tools and user agents used
  - Traffic analysis with:
    - Peak hours identification
    - 15-minute interval breakdowns
    - Time period comparisons (Morning/Afternoon/Evening/Night)
    - Average requests per hour
    - Traffic pattern detection
- 🌍 IP Geolocation using ipinfo.io API
- 📝 Detailed report generation
- 💾 Persistent API token storage

## Requirements

If installing from source:
- Python 3.x
- PySide6
- Requests
- Keyring

No additional requirements for the pre-built releases.

## Usage

1. Launch Log Analyser
2. Get an API token from [ipinfo.io](https://ipinfo.io/account/token)
3. Enter your API token in the application
4. Upload a log file
5. Click "Analyse" to start processing
