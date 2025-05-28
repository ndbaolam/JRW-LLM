import pandas as pd
import os

def extract_text_from_excel(file_path: str, output_txt: str = None):    
    sheets = pd.read_excel(file_path, sheet_name=None)
    all_texts = []

    for sheet_name, df in sheets.items():
        df_clean = df.dropna(how="all").dropna(axis=1, how="all")
        if df_clean.empty:
            continue

        all_texts.append(f"=== Sheet: {sheet_name} ===")
        for column in df_clean.columns:
            col_data = df_clean[column].dropna()
            if col_data.apply(lambda x: isinstance(x, str)).all():
                for val in col_data:
                    all_texts.append(str(val))

    combined_text = "\n".join(all_texts)
    
    if not output_txt:
        output_txt = os.path.splitext(file_path)[0] + "_text.txt"

    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(combined_text)

    print(f"✅ {output_txt}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("⚠️ python extract_text_from_excel.py <đường_dẫn_file_excel>")
    else:
        file_path = sys.argv[1]
        extract_text_from_excel(file_path)
