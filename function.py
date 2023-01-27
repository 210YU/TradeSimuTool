
import global_value as g
import pandas as pd
import tkinter as tk
import view


def import_df(file):
    df = pd.DataFrame()
    df["T1"] = [0, 1, 2, 3]
    df["T2"] = ["a", "b", "c", "d"]
    df["T3"] = ["#", "$", "%", "&"]
    return df


def next_func():
    print("Click button : next_func")
    # 保持ポジションウィンドウ更新
    update_position()
    # 候補ウィンドウ更新
    update_candidate()
    # ログ表示
    insert_log("Test")


def insert_log(mes):
    g.tree_log.insert("", "end", values=(mes))


def delete_tree(tree):
    for i in tree.get_children():
        tree.delete(i)


def insert_position(df):
    for i in range(len(df)):
        g.tree_position.insert("", "end", values=(
            df['T1'][i], df['T2'][i], df['T3'][i]))


def update_position():
    delete_tree(g.tree_position)
    df = import_df("position")
    insert_position(df)


def insert_candidate(df):
    for i in range(len(df)):
        g.tree_candidate.insert("", "end", values=(
            df['T1'][i], df['T2'][i], df['T3'][i]))


def update_candidate():
    delete_tree(g.tree_candidate)
    df = import_df("candidate")
    insert_candidate(df)


def insert_result(df):
    for i in range(len(df)):
        g.tree_result.insert("", "end", values=(
            df['T1'][i], df['T2'][i], df['T3'][i]))


def update_result():
    delete_tree(g.tree_result)
    df = import_df("result")
    insert_result(df)
