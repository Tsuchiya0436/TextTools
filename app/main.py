import customtkinter as ctk
import tkinter as tk
from menu import create_menu

def main():
    ctk.set_appearance_mode('light')
    ctk.set_default_color_theme('blue')

    root = ctk.CTk()
    root.title('TextTools')
    root.geometry('800x600')

    # ===== Projectセクション =====
    ctk.CTkLabel(root, text="Project", font=("Arial", 16, "bold")).pack(padx=10, anchor="w")
    project_frame = ctk.CTkFrame(root)
    project_frame.pack(padx=10, pady=(0, 10), fill='x')

    ctk.CTkLabel(project_frame, text='現在のプロジェクト').grid(row=0, column=0, sticky='w', padx=5, pady=5)
    project_name_label = ctk.CTkLabel(project_frame, text='（未選択）')
    project_name_label.grid(row=0, column=1, sticky='w', padx=5, pady=5)

    # プロジェクトメモの表示
    ctk.CTkLabel(project_frame, text='メモ：').grid(row=2, column=0, sticky='w', padx=5, pady=5)
    memo_label = ctk.CTkLabel(project_frame, text='（なし）')
    memo_label.grid(row=2, column=1, sticky='w', padx=5, pady=5)


    # ===== Database Statsセクション =====
    ctk.CTkLabel(root, text="Database Stats", font=("Arial", 16, "bold")).pack(padx=10, anchor="w")
    stats_frame = ctk.CTkFrame(root)
    stats_frame.pack(padx=10, pady=(0, 10), fill='x')

    total_words_label = ctk.CTkLabel(stats_frame, text="総抽出語数（使用）：- (-)")
    total_words_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

    unique_words_label = ctk.CTkLabel(stats_frame, text="異なり語数（使用）：- (-)")
    unique_words_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)

    unit_label = ctk.CTkLabel(stats_frame, text="集計単位：ケース数")
    unit_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)

    simple_stats_label = ctk.CTkLabel(stats_frame, text="文書の単純集計：文 - ／段落 -")
    simple_stats_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)

    # ===== 確認ボタン =====
    def show_text_window():
        content = text_area.get("1.0", "end").strip()
        if not content:
            print("表示するテキストがありません")
            return

        # 新しいウィンドウ作成
        win = ctk.CTkToplevel(root)
        win.title("全文表示")
        win.geometry("600x400")

        # メインウィンドウの位置を取得して少し右下に表示
        root.update_idletasks()
        x = root.winfo_x()
        y = root.winfo_y()
        win.geometry(f"+{x + 100}+{y + 100}")  # ちょっとずらす

        # 最前面に出す
        win.lift()
        win.attributes('-topmost', True)
        win.focus_force()

        # テキスト表示
        preview_box = ctk.CTkTextbox(win, width=580, height=330)
        preview_box.insert("1.0", content)
        preview_box.configure(state="disabled")
        preview_box.pack(padx=10, pady=10)

        # 閉じるボタン
        close_btn = ctk.CTkButton(win, text="閉じる", command=win.destroy)
        close_btn.pack(pady=(0, 10))

    # ボタン設置
    preview_button = ctk.CTkButton(root, text="確認", command=show_text_window)
    preview_button.pack(pady=(0, 20))

    # ===== テキストボックス（非表示）=====
    text_area = ctk.CTkTextbox(root, width=780, height=300)
    text_area.pack_forget()

    # ===== メニュー作成 =====
    menubar = create_menu(
        root,
        text_area,
        project_name_label,
        total_words_label,
        unique_words_label,
        simple_stats_label,
        memo_label
    )
    root.configure(menu=menubar)

    root.mainloop()

if __name__ == '__main__':
    main()
