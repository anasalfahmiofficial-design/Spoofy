# Spoofy 🕵️‍♂️

**Spoofy** is an advanced file extension spoofing detector. Out of the box, it runs a blazing-fast local engine to detect disguised binary files. For power users, it offers an optional AI-driven engine to deeply analyze scripts and text files.

## 🌟 Features

### 1. Core Engine (No Setup Required) ⚡
* **Hex Signature Matching:** Instantly detects if a binary file (like an `.exe` disguised as a `.jpg`) is spoofed by verifying its Magic Numbers against a built-in database.
* **100% Offline & Private:** Your files are scanned locally on your machine.

### 2. AI Engine (Optional Power-Up) 🧠
* **Deep Content Analysis:** By adding a free Gemini API Key, Spoofy gains the ability to read and understand code. It can detect malicious scripts (e.g., Python code hiding inside a `.txt` or `.sh` file).
* **Smart Predictions:** Predicts the true programming language or format of plain text files that evade traditional binary scans.

### 3. Cross-Platform 🌍
* Works flawlessly on **Windows, Linux, and macOS**. Built with `pathlib` to handle file paths dynamically across any operating system.

## ⚙️ Prerequisites
* Python 3.8+
* Git
* *Optional:* A Google Gemini API Key (Only if you want to unlock the AI Engine).

## 🚀 Installation

Choose your operating system below and run the commands in your terminal or command prompt:

### 🐧 For Linux / macOS (Terminal)
```bash
# 1. Clone the repository
git clone [https://github.com/anasalfahmiofficial-design/Spoofy.git](https://github.com/anasalfahmiofficial-design/Spoofy.git)

# 2. Enter the directory
cd Spoofy

# 3. Install required libraries
pip3 install google-genai python-dotenv
```
🐧 For Windows (cmd) 
```cmd
:: 1. Clone the repository git clone OR press the green CODE button in above
[https://github.com/anasalfahmiofficial-design/Spoofy.git](https://github.com/anasalfahmiofficial-design/Spoofy.git) 

:: 2. Enter the directory
 cd Spoofy

:: 3. Install required libraries
 pip install google-genai python-dotenv
```


💻 Usage On Linux/macOS:
```bash
python3 Spoofy.py -f suspicious_file.jpg
```
On Windows:
```cmd
python Spoofy.py -f suspicious_file.jpg
```
Advanced Mode (Activate the AI) To supercharge Spoofy with AI capabilities: 
Get a free API key from Google AI Studio. Create a file named .env in the Spoofy folder. Add your key like this: GEMINI_API_KEY=your_api_key_here

To use the AI deep scan, you need to create a .env file. To avoid encoding issues on Windows, run this exact command in your terminal:
```cmd
Set-Content -Path .env -Value "GEMINI_API_KEY=your_api_key_here" -Encoding ascii
```

4. Run the tool normally. The AI engine will automatically activate!

## 🛡️ Disclaimer
This tool was developed for educational and cybersecurity analysis purposes. Ensure you have the proper authorization before scanning files on systems you do not own.
