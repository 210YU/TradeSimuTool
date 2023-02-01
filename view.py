import tkinter as tk
import tkinter.ttk as ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
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
    text_list = ["tradeDay", "closeDay", "tradePeriod", "benefit", "swap_benefit", "flag", "corrDf_num", "close_tradeDiff", "target_profit", "pair1", "pair2", "pair3", "pair4", "tradeDiff", "tradePrice1", "tradePrice2", "tradePrice3", "tradePrice4",
                 "swap", "close_norm1", "close_norm2",  "tradeLots1",
                 "cost",   "closePrice1", "closePrice2", "closePrice3", "closePrice4", "benefit1", "benefit2", "benefit3", "benefit4"]
    g.tree_result = ttk.Treeview(window, selectmode="extended")
    # 列を３列作る
    g.tree_result["column"] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                               16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31)
    g.tree_result["show"] = "headings"
    # ヘッダーテキスト
    create_tree_column(text_list, g.tree_result)
    # データ挿入
    insert_result(g.result)
    # 設置
    g.tree_result.pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def view_position(window, file):
    print("start view_position")
    text_list = ["flag", "corrDf_num", "benefit", "swap_benefit", "close_tradeDiff", "target_profit", "pair1", "pair2", "pair3", "pair4", "tradeDiff", "tradePrice1", "tradePrice2", "tradePrice3", "tradePrice4",
                 "swap", "close_norm1", "close_norm2", "tradeDay", "tradeLots1",
                 "cost", "closeDay", "tradePeriod", "closePrice1", "closePrice2", "closePrice3", "closePrice4", "benefit1", "benefit2", "benefit3", "benefit4"]
    g.tree_position = ttk.Treeview(window, selectmode="extended")
    g.tree_position.bind("<Double-1>", select_position)  # 左ダブルクリック
    g.tree_position.bind("<Button-3>", select_position)  # 右クリック
    g.tree_position.bind("<Return>", select_position)  # Enterキー

    # 列を３列作る
    g.tree_position["column"] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                                 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31)
    g.tree_position["show"] = "headings"
    # ヘッダーテキスト
    create_tree_column(text_list, g.tree_position)

    # データ挿入
    insert_positions(g.positions)
    # 設置
    g.tree_position.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    add_scrollbar(g.tree_position)


def view_candidate(window):
    print("start view_candidate")
    text_list = ["Date", "No", "CLOSE_NORM_DIFF", "CLOSE_NORM_DIFF_PREV", "CLOSE_NORM_DIFF_DIFF",
                 "S1", "S2", "S1_Close", "S2_Close", "S1_J_Close", "S2_J_Close", "swap1", "swap2", "swap3", "swap4", "swap",
                 "CLOSE_ZSCORE_DIFF", "CLOSE_ZSCORE_DIFF_PREV", "CLOSE_ZSCORE_DIFF_DIFF", "S1_CLOSE_NORM", "S2_CLOSE_NORM ",
                 "TODAY_BENEFIT", "TODAY_BENEFIT_TOTAL"]
    g.tree_candidate = ttk.Treeview(window, selectmode="extended")
    g.tree_candidate.bind("<Double-1>", select_candidate)
    g.tree_candidate.bind("<Button-3>", select_candidate)
    g.tree_candidate.bind("<Return>", select_candidate)

    # 列を３列作る
    g.tree_candidate["column"] = (
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23)
    g.tree_candidate["show"] = "headings"

    create_tree_column(text_list, g.tree_candidate)

    # データ挿入
    insert_candidate(g.today_df, g.sort_diff)
    # 設置
    g.tree_candidate.pack(side=tk.TOP, padx=5, pady=5,
                          fill=tk.BOTH, expand=True)
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


def view_plot(window):
    # matplotlibの描画領域の作成
    fig = Figure(figsize=(10, 2))
    # 座標軸の作成
    g.ax1 = fig.add_subplot(1, 1, 1)
    g.ax2 = fig.add_subplot(1, 2, 1)

    # matplotlibの描画領域とウィジェット(Frame)の関連付け
    g.fig_canvas = FigureCanvasTkAgg(fig, window)
    # matplotlibのツールバーを作成
    g.toolbar = NavigationToolbar2Tk(g.fig_canvas, window)
    # matplotlibのグラフをフレームに配置
    g.fig_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def add_scrollbar(tree):
    hscrollbar = ttk.Scrollbar(
        tree, orient=tk.HORIZONTAL, command=tree.xview)
    vscrollbar = ttk.Scrollbar(
        tree, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(xscrollcommand=lambda f, l: hscrollbar.set(f, l))
    tree.configure(yscrollcommand=lambda f, l: vscrollbar.set(f, l))
    hscrollbar.pack(side="bottom", fill="x")
    vscrollbar.pack(side="right", fill="y")


def view_control():
    g.next_button = tk.Button(
        g.control_frame, text='Next', command=partial(next_func)).pack(side=tk.LEFT)
    g.step = 5
    g.skip_button = tk.Button(
        g.control_frame, text='Next to N step', command=partial(next_multi_func)).pack(side=tk.LEFT)


def create_tree_column(list, tree):
    for i, t in enumerate(list):
        tree.heading(i+1, text=t)
        # 列の幅
        if t == "Date":
            tree.column(i+1, width=100)
        elif t == "No":
            tree.column(i+1, width=20)
        else:
            tree.column(i+1, width=50)
