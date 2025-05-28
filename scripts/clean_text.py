import re
import os

def clean_text_file(input_txt: str, output_txt: str = None):
    with open(input_txt, "r", encoding="utf-8") as f:
        lines = f.readlines()

    cleaned_lines = []
    prev_line = None

    for line in lines:
        line = re.sub(r"[^\wぁ-んァ-ン一-龯ー。、・\s\-→⇔〇/＝:=\[\](){}0-9]", "", line.strip())
        if not line:
            continue
        if line == prev_line:
            continue
        cleaned_lines.append(line)
        prev_line = line

    result = "\n".join(cleaned_lines)

    if not output_txt:
        output_txt = os.path.splitext(input_txt)[0] + "_cleaned.txt"

    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"✅ {output_txt}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("⚠️ python clean_text_file.py <file.txt>")
    else:
        clean_text_file(sys.argv[1])
