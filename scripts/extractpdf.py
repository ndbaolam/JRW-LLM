import os
import re
import pdfplumber
import sys
import warnings
warnings.filterwarnings("ignore")

patterns_to_remove = [
    r"Hitachi,Ltd\..*?Japan",
    r"OMIKA DWG\. NO\..*?\n",
    r"PAGE\s*\d+/?\d*",
    r"331DV\d+",
    r"\(?[根池飯横貝]\)?",
    r"REV\.\s*Ｓ　Ｏ　Ｎ　Ａ",
    r"TITLE\s+REV\.",
    r"DWN\..*?SIGNATURE",
    r"REVISIONS[\s\S]{0,100}?(DATE|DESCRIPTION)",
    r"^\s*$",
    r"[\u3000\s]{2,}",    
    r"[○◎●◆◇■□※＊★☆▲△▼▽]+",
]

def extract_data(filename: str):
    print(f"Extracting data from {filename}")

    all_text = ""
    with pdfplumber.open(filename) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                for pattern in patterns_to_remove:
                    text = re.sub(pattern, "", text)
                    text = re.sub(r'(.)\1{2,}', r'\1', text)
                   
                    text = re.sub(r'[Ａ-Ｚ]', lambda m: chr(ord(m.group(0)) - 65248), text)  # full-width → normal
                    text = re.sub(r'(?<=\b)([A-Z])(?:\s+[A-Z]){1,}', lambda m: ''.join(m.group(0).split()), text)


                all_text += text + "\n"    
    
    output_file = os.path.splitext(os.path.basename(filename))[0] + ".txt"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(all_text)
    print(f"Saved to: {output_file}")

if __name__ == "__main__":
    file_path = sys.argv[1]
    extract_data(file_path)