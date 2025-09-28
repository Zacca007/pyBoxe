# PyBoxe

A Python application for searching and exporting Italian boxing athlete data from the FPI (Federazione Pugilistica Italiana) website.

## Features

- **Athlete Search**: Search for boxers based on match count range and various filters
- **Filter Options**: Filter by committee, qualification, and weight category
- **Excel Export**: Export search results to formatted Excel files
- **Dual Interface**: Choose between GUI (Tkinter) or command-line interface
- **Statistics Integration**: Automatically fetches win/loss/draw statistics for each athlete

## Installation

1. Clone the repository
2. Install required dependencies:
   ```bash
   pip install requests beautifulsoup4 openpyxl
   ```

## Usage

### GUI Mode (Default)
```bash
python src/main.py
```

### Console Mode
```bash
python src/main.py console
```

### GUI Features
- Set minimum and maximum match counts
- Select optional filters (committee, qualification, weight)
- Enter output filename
- Click "Search athletes" to start the process

### Console Features
- Interactive prompts for search parameters
- Optional filter selection with numbered menus
- Real-time progress feedback

## Project Structure

```
src/
├── core/                   # Core business logic
│   ├── athlete.py         # Athlete data model
│   ├── client.py          # HTTP client for FPI website
│   ├── parser.py          # HTML parsing utilities
│   ├── service.py         # High-level service layer
│   └── writer.py          # Excel export functionality
├── interface/
│   └── window.py          # Tkinter GUI interface
└── main.py                # Application entry point
```

## Output

The application generates Excel files with the following columns:
- Name
- Age
- Club
- Total Matches
- Wins
- Losses
- Draws

## Requirements

- Python3
- requests
- beautifulsoup4
- openpyxl
- tkinter (usually included with Python)

## Notes

- The application fetches data from the official FPI website
- Search operations may take time due to network requests
- Excel files are saved in the same directory as the script
