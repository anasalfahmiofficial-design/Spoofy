import os
import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dotenv import load_dotenv
from google import genai

# Load environment variables from the .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

class SignatureDB:
    """Database for binary file digital signatures (Magic Numbers)."""
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.signatures = self._load_db()
        # Determine the maximum byte length to read from file headers
        self.max_bytes = max((len(s['hex']) // 2 + s.get('offset', 0) for s in self.signatures), default=32)

    def _load_db(self) -> List[Dict]:
        if not self.db_path.exists():
            return []
        with open(self.db_path, 'r', encoding='utf-8') as f:
            return json.load(f).get("signatures", [])

class FileAnalyzer:
    """Dual-engine analysis: Hex Signatures + AI Content Inspection."""
    def __init__(self, db: SignatureDB):
        self.db = db
        self.client = genai.Client(api_key=API_KEY) if API_KEY else None

    def _predict_with_ai(self, file_path: Path) -> Optional[str]:
        """Leverages AI to analyze the content of scripts and text files."""
        if not self.client:
            return None
        try:
            # Read a limited sample to prevent memory issues with massive files
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                snippet = f.read(2000) 
            
            if not snippet.strip():
                return None

            # Call the generative AI model
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=f"Analyze the content and identify its most likely file extension. Return ONLY the exact extension (e.g., .py, .sh, .json) without any markdown formatting, backticks, or extra words. Content:\n{snippet}"
            )
             
            # Sanitize the AI response (remove markdown backticks and spaces)
            raw_response = response.text.strip().lower().replace("`", "")
            
            # Optional: Debug line to view the exact AI output
            # print(f"\033[94m  [DEBUG] AI Answered: '{raw_response}'\033[0m")
            
            return raw_response
            
        except Exception as e:
            # Catch and display API connection errors safely
            # print(f"\n\033[93m  [DEBUG ERROR] API Failed: {e}\033[0m")
            return None

    def analyze(self, file_path: Path) -> Tuple[bool, str]:
        declared_ext = file_path.suffix.lower()
        
        # Phase 1: Hex Signature verification for binary files
        try:
            with open(file_path, 'rb') as f:
                header = f.read(self.db.max_bytes)
            
            for sig in self.db.signatures:
                sig_bytes = bytes.fromhex(sig['hex'])
                offset = sig.get('offset', 0)
                if header[offset:offset+len(sig_bytes)] == sig_bytes:
                    is_spoofed = declared_ext not in sig['extensions']
                    return is_spoofed, f"Signature: {sig['description']}"
        except Exception:
            return False, "Error reading file header"

        # Phase 2: AI verification (fallback if no binary signature is found)
        ai_prediction = self._predict_with_ai(file_path)
        if ai_prediction and ai_prediction != ".txt":
            # Flag as spoofed if the AI prediction contradicts the declared extension
            is_spoofed = (declared_ext != ai_prediction)
            return is_spoofed, f"AI Predicted: {ai_prediction}"

        return False, "Plain Text"

def main():
    parser = argparse.ArgumentParser(description="Advanced File Spoofing Detector")
    parser.add_argument("-f", "--file", required=True, help="Path to the file or directory to scan")
    args = parser.parse_args()

    # Check and display API status cleanly
    if not API_KEY:
        print("\033[93m[!] Warning: API Key not found in .env. AI features are disabled.\033[0m")
    else:
        print("\033[92m[*] API Key loaded. AI Engine is active.\033[0m")

    db = SignatureDB("signatures.json")
    analyzer = FileAnalyzer(db)
    target = Path(args.file)

    print(f"{'STATUS':<15} | {'FILE':<35} | {'METHOD/DETAILS'}")
    print("-" * 80)

    files = [target] if target.is_file() else target.glob("*")
    
    for p in files:
        if p.is_file():
            is_spoofed, detail = analyzer.analyze(p)
            status = "\033[91m[SPOOFED]\033[0m" if is_spoofed else "[OK]"
            print(f"{status:<24} | {p.name:<35} | {detail}")

if __name__ == "__main__":
    main()
