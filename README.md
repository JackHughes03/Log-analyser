# Log Analyser

A modern desktop application for analysing web server log files.

## Quick Start

### Option 1: Download Release

1. Go to the [Releases](https://github.com/yourusername/log-analyser/releases) page
2. Download the latest version for your platform:
   - `LogAnalyser-Mac.dmg` for MacOS
3. Run the installer

### Option 2: Install from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/log-analyser.git

# Install dependencies
pip install PySide6 requests keyring
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

## Features in Detail

### Response Codes Analysis
- Track HTTP response codes distribution
- Identify common error codes
- Monitor success rates

### IP Analysis
- Analyse visitor IPs with country and ISP information
- Track frequent visitors
- Identify potential security issues

### File Request Analysis
- Monitor most requested resources
- Track access patterns
- Identify popular content

### Tools Analysis
- Identify user agents and tools
- Track browser usage
- Monitor bot activity

### Traffic Analysis
- View peak traffic hours (24-hour format)
- Compare traffic across different periods:
  - Morning (6AM-11AM)
  - Afternoon (12PM-5PM)
  - Evening (6PM-11PM)
  - Night (12AM-5AM)
- Calculate average requests per hour
- Identify busiest periods
- Track traffic patterns and trends

## Screenshots

Screenshots on the way

## Versioning

- **Latest Release**: v0.0.1 Pre-release
- **Release Date**: Unplanned
- [View Changelog](https://github.com/yourusername/log-analyser/blob/main/CHANGELOG.md)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.