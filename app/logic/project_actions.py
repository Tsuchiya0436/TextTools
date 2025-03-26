from ui.new_project_dialog import NewProjectDialog
from utils.project_storage import save_project_info
import os

def new_project(root, text_area, project_name_label, memo_label, total_words_label, unique_words_label, simple_stats_label):
    def on_new_project_confirmed(filepath, memo, language, parser):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            text_area.delete("1.0", "end")
            text_area.insert("1.0", content)
            filename = os.path.basename(filepath)
            project_name_label.configure(text=filename)
            memo_label.configure(text=memo)  # ← ここで表示！

            total_words_label.configure(text="総抽出語数（使用）：- (-)")
            unique_words_label.configure(text="異なり語数（使用）：- (-)")
            simple_stats_label.configure(text="文書の単純集計：文 - ／段落 -")

            project_data = {
                "filename": filename,
                "filepath": filepath,
                "memo": memo,
                "language": language,
                "parser": parser
            }
            save_project_info(project_data)

    NewProjectDialog(root, on_new_project_confirmed)

