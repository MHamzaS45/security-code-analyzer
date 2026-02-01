import os
from dotenv import load_dotenv      # tools to read environment variables
import google.generativeai as genai
from colorama import init, Fore, Style
import sys

# Initialize colorama
init(autoreset=True)

load_dotenv() # Load environment variables from .env file


api_key = os.getenv("API_KEY") # Configure with your own API key from environment variable
genai.configure(api_key=api_key)


model = genai.GenerativeModel("gemini-2.5-flash") # Initialize the model

security_prompt = """
You are a security expert. Analyze this code for security vulnerabilities. Be concise.

For each issue use this exact format:

- --
SEVERITY: [CRITICAL/HIGH/MEDIUM/LOW]
TYPE: [Vulnerability Name]
DESCRIPTION: [One sentence explaining the issue]
IMPACT: [One sentence on potential damage]
FIX: [Code snippet only]
---

Code:
{code}
"""

# Vulnerable code example 1: SQL Injection
vulnerable_code_1 = '''
def get_user(username):
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchone()
'''
# Vulnerable code example 2: Hardcoded credentials
vulnerable_code_2 = '''
DATABASE_PASSWORD = "supersecret123"
API_KEY = "sk-1234567890abcdef"

def connect_db():
    return psycopg2.connect(
        host="localhost",
        password=DATABASE_PASSWORD
    )
'''
# Vulnerable code example 3: Weak cryptography
vulnerable_code_3 = '''
import hashlib

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()
'''


def add_colors_to_output(text):
    """Colours added to classify severity levels in the output."""
    text = text.replace("SEVERITY: CRITICAL", f"SEVERITY: {Fore.RED}{Style.BRIGHT}CRITICAL{Style.RESET_ALL}")
    text = text.replace("SEVERITY: HIGH", f"SEVERITY: {Fore.YELLOW}{Style.BRIGHT}HIGH{Style.RESET_ALL}")
    text = text.replace("SEVERITY: MEDIUM", f"SEVERITY: {Fore.BLUE}{Style.NORMAL}MEDIUM{Style.RESET_ALL}")
    text = text.replace("SEVERITY: LOW", f"SEVERITY: {Fore.GREEN}{Style.DIM}LOW{Style.RESET_ALL}")
    return text



def scan_file(file_path):
    """Scan a provided file and analyze the code for vulnerabilities. """
    try:
        with open(file_path, 'r') as file:
            code = file.read()
        print(f"\n{'=' * 65}")
        print(f"\n{Fore.YELLOW}Scanning {file_path}{Style.RESET_ALL}.....")
        print(f"\n{'=' * 65}")

        # Analyze the code for vulnerabilities
        response = model.generate_content(security_prompt.format(code=code))
        output = add_colors_to_output(response.text)
        print(f"\n{Fore.GREEN} FilePath scanned! {Style.RESET_ALL}\n")
        print(output)

    except FileNotFoundError:
        print(f"{Fore.RED}Error: File {file_path} not found..{Style.RESET_ALL}")


# ============================================================
# Filename verification start
# ============================================================

# Check if a filename was provided
if len(sys.argv) > 1:
    filepath = sys.argv[1]
    print(f"Scanning file: {filepath}\n")
    scan_file(filepath)
else:
    print("Usage: python scaner.py <filepath>")
    print("Example: python scanner.py vulnerable.py")


# ============================================================
# Filename verification end
# ============================================================

