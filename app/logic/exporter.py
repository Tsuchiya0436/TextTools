import csv
import pandas as pd
from tkinter import filedialog
import tkinter.messagebox as messagebox


def export_results(word_counts):
    print(f"エクスポート開始時の word_counts: {word_counts.most_common(5)}")

    # エクスポート時に空ならエラー
    if not word_counts or len(word_counts) == 0:
        messagebox.showwarning("エクスポートエラー", "解析結果がありません。前処理を実行してください。")
        return

    # ファイル保存ダイアログ
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSVファイル", "*.csv"), ("Excelファイル", "*.xlsx")],
        title="エクスポート先を選択"
    )

    if not file_path:
        print("エクスポートがキャンセルされました。")
        return

    # CSV or Excel エクスポート
    if file_path.endswith(".csv"):
        with open(file_path, "w", newline='', encoding="utf-8-sig") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["単語", "出現回数"])
            for word, count in word_counts.most_common():
                writer.writerow([word, count])
    elif file_path.endswith(".xlsx"):
        df = pd.DataFrame(word_counts.items(), columns=["単語", "出現回数"])
        df.to_excel(file_path, index=False, engine="openpyxl")

    messagebox.showinfo("エクスポート完了", f"エクスポート完了！\n{file_path} に保存されました。")
    print(f"エクスポート完了！ {file_path} に保存されました。")
