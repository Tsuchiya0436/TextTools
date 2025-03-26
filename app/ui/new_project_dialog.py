import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from utils.project_storage import load_projects

# 新規プロジェクト作成ダイアログ
class NewProjectDialog(ctk.CTkToplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.title("新規プロジェクト")
        self.geometry("550x200")
        self.callback = callback  # OKを押した後の処理を受け取るコールバック

        # 初期値
        self.selected_file = tk.StringVar()
        self.memo = tk.StringVar()
        self.language = tk.StringVar(value="日本語")
        self.parser = tk.StringVar(value="MeCab")

        self.lift()
        self.attributes('-topmost', True)
        self.focus_force()

        # ファイル選択ラベル
        ctk.CTkLabel(self, text="分析対象ファイル：").grid(row=0, column=0, sticky="w", padx=10, pady=10)

        # 参照ボタン（先に左に置く）
        browse_btn = ctk.CTkButton(self, text="参照", width=60, command=self.select_file)
        browse_btn.grid(row=0, column=1, padx=(5, 5), pady=10, sticky="w")

        # ファイルパスのエントリ（右に広がるように）
        file_entry = ctk.CTkEntry(self, textvariable=self.selected_file, width=280)
        file_entry.grid(row=0, column=2, padx=5, pady=10, sticky="we")

        # メモ
        ctk.CTkLabel(self, text="説明（メモ）：").grid(row=1, column=0, sticky="w", padx=10)
        memo_entry = ctk.CTkEntry(self, textvariable=self.memo, width=300)
        memo_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="w")

        # 言語 & 形態素解析器（固定）
        ctk.CTkLabel(self, text="言語：").grid(row=2, column=0, sticky="w", padx=10)
        lang_label = ctk.CTkLabel(self, textvariable=self.language)
        lang_label.grid(row=2, column=1, sticky="w")

        parser_label = ctk.CTkLabel(self, textvariable=self.parser)
        parser_label.grid(row=2, column=2, sticky="w")

        # ボタン
        btn_frame = ctk.CTkFrame(self)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=15)
        ok_btn = ctk.CTkButton(btn_frame, text="OK", command=self.on_ok)
        ok_btn.pack(side="left", padx=10)
        cancel_btn = ctk.CTkButton(btn_frame, text="キャンセル", command=self.destroy)
        cancel_btn.pack(side="left")

    def select_file(self):
        # 一時的に topmost を外す
        self.attributes('-topmost', False)

        filepath = filedialog.askopenfilename(
            title="分析対象ファイルを選択",
            filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')]
        )

        if filepath:
            self.selected_file.set(filepath)

        # 終わったら再び最前面に戻す
        self.lift()
        self.attributes('-topmost', True)
        self.focus_force()

    def on_ok(self):
        filepath = self.selected_file.get()
        # 重複チェック
        existing = load_projects()
        if any(p['filepath'] == filepath for p in existing):
            messagebox.showwarning('TextTools',
                                    'このファイルはすでにプロジェクトに保存されています。\n「プロジェクト」からそのファイルを選択して「開く」ボタンをクリックしてください',
                                    parent=self)
            return 
        self.callback(
            self.selected_file.get(),
            self.memo.get(),
            self.language.get(),
            self.parser.get()
        )
        self.destroy()
