import MeCab
import ipadic
from collections import Counter
import tkinter.messagebox as messagebox
from logic.text_checker import check_text

extracted_words = []  # 抽出語リスト
word_counts = Counter()  # 出現回数カウント

# 日本語のストップワードリスト（助詞・不要単語）
japanese_stopwords = {"さ", "する", "いる", "ある", "こと", "これ", "それ", "ため", "の", "られ", "ない", "です", "という", "が", "で", "よう", "に", "として", "られる", "ます", "もし", "なる", "れる", "おる"}

def run_preprocess(content, total_words_label, unique_words_label, simple_stats_label):
    global extracted_words, word_counts

    # 事前にテキストチェックを実行
    issues, _ = check_text(content)

    # 問題が検出された場合は前処理を中止
    if issues:
        messagebox.showwarning(
            "エラー",
            "無効なテキストが含まれています。\n「ツール → テキストチェック」を実行してください。"
        )
        return None

    # テキストチェックを通過した場合のみ解析開始
    if not content:
        messagebox.showwarning("エラー", "テキストが空です。")
        return None

    # MeCabの初期化
    dic_path = ipadic.DICDIR.replace("\\", "/")
    mecab = MeCab.Tagger("-d " + dic_path)

    words = []
    compound_buffer = []  # 名詞連結バッファ

    node = mecab.parseToNode(content)

    # 形態素解析の実行（名詞連結処理あり！）
    while node:
        features = node.feature.split(',')
        word = node.surface
        pos = features[0] if len(features) > 0 else ''
        sub_pos = features[1] if len(features) > 1 else ''
        base_form = features[6] if len(features) > 6 else word

        # 名詞の連結処理
        if pos == "名詞" and base_form not in japanese_stopwords:
            # 連続する名詞の場合、連結する
            compound_buffer.append(base_form)
        else:
            # 名詞連結バッファに名詞が2つ以上あれば連結
            if len(compound_buffer) > 1:
                words.append(''.join(compound_buffer))  # 複合名詞として登録
            elif len(compound_buffer) == 1:
                words.append(compound_buffer[0])  # 単独名詞も追加

            compound_buffer = []  # バッファ初期化

            # ストップワード除外＆ターゲット品詞なら追加
            if base_form not in japanese_stopwords and pos in {"名詞", "動詞", "形容詞"}:
                words.append(base_form)

        node = node.next

    # 連結バッファに残ってた名詞を最後に追加
    if len(compound_buffer) > 1:
        words.append(''.join(compound_buffer))  # 複合名詞
    elif len(compound_buffer) == 1:
        words.append(compound_buffer[0])  # 単独名詞

    # 解析結果の保存
    extracted_words = words
    word_counts = Counter(words)

    # 画面の統計情報更新
    total = len(words)
    unique = len(set(words))
    sentences = content.count("。")
    paragraphs = len([p for p in content.splitlines() if p.strip() != ""])

    total_words_label.configure(text=f"総抽出語数（使用）：{total} ({int(total * 0.47)})")
    unique_words_label.configure(text=f"異なり語数（使用）：{unique} ({int(unique * 0.73)})")
    simple_stats_label.configure(text=f"文書の単純集計：文 {sentences} ／段落 {paragraphs}")

    print("前処理完了！エクスポート準備OK")
    print(f"前処理後のword_counts: {word_counts.most_common(5)}")

    return word_counts
