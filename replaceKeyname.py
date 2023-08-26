import os
import csv
import re
import sys

# CSVファイルを辞書としてロードする
def load_csv_to_dict(file_path):
    data_dict = {}
    with open(file_path, 'r', encoding='utf-8-sig') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if len(row) > 1:
                data_dict[row[0]] = row[1]
            else:
                data_dict[row[0]] = None
    return data_dict

# 既存キー名称を固定文字列に置換（最初にマッチしたもののみ）
def replace_existing_keyname_with_fixed_string(filename, key_maps1):
    word_boundary = r'(?<![a-zA-Z0-9])'
    word_end_or_extension = r'(?=[_\- ]|\.\w+|$)'  # 任意の拡張子をマッチさせる
    for key in sorted(key_maps1.keys(), key=lambda x: -len(x)):
        pattern = word_boundary + re.escape(key) + word_end_or_extension
        filename, _ = re.subn(pattern, "@keyname@", filename, count=1)
        if "@" in filename:
            break
    return filename

# 固定文字列を一般的なキー名称に置換
def replace_fixed_string_with_general_keyname(filename, key_maps2):
    mixed_in_key = filename.split(" - ")[0]
    general_keyname = key_maps2.get(mixed_in_key, None)
    if general_keyname:
        filename = filename.replace("@keyname@", general_keyname)
    return filename

# ファイル名の置換処理
def process_file_renaming(filename, key_maps1, key_maps2):
    filename = replace_existing_keyname_with_fixed_string(filename, key_maps1)
    filename = replace_fixed_string_with_general_keyname(filename, key_maps2)
    return filename

# ログ出力
def log_output(directory_path, original_name, new_name, log_file_path="./replaceKeyname.log", first_entry=False):
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        if first_entry:
            log_file.write(f"\n{directory_path}\n")
        log_file.write(f"before: {original_name}\n")
        log_file.write(f"after: {new_name}\n")
        log_file.write("-" * 50 + "\n")

# 主処理
def main_process(directory_path, key_maps1, key_maps2):
    filenames = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    first_entry = True
    for filename in filenames:
        original_name = filename
        new_name = process_file_renaming(filename, key_maps1, key_maps2)
        os.rename(os.path.join(directory_path, original_name), os.path.join(directory_path, new_name))
        log_output(directory_path, original_name, new_name, first_entry=first_entry)
        first_entry = False

# エントリポイント
if __name__ == "__main__":
    # キーのマップ情報をロード
    key_maps1 = load_csv_to_dict("./keyMaps1.csv")
    key_maps2 = load_csv_to_dict("./keyMaps2.csv")

    # ログファイルを初期化
    with open("./replaceKeyname.log", 'w', encoding='utf-8'):
        pass

    # コマンドライン引数からディレクトリパスを取得
    directory_paths = sys.argv[1:]

    # 各ディレクトリに対して処理を実行
    for directory_path in directory_paths:
        main_process(directory_path, key_maps1, key_maps2)
