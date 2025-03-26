import os
import csv
import tkinter as tk
import MeCab
import ipadic
from tkinter import filedialog
import tkinter.messagebox as messagebox
from janome.tokenizer import Tokenizer
from collections import Counter
from ui.new_project_dialog import NewProjectDialog
from ui.project_manager_dialog import ProjectManagerDialog
from utils.project_storage import save_project_info, load_projects
from logic.project_actions import new_project

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

                    # メモ表示
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
    menu_project.add_command(label='終了', accelerator='Ctrl+Q', command=root.quit)

    # ===== 前処理メニュー =====
    menu_preprocess = tk.Menu(menubar, tearoff=0)

    def run_preprocess():
        # MeCabの初期化

        dic_path = ipadic.DICDIR.replace("\\", "/")
        mecab = MeCab.Tagger("-d " + dic_path)

        content = text_area.get("1.0", "end").strip()
        if not content:
            print("テキストが空です")
            return

        # ターゲットとする品詞（変更なし）
        target_pos = {
            '名詞': {'一般', '固有名詞', 'サ変接続'},
            '動詞': {'自立'},
            '形容詞': {'自立'},
            '副詞': {'一般'}
        }

        words = []
        node = mecab.parseToNode(content)

        # 名詞連結用の一時バッファ
        compound_buffer = []

        while node:
            features = node.feature.split(',')
            pos = features[0]
            sub_pos = features[1] if len(features) > 1 else ''
            base_form = features[6] if len(features) > 6 else node.surface

            if pos == '名詞' and sub_pos in {'一般', '固有名詞', 'サ変接続'}:
                compound_buffer.append(base_form)
            else:
                if len(compound_buffer) > 1:
                    words.append(''.join(compound_buffer))  # 複合語として追加
                elif len(compound_buffer) == 1:
                    words.append(compound_buffer[0])  # 単独名詞
                compound_buffer = []

                # 複合語以外もターゲットなら追加
                if pos in target_pos and sub_pos in target_pos[pos]:
                    words.append(base_form)

            node = node.next

        # バッファに残ってた場合
        if compound_buffer:
            if len(compound_buffer) > 1:
                words.append(''.join(compound_buffer))
            else:
                words.append(compound_buffer[0])

        total = len(words)
        unique = len(set(words))
        sentences = content.count("。")
        paragraphs = len([p for p in content.splitlines() if p.strip() != ""])

        total_words_label.configure(text=f"総抽出語数（使用）：{total} ({int(total*0.47)})")
        unique_words_label.configure(text=f"異なり語数（使用）：{unique} ({int(unique*0.73)})")
        simple_stats_label.configure(text=f"文書の単純集計：文 {sentences} ／段落 {paragraphs}")

        # CSVエクスポート
        word_counts = Counter(words)
        with open("texttools_output.csv", "w", newline='', encoding="utf-8-sig") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["単語", "出現回数"])
            for word, count in word_counts.most_common():
                writer.writerow([word, count])

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
    root.bind_all('<Control-o>', lambda e: open_project())
    root.bind_all('<Control-q>', lambda e: root.quit())

    return menubar
