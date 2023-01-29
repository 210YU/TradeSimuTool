import tkinter as tk
import global_value as g
from view import *
from function import *


def init():
    import_settings()
    init_main_window()
    init_position_window()
    init_candidate_window()


def init_main_window():
    g.root.title("メイン画面")
    g.root.geometry(str(g.settings["w_wide_half"])+"x"+str(g.settings["w_high"]) +
                    "+0+0")
    g.control_frame = tk.Frame(g.root)
    g.control_frame.pack(fill=tk.BOTH, padx=5, pady=5)
    view_control()
    g.result_frame = tk.Frame(g.root)
    g.result_frame.pack(fill=tk.BOTH, padx=5, pady=5)
    view_result(g.result_frame, "result")
    g.plot_frame = tk.Frame(g.root)
    g.plot_frame.pack(fill=tk.BOTH, padx=5, pady=5)
    view_result(g.plot_frame, "result")
    g.log_frame = tk.Frame(g.root)
    g.log_frame.pack(side="left", fill=tk.BOTH, padx=5, pady=5, expand=True)
    view_log(g.log_frame)


def init_position_window():
    g.position_win = tk.Toplevel()
    g.position_win.geometry(str(g.settings["w_wide_half"])+"x"+str(g.settings["w_high_half"]) +
                            "+"+str(g.settings["w_wide_half"])+"+0")
    g.position_win.title("ポジション一覧")
    view_position(g.position_win, "position")


def init_candidate_window():
    g.candidate_win = tk.Toplevel()
    g.candidate_win.geometry(str(g.settings["w_wide_half"])+"x"+str(g.settings["w_high_half"]) +
                             "+"+str(g.settings["w_wide_half"])+"+"+str(g.settings["w_high_half"]))
    g.candidate_win.title("候補一覧")
    view_candidate(g.candidate_win, "candidate")


def main():
    g.root = tk.Tk()
    init()
    g.root.mainloop()


main()
