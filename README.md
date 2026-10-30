# Ethical OSINT Toolkit

This project provides a professional, mobile-friendly OSINT interface built using Python and Streamlit.

## Features
- Username checking across public profiles
- Domain intelligence (DNS and WHOIS)
- Email breach lookup (with HIBP API key if configured)
- Metadata extraction from images and PDF files
- Mobile-friendly responsive interface

## Project structure
- `main.py` — classic CLI version
- `app.py` — modern Streamlit web interface
- `modules/` — OSINT logic modules
- `config.json` — configuration
- `requirements.txt` — dependencies

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the CLI version

```bash
python main.py --username octocat
python main.py --domain github.com
python main.py --email someone@example.com
python main.py --file ./sample.jpg
```

## Run the mobile-friendly web version

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## HIBP Setup (optional)

For email breach checks, set the API key:

```bash
export HIBP_API_KEY="YOUR_API_KEY"
```

On Windows PowerShell:

```powershell
$env:HIBP_API_KEY="YOUR_API_KEY"
```

## Disclaimer
This tool is intended for authorized or educational use only. It must not be used to violate laws, privacy rights, or platform terms.

## GitHub repository
https://github.com/dbo0m/ethical-osint-toolkit

## Notes
- Some public platforms may block automated requests.
- Some metadata may contain sensitive fields such as GPS or device details.
- Handle all results with care and legal compliance.

