import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox as messagebox
from ui.edit_project_dialog import EditProjectDialog
from utils.project_storage import delete_project
from logic.project_actions import new_project


class ProjectManagerDialog(ctk.CTkToplevel):
    def __init__(
    self,
    parent,
    project_list,
    on_open_callback,
    current_filename=None,
    text_area=None,
    project_name_label=None,
    total_words_label=None,
    unique_words_label=None,
    simple_stats_label=None,
    memo_label=None
):
        super().__init__(parent)
        self.title("プロジェクト・マネージャ")
        self.geometry("600x300")
        self.on_open_callback = on_open_callback
        self.projects = project_list
        self.current_filename = current_filename
        self.text_area = text_area
        self.project_name_label = project_name_label
        self.total_words_label = total_words_label
        self.unique_words_label = unique_words_label
        self.simple_stats_label = simple_stats_label
        self.memo_label = memo_label

        self.attributes('-topmost', True)
        self.focus_force()

        # ヘッダーラベルを追加
        header_frame = ctk.CTkFrame(self)
        header_frame.pack(padx=10, pady=(10, 0), fill="x")

        header_font = ("Courier New", 14, "bold")

        ctk.CTkLabel(header_frame, text="ファイル名         ", font=header_font, width=160, anchor="w").pack(side="left")
        ctk.CTkLabel(header_frame, text="言語    ", font=header_font, width=70, anchor="w").pack(side="left")
        ctk.CTkLabel(header_frame, text="メモ                      ", font=header_font, width=220, anchor="w").pack(side="left")
        ctk.CTkLabel(header_frame, text="ディレクトリ", font=header_font, width=240, anchor="w").pack(side="left")

        self.project_listbox = tk.Listbox(self, height=10, font=("Courier New", 14))
        self.project_listbox.pack(padx=10, pady=10, fill="both", expand=True)

        for proj in project_list:
            memo = proj['memo']
            short_memo = memo[:10] + "…" if len(memo) > 10 else memo
            display = f"{proj['filename']:<15} {proj['language']:<6} {short_memo:<7} {proj['filepath']}"
            self.project_listbox.insert("end", display)


        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=5, padx=10, fill="x")

        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)
        btn_frame.columnconfigure(2, weight=1)

        # 左寄せ（削除）
        delete_btn = ctk.CTkButton(btn_frame, text="削除", width=80, command=self.delete_project)
        delete_btn.grid(row=0, column=0, sticky="w", padx=(0, 10))

        # 中央（新規・編集）
        mid_frame = ctk.CTkFrame(btn_frame)
        mid_frame.grid(row=0, column=1)
        new_btn = ctk.CTkButton(mid_frame, text="新規", width=80, command=self.handle_new_project)
        new_btn.pack(side="left", padx=5)
        edit_btn = ctk.CTkButton(mid_frame, text="編集", width=80, command=self.edit_project)
        edit_btn.pack(side="left", padx=5)

        # 右寄せ（開く・キャンセル）
        open_btn = ctk.CTkButton(btn_frame, text="開く", width=80, command=self.open_project)
        open_btn.grid(row=0, column=2, sticky="e", padx=(10, 85))
        cancel_btn = ctk.CTkButton(btn_frame, text="キャンセル", width=80, command=self.destroy)
        cancel_btn.grid(row=0, column=2, sticky="e", padx=(95, 0))  # ←開くの右横に詰める感じ


    def handle_new_project(self):
        # ダイアログを閉じてから新規プロジェクト作成を呼び出す
        self.destroy()

        new_project(
            self.master,  # parent
            self.text_area,
            self.project_name_label,
            self.total_words_label,
            self.unique_words_label,
            self.simple_stats_label
        )

    def open_project(self):
        selection = self.project_listbox.curselection()
        if not selection:
            return

        selected_index = selection[0]
        selected_project = self.projects[selected_index]
        self.on_open_callback(selected_project)

        if self.memo_label:
            self.memo_label.configure(text=selected_project.get('memo', ''))

        self.destroy()

    def edit_project(self):
        selection = self.project_listbox.curselection()
        if not selection:
            return

        selected_index = selection[0]
        selected_project = self.projects[selected_index]

        self.withdraw()

        def on_updated(updated_project):
            self.projects[selected_index] = updated_project
            # 表示を更新
            self.project_listbox.delete(selected_index)
            display = f'{updated_project["filename"]}｜{updated_project["language"]}｜{updated_project["memo"]}｜{updated_project["filepath"]}'
            self.project_listbox.insert(selected_index, display)
            self.deiconify()

        EditProjectDialog(self, selected_project, on_updated)

    def delete_project(self):
        selection = self.project_listbox.curselection()
        if not selection:
            return

        selected_index = selection[0]
        selected_project = self.projects[selected_index]

        if selected_project["filename"] == self.current_filename:
            messagebox.showwarning("削除できません", "現在開いているプロジェクトは削除できません。", parent=self)
            return

        from utils.project_storage import delete_project
        delete_project(selected_project["filename"])
        self.project_listbox.delete(selected_index)
        self.projects.pop(selected_index)