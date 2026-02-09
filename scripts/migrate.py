import os
import requests
import logging
from pathlib import Path

print("=== FOXPRO → CONSOLE C# (GROQ) ===")

# ================================
# LOGGING
# ================================
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s"
)
log = logging.getLogger("foxpro-groq")

# ================================
# CONFIG
# ================================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not set")

MODEL = "llama-3.1-8b-instant"
API_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

FOXPRO_DIR = Path(".")
OUT_DIR = Path("dotnet_out")
OUT_DIR.mkdir(exist_ok=True)

EXTENSIONS = [".prg"]

# ================================
# CLEAN FOXPRO
# ================================
def clean_text(s):
    return "".join(c for c in s if c == "\n" or (32 <= ord(c) <= 126))

# ================================
# GROQ CALL
# ================================
def groq_call(prompt):
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "max_tokens": 2048
    }

    r = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

# ================================
# CONVERT FOXPRO → CONSOLE C#
# ================================
def convert_foxpro(code):
    prompt = f"""
You are converting Visual FoxPro code into C# CONSOLE APPLICATION code.

TARGET PLATFORM:
- .NET Console
- Linux compatible
- OnlineGDB compatible

ABSOLUTE RULES (MANDATORY):
- Output ONLY console-based C#
- Use Console.ReadLine() and Console.WriteLine()
- DO NOT use System.Windows.Forms
- DO NOT use Microsoft.VisualBasic
- DO NOT use MessageBox
- DO NOT use InputBox
- DO NOT invent GUI logic

MAPPING RULES:
- INPUT var      → Console.ReadLine()
- ? output       → Console.WriteLine()
- FoxPro numeric → double
- DO CASE        → if / else if / else
- IF / ELSE      → if / else

GENERAL:
- Preserve logic exactly
- Line-by-line conversion
- No refactoring
- No markdown
- No explanations
- Output ONLY valid C# code

FOXPRO CODE:
{code}
"""
    return groq_call(prompt)

# ================================
# MAIN
# ================================
files = []
for ext in EXTENSIONS:
    files.extend(FOXPRO_DIR.rglob(f"*{ext}"))

log.info("FoxPro files found: %d", len(files))

for f in files:
    log.info("Converting %s", f.name)

    fox = clean_text(f.read_text(errors="ignore"))
    cs = convert_foxpro(fox)

    out_file = OUT_DIR / (f.stem + ".cs")
    out_file.write_text(cs, encoding="utf-8")

    log.info("Saved → %s", out_file)

print("=== CONVERSION COMPLETE ===")
