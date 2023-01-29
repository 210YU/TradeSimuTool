import tkinter as tk
import tkinter.ttk as ttk
import global_value as g
from function import *
from functools import partial


class MovePositionButton(tk.Button):
    def move_position(self):
        w = self.winfo_screenwidth()  # モニター幅取得
        h = self.winfo_screenheight()  # モニター高さ取得
        return w, h


def view_result(window, file):
    print("start view_result")
    df = import_df(file)
    g.tree_result = ttk.Treeview(window)
    # 列を３列作る
    g.tree_result["column"] = (1, 2, 3)
    g.tree_result["show"] = "headings"
    # ヘッダーテキスト
    g.tree_result.heading(1, text="検索ワード")
    g.tree_result.heading(2, text="ランキング(ドメイン)")
    g.tree_result.heading(3, text="ランキング（URL）")
    # 列の幅
    g.tree_result.column(1, width=200)
    g.tree_result.column(2, width=100)
    g.tree_result.column(3, width=100)
    # データ挿入
    insert_result(df)
    # 設置
    g.tree_result.pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def view_position(window, file):
    print("start view_position")
    df = import_df(file)
    g.tree_position = ttk.Treeview(window)
    # 列を３列作る
    g.tree_position["column"] = (1, 2, 3)
    g.tree_position["show"] = "headings"
    # ヘッダーテキスト
    g.tree_position.heading(1, text="検索ワード")
    g.tree_position.heading(2, text="ランキング(ドメイン)")
    g.tree_position.heading(3, text="ランキング（URL）")
    # 列の幅
    g.tree_position.column(1, width=200)
    g.tree_position.column(2, width=100)
    g.tree_position.column(3, width=100)
    # データ挿入
    insert_position(df)
    # 設置
    g.tree_position.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    add_scrollbar(g.tree_position)


def view_candidate(window, file):
    print("start view_candidate")
    df = import_df(file)
    g.tree_candidate = ttk.Treeview(window)
    # 列を３列作る
    g.tree_candidate["column"] = (1, 2, 3)
    g.tree_candidate["show"] = "headings"
    # ヘッダーテキスト
    g.tree_candidate.heading(1, text="検索ワード")
    g.tree_candidate.heading(2, text="ランキング(ドメイン)")
    g.tree_candidate.heading(3, text="ランキング（URL）")
    # 列の幅
    g.tree_candidate.column(1, width=200)
    g.tree_candidate.column(2, width=100)
    g.tree_candidate.column(3, width=100)
    # データ挿入
    insert_candidate(df)
    # 設置
    g.tree_candidate.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    add_scrollbar(g.tree_candidate)


def view_log(window):
    print("start view_log")
    g.tree_log = ttk.Treeview(window)
    g.tree_log["column"] = (1)
    g.tree_log["show"] = "headings"
    # ヘッダーテキスト
    g.tree_log.heading(1, text="Logs")
    # 設置
    g.tree_log.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    add_scrollbar(g.tree_log)


def add_scrollbar(tree):
    hscrollbar = ttk.Scrollbar(
        tree, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=lambda f, l: hscrollbar.set(f, l))
    hscrollbar.pack(side="right", fill="y")


def view_control():
    g.next_button = tk.Button(
        g.control_frame, text='Next', command=partial(next_func, False,"a")).pack(side=tk.LEFT)
    g.skip_button = tk.Button(
        g.control_frame, text='Next to 10step').pack(side=tk.LEFT)
