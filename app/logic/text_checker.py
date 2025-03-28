import re
import tkinter.messagebox as messagebox

def check_text(content):
    issues = []
    suggestions = []  # 修正候補

    # ① 空行が多すぎる
    if content.count("\n\n") > 5:
        issues.append("空行が多すぎます")
        suggestions.append("空行を1行にまとめる")

    # ④ 重複文の検出
    sentences = [s.strip() for s in content.splitlines() if s.strip()]
    if len(sentences) != len(set(sentences)):
        issues.append("重複した文があります")
        suggestions.append("重複文を自動的に削除する")

    # ⑤ 空白・タブの異常検出
    if re.search(r'\s{2,}', content):
        issues.append("空白が多すぎます")
        suggestions.append("空白/タブを適切に修正")

    # ⑥ 禁則文字・異常記号の検出
    if re.search(r'[★☆■◆□]', content):
        issues.append("機種依存文字が含まれています")
        suggestions.append("機種依存文字を ? に変換する")

    return issues, suggestions


def auto_fix_text(content):
    # 空行の調整
    content = re.sub(r'\n{3,}', '\n\n', content)

    # 重複文の削除
    lines = list(dict.fromkeys(content.splitlines()))
    content = '\n'.join(lines)

    # 空白・タブの調整
    content = re.sub(r'\s{2,}', ' ', content)
    content = content.replace('\t', ' ')

    # 機種依存文字の置換
    content = re.sub(r'[★☆■◆□]', '?', content)

    return content


def run_text_check(text_area):
    content = text_area.get("1.0", "end").strip()
    if not content:
        messagebox.showwarning("エラー", "テキストが空です。")
        return content  # 元の内容を返す

    issues, suggestions = check_text(content)
    if issues:
        issue_message = "\n".join([f"⚠️ {issue}" for issue in issues])
        suggestion_message = "\n".join([f"➡️ {suggestion}" for suggestion in suggestions])

        # 修正するか確認
        choice = messagebox.askyesno(
            "テキストチェック結果",
            f"{issue_message}\n\n{suggestion_message}\n\n修正して続行しますか？"
        )

        if choice:
            content = auto_fix_text(content)  # 自動修正
            text_area.delete("1.0", "end")
            text_area.insert("1.0", content)  # 修正後のテキストを表示
            messagebox.showinfo("修正完了", "問題を自動的に修正しました！")
            return content  # 修正後のテキストを返す
        else:
            messagebox.showwarning("修正なし", "テキスト修正せずに終了しました。")
            return content  # 修正なしの場合、元のテキストを返す
    else:
        messagebox.showinfo("チェック完了", "問題は検出されませんでした。")
        return content  # 問題なしならそのままの内容を返す


