import json

# Load the JSON file
json_path = "/mnt/data/環大_240512_工事用端末中止入力が出来ない事象について_text_cleaned_block_generated.json"
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract only the 'generated' field and prepare for saving
text_blocks = [entry["generated"].strip() for entry in data if "generated" in entry]

# Save as .txt (concatenated)
txt_output_path = "/mnt/data/railway_generated_corpus.txt"
with open(txt_output_path, "w", encoding="utf-8") as f:
    f.write("\n\n".join(text_blocks))

# Save as .jsonl (each line a JSON with {"text": ...})
jsonl_output_path = "/mnt/data/railway_generated_corpus.jsonl"
with open(jsonl_output_path, "w", encoding="utf-8") as f:
    for block in text_blocks:
        json.dump({"text": block}, f, ensure_ascii=False)
        f.write("\n")

txt_output_path, jsonl_output_path
