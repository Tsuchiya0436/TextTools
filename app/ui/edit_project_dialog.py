import customtkinter as ctk
import tkinter as tk
from utils.project_storage import save_project_info


class EditProjectDialog(ctk.CTkToplevel):
    def __init__(self, parent, project_data, on_updated_callback):
        super().__init__(parent)
        self.title("プロジェクト編集")
        self.geometry("500x200")
        self.project_data = project_data
        self.on_updated_callback = on_updated_callback

        self.attributes('-topmost', True)
        self.focus_force()

        self.memo_var = tk.StringVar(value=project_data.get("memo", ""))

        # 表示部分
        ctk.CTkLabel(self, text=f"ファイル名：{project_data['filename']}").pack(pady=5, anchor="w", padx=10)
        ctk.CTkLabel(self, text=f"パス：{project_data['filepath']}").pack(pady=5, anchor="w", padx=10)

        # メモ編集
        ctk.CTkLabel(self, text="説明（メモ）：").pack(pady=(10, 0), anchor="w", padx=10)
        memo_entry = ctk.CTkEntry(self, textvariable=self.memo_var, width=400)
        memo_entry.pack(padx=10, pady=5, anchor="w")

        # ボタン
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=10)

        save_btn = ctk.CTkButton(btn_frame, text="保存", command=self.save)
        save_btn.pack(side="left", padx=10)

        cancel_btn = ctk.CTkButton(btn_frame, text="キャンセル", command=self.destroy)
        cancel_btn.pack(side="left")

        self.lift()
        self.attributes('-topmost', True)
        self.focus_force()

    def save(self):
        self.project_data["memo"] = self.memo_var.get()
        save_project_info(self.project_data)  # 上書き保存
        self.on_updated_callback(self.project_data)
        self.destroy()
