import os
import tkinter as tk
from tkinter import filedialog
from ui.new_project_dialog import NewProjectDialog
from ui.project_manager_dialog import ProjectManagerDialog
from utils.project_storage import save_project_info, load_projects
from logic.project_actions import new_project
from logic.preprocessing import run_preprocess, extracted_words, word_counts
from logic.text_checker import run_text_check
from logic.exporter import export_results
from logic.wordcloud import create_wordcloud


def create_menu(
    root,
    text_area,
    project_name_label,
    total_words_label,
    unique_words_label,
    simple_stats_label,
    memo_label
):
    menubar = tk.Menu(root)

    # ===== プロジェクトメニュー =====
    menu_project = tk.Menu(menubar, tearoff=0)

    def open_project():
        projects = load_projects()
        if not projects:
            print("保存されたプロジェクトがありません")
            return

        def on_project_selected(proj):
            try:
                with open(proj["filepath"], "r", encoding="utf-8") as f:
                    content = f.read()
                    text_area.delete("1.0", "end")
                    text_area.insert("1.0", content)

                    filename = os.path.basename(proj["filepath"])
                    project_name_label.configure(text=filename)
                    memo_label.configure(text=proj.get("memo", ""))

                    # 統計リセット
                    total_words_label.configure(text="総抽出語数（使用）：- (-)")
                    unique_words_label.configure(text="異なり語数（使用）：- (-)")
                    simple_stats_label.configure(text="文書の単純集計：文 - ／段落 -")
            except Exception as e:
                print("読み込みに失敗:", e)

        ProjectManagerDialog(
            root,
            projects,
            on_project_selected,
            current_filename=project_name_label.cget("text"),
            text_area=text_area,
            project_name_label=project_name_label,
            total_words_label=total_words_label,
            unique_words_label=unique_words_label,
            simple_stats_label=simple_stats_label,
            memo_label=memo_label
        )

    def export_with_global_counts():
        global word_counts
        print(f"エクスポート時の word_counts: {word_counts.most_common(5)}")
        export_results(word_counts)

    def close_project():
        project_name_label.configure(text="（未選択）")
        total_words_label.configure(text="総抽出語数（使用）：- (-)")
        unique_words_label.configure(text="異なり語数（使用）：- (-)")
        simple_stats_label.configure(text="文書の単純集計：文 - ／段落 -")

    menu_project.add_command(label='新規',
                             accelerator='Ctrl+N',
                             command=lambda: new_project(root,
                                                         text_area,
                                                         project_name_label,
                                                         memo_label,
                                                         total_words_label,
                                                         unique_words_label,
                                                         simple_stats_label
                                                         )
                             )
    menu_project.add_command(label='開く', accelerator='Ctrl+O', command=open_project)
    menu_project.add_command(label='閉じる', accelerator='Ctrl+W', command=close_project)
    menu_project.add_separator()
    menu_project.add_command(label="エクスポート (CSV / Excel)", command=lambda: export_with_global_counts())
    menu_project.add_separator()
    menu_project.add_command(label='終了', accelerator='Ctrl+Q', command=root.quit)

    # ===== 前処理メニュー =====

    # 修正後のテキストを前処理で使う
    def update_text_after_check(text_area):
        updated_content = run_text_check(text_area)
        if updated_content:
            text_area.delete("1.0", "end")
            text_area.insert("1.0", updated_content)

    # `word_counts` を更新する関数
    def update_word_counts(content, total_words_label, unique_words_label, simple_stats_label):
        global word_counts
        new_word_counts = run_preprocess(content, total_words_label, unique_words_label, simple_stats_label)

        # None じゃなかったら word_counts を更新
        if new_word_counts is not None:
            word_counts = new_word_counts
            print(f"word_counts 更新完了！: {word_counts.most_common(5)}")
        else:
            print("⚠️ word_counts の更新がスキップされました！")

    menu_preprocess = tk.Menu(menubar, tearoff=0)
    menu_preprocess.add_command(
        label='前処理の実行',
        command=lambda: update_word_counts(
            text_area.get("1.0", "end").strip(),
            total_words_label,
            unique_words_label,
            simple_stats_label
        )
    )
    menu_preprocess.add_command(label="テキストチェック", command=lambda: update_text_after_check(text_area))

    # ===== ツールメニュー =====
    menu_tools = tk.Menu(menubar, tearoff=0)
    
    # ===== 抽出語メニュー =====
    menu_extract_words = tk.Menu(menu_tools, tearoff=0)
    menu_extract_words.add_command(label='抽出語リスト', command=lambda: print('抽出語リスト表示'))
    menu_extract_words.add_command(label='ワードクラウド', command=lambda: create_wordcloud(word_counts))
    menu_extract_words.add_command(label='記述統計', command=lambda: print('記述統計表示'))
    menu_tools.add_cascade(label='抽出語', menu=menu_extract_words)


    # ===== ヘルプメニュー (追加予定) =====
    menu_help = tk.Menu(menubar, tearoff=0)
    menu_help.add_command(label="バージョン情報", command=lambda: print("バージョン 1.0.0"))
    menu_help.add_command(label="使い方", command=lambda: print("使い方の説明はここに表示"))

    # ===== メニューバーに各メニューを追加 =====
    menubar.add_cascade(label='プロジェクト(P)', menu=menu_project)
    menubar.add_cascade(label='前処理(R)', menu=menu_preprocess)
    menubar.add_cascade(label='ツール(T)', menu=menu_tools)
    menubar.add_cascade(label='ヘルプ(H)', menu=menu_help)

    # ===== ショートカットキー =====
    root.bind_all('<Control-n>', lambda e: new_project(
        root,
        text_area,
        project_name_label,
        memo_label,
        total_words_label,
        unique_words_label,
        simple_stats_label
    ))
    root.bind_all('<Control-o>', lambda e: open_project())
    root.bind_all('<Control-q>', lambda e: root.quit())
    root.bind_all("<Control-e>", lambda e: export_with_global_counts())
    root.bind_all("<Control-w>", lambda e: create_wordcloud())

    return menubar
