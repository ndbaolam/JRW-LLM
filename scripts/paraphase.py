import json
import time
import random
import os
import google.generativeai as genai
from typing import List, Dict, Any
from tqdm import tqdm  # Import thư viện tqdm để hiển thị thanh tiến trình
import sys

# Gemini API Configuration
API_KEYS = [
    "AIzaSyA1XrP_xTskOR-MZ5oxYldLsomgJSrfHTA",
    "AIzaSyCN8cHAKD2Lz7hhI6nbct0GO5TiwfquWv4",
    "AIzaSyD3Zwc_zzIswWT1BawW7EhXG6Sb7Phg1sA",
    "AIzaSyA8YCsa60MCsQczCYlo06__URooIPiX5ts",
    "AIzaSyBbZXkww03L5UjN-5LLjdu7z7hWkN9UQbE",
    "AIzaSyA-_Te-cNeuC05oT1KQ1OfKMSzaceC9ifc",
    "AIzaSyA2fFGyrfR1p7ilT-VkHDcKp_cgiKppHdc",
    "AIzaSyAicd9hriwMcoG6t9IhyQV7HlEn0n5B8hY"
]

current_key_index = 0

def get_current_api_key():
    return API_KEYS[current_key_index]

def rotate_api_key():
    global current_key_index
    current_key_index = (current_key_index + 1) % len(API_KEYS)
    print(f"Đổi sang API key {current_key_index + 1}/{len(API_KEYS)}")
    return API_KEYS[current_key_index]

def call_gemini_generate(text_block: str) -> str | None:
    prompt = f"""
以下の20文の日本語文に基づいて、鉄道や列車の文脈に自然に関連する新しい文章を1つ作成してください。
- 内容は現実的で自然にしてください。
- 語彙や雰囲気は元の文に近づけてください。
- 出力は文章1つのみ、JSON形式で返してください。

元の文ブロック：
{text_block}

出力形式（JSONのみ）:
{{
  "generated": "新しい日本語の文章"
}}
"""

    max_retries = len(API_KEYS) * 2
    for attempt in range(max_retries):
        try:
            genai.configure(api_key=get_current_api_key())
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            response = model.generate_content(prompt)
            
            if response.text:
                text = response.text.strip()
                if text.startswith("```json"):
                    text = text.removeprefix("```json").strip()
                if text.endswith("```"):
                    text = text[:-3].strip()
                parsed = json.loads(text)
                return parsed.get("generated", None)
        except Exception as e:
            print(f"Lỗi khi gọi API: {e}")
            rotate_api_key()
        time.sleep(1 + random.random())

    print(f"❌ Không thể tạo nội dung cho block văn bản")
    return None

def process_txt_file(input_path: str):
    if not os.path.isfile(input_path):
        print(f"❌ File không tồn tại: {input_path}")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    results = []

    chunk_size = 20
    total_chunks = (len(lines) + chunk_size - 1) // chunk_size

    for i in tqdm(range(0, len(lines), chunk_size), desc="Đang xử lý block"):
        block = lines[i:i + chunk_size]
        text_block = "\n".join(block)
        print(f"\n➡️ Đang sinh nội dung cho block {i//chunk_size + 1}/{total_chunks}...\n")

        generated = call_gemini_generate(text_block)
        if generated:
            print(f"✅ Kết quả:\n{generated}\n")
            results.append({
                "source_lines": block,
                "generated": generated
            })
        else:
            print(f"⚠️ Không sinh được kết quả cho block này.")

        time.sleep(1.5 + random.random())

    output_path = input_path.replace(".txt", "_block_generated.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Đã lưu {len(results)} kết quả vào {output_path}")

# --- Điểm bắt đầu ---
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("📌 Cách dùng: python abc.py đường_dẫn_tới_file.txt")
        sys.exit(1)

    input_path = sys.argv[1]
    process_txt_file(input_path)