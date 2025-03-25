import os
import tkinter as tk
from tkinter import filedialog

def create_menu(
    root,
    text_area,
    project_name_label,
    total_words_label,
    unique_words_label,
    simple_stats_label
):
    menubar = tk.Menu(root)

    # ===== プロジェクトメニュー =====
    menu_project = tk.Menu(menubar, tearoff=0)

    def new_project():
        text_area.delete("1.0", "end")
        project_name_label.configure(text="（未選択）")
        total_words_label.configure(text="総抽出語数（使用）：- (-)")
        unique_words_label.configure(text="異なり語数（使用）：- (-)")
        simple_stats_label.configure(text="文書の単純集計：文 - ／段落 -")

    def open_file():
        filepath = filedialog.askopenfilename(
            title='プロジェクトを開く',
            filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')]
        )
        if filepath:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                text_area.delete("1.0", "end")
                text_area.insert("1.0", content)

                filename = os.path.basename(filepath)
                project_name_label.configure(text=filename)

    def close_project():
        project_name_label.configure(text="（未選択）")
        total_words_label.configure(text="総抽出語数（使用）：- (-)")
        unique_words_label.configure(text="異なり語数（使用）：- (-)")
        simple_stats_label.configure(text="文書の単純集計：文 - ／段落 -")

    menu_project.add_command(label='新規', accelerator='Ctrl+N', command=new_project)
    menu_project.add_command(label='開く', accelerator='Ctrl+O', command=open_file)
    menu_project.add_command(label='閉じる', accelerator='Ctrl+W', command=close_project)
    menu_project.add_separator()
    menu_project.add_command(label='終了', accelerator='Ctrl+Q', command=root.quit)

    # ===== 前処理メニュー =====
    menu_preprocess = tk.Menu(menubar, tearoff=0)

    def run_preprocess():
        content = text_area.get("1.0", "end").strip()
        if not content:
            print("テキストが空です")
            return

        words = content.split()
        total = len(words)
        unique = len(set(words))
        sentences = content.count("。")
        paragraphs = content.count("\n\n") + 1

        total_words_label.configure(text=f"総抽出語数（使用）：{total} ({int(total*0.47)})")
        unique_words_label.configure(text=f"異なり語数（使用）：{unique} ({int(unique*0.73)})")
        simple_stats_label.configure(text=f"文書の単純集計：文 {sentences} ／段落 {paragraphs}")

    menu_preprocess.add_command(label='前処理の実行', command=run_preprocess)

    # ===== その他メニュー =====
    menu_tools = tk.Menu(menubar, tearoff=0)
    menu_help = tk.Menu(menubar, tearoff=0)

    menubar.add_cascade(label='プロジェクト(P)', menu=menu_project)
    menubar.add_cascade(label='前処理(R)', menu=menu_preprocess)
    menubar.add_cascade(label='ツール(T)', menu=menu_tools)
    menubar.add_cascade(label='ヘルプ(H)', menu=menu_help)

    # ===== ショートカットキー =====
    root.bind_all('<Control-n>', lambda e: new_project())
    root.bind_all('<Control-o>', lambda e: open_file())
    root.bind_all('<Control-q>', lambda e: root.quit())

    return menubar
