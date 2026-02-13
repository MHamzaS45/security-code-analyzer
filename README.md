# Security Code Analyzer

An **AI-powered CLI code analyzer** that uses Google's Gemini model to parse through python files for security issues. Get structured, severity-colored reports for SQL injection, hardcoded credentials, weak cryptography, command injection, and more.

---

## Algorithm 

<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/ca2a14bb-512c-4649-a59e-b00e891c43a1" />


## Features

- **AI-driven analysis** — Uses Gemini 2.5 Flash to identify security vulnerabilities in your code
- **Structured output** — Each finding includes:
  - **SEVERITY** — CRITICAL, HIGH, MEDIUM, or LOW
  - **TYPE** — Vulnerability name (e.g., SQL Injection, Hardcoded Credentials)
  - **DESCRIPTION** — Brief explanation of the issue
  - **IMPACT** — Potential damage
  - **FIX** — Suggested code snippet to remediate
- **Color-coded severity** — Red (Critical), Yellow (High), Blue (Medium), Green (Low) in the terminal
- **File-based scanning** — Pass any source file as a command-line argument

---

## Project Structure

```
security-scanner/
├── scanner.py          # Main scanner: loads code, calls Gemini, prints colored report
├── vulnerable.py       # Sample file with intentional vulnerabilities (for testing)
├── .env                # Your API key (create this, not committed for safety reasons)
├── .gitignore
└── README.md
```

## Requirements

- Python 3.8+
- [Google Generative AI](https://pypi.org/project/google-generativeai/) (Gemini API)
- [python-dotenv](https://pypi.org/project/python-dotenv/) — load API key from `.env`
- [colorama](https://pypi.org/project/colorama/) — colored terminal output (especially on Windows)

---

## Setup

### 1. Install dependencies

```bash
pip install google-generativeai python-dotenv colorama
```

Or with a requirements file (create `requirements.txt`):

```
google-generativeai>=0.8.0
python-dotenv>=1.0.0
colorama>=0.4.6
```

Then:

```bash
pip install -r requirements.txt
```


### 2. Get a Gemini API key

1. Go to Google AI Studio (or the Gemini API key page).
2. Create an API key and copy it.


### 3. Configure the API key in the environment variable

Create a `.env` file in the project root:

```env
API_KEY=your_actual_api_key_here  # Paste the API key received
```

**Important:** In `scanner.py`, the key must be read using the **variable name** you use in `.env`, for example:

```python
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
```

If your `.env` uses a different variable name, use that same name in `os.getenv("YOUR_VAR_NAME")`. 

[!NOTE](Never commit your real API key or put it directly in source code.)

---

## Usage

Scan a file by passing its path as an argument:

```bash
python scanner.py path/to/your/file.py
```

**Example — scan the included sample file:**
```bash
python scanner.py vulnerable.py
```

The provided sample `vulnerable.py` contains intentional issues (e.g., SQL injection, hardcoded secrets, weak MD5 hashing, command injection) so you can understand how the scanner reports findings. 

**Without arguments:**

```bash
python scanner.py
```

Prints usage: `python scanner.py <filepath>`.

---

## Example Output

The scanner prints a header for the file being scanned, then one block per finding, for example:

```
============================================================
Scanning vulnerable.py.....
============================================================

SEVERITY: CRITICAL
TYPE: SQL Injection
DESCRIPTION: User input is concatenated into the query string.
IMPACT: Attackers can execute arbitrary SQL.
FIX: [suggested parameterized query code]
---
...
```

Severity levels are colorized in the terminal. (Critical=red, High=yellow, Medium=blue, Low=green .).

---

## Security Notes:

- Keep your `.env` and API keys out of version control (`.gitignore` already includes `.env`).
- Do not paste production credentials or real secrets into code you scan; use sample or test data when possible.

---

## License

The code is free to use and modify for your own projects.
