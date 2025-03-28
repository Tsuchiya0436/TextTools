import matplotlib.pyplot as plt
import japanize_matplotlib
import random
from wordcloud import WordCloud
import tkinter.messagebox as messagebox

def create_wordcloud(word_counts):
    if not word_counts:
        messagebox.showwarning('ワードクラウドエラー', '単語の解析結果がありません。前処理を実行してください。')
        return

    def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        # 色候補（黄色系を除外）
        colors = [
            "#4169e1",  # ブルー
            "#9b59b6",  # パープル
            "#e74c3c",  # 赤
            "#2ecc71",  # グリーン
            "#f39c12",  # オレンジ（薄め）
            "#ee82ee",  # ヴァイオレット
            "#00ff00",  # ライム
            "#ffd700",  # ゴールド
            "#00bfff",  # deepskyblue
        ]
        return random.choice(colors)

    # ワードクラウド生成
    wc = WordCloud(
        font_path="C:/Windows/Fonts/meiryo.ttc",  # 日本語対応
        background_color="white",  # 白背景
        width=2500,
        height=1000,
        min_font_size=3,
        max_font_size=150,
        relative_scaling=0.4,
        prefer_horizontal=1.0,  # 横向き固定
        max_words=1000,  # 表示する単語数
        color_func=color_func,  # カスタムカラー関数
    ).generate_from_frequencies(word_counts)

    # 画像の表示
    plt.figure(figsize=(10, 8))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()
