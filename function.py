
import global_value as g
import view
import calculation
import pandas as pd
import tkinter as tk
import datetime as dt


def import_df(file):
    df = pd.DataFrame()
    df["T1"] = [0, 1, 2, 3]
    df["T2"] = ["a", "b", "c", "d"]
    df["T3"] = ["#", "$", "%", "&"]
    return df


def next_func(recalc, test_v):
    print("Click button : next_func")
    insert_log(test_v)
    # 保持ポジションウィンドウ更新
    update_position()
    # 候補ウィンドウ更新
    update_candidate()
    # ログ表示
    insert_log("Test")


def insert_log(mes):
    mes = mes.replace(" ", "_")
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


def import_data(re_calc=False):
    # re_calc:Trueで再計算 Falseで保存されたdfを読み込み
    if re_calc:
        print("start calculation")
        g.dfSelectList = calculation.calc_maxmin_df()
    else:
        g.dfSelectList = []
        for i in range(len(g.corrDf)):
            a = pd.read_pickle(g.settings["df_dir"]+str(i)+".pickle")
            g.dfSelectList.append(a)


def searchDayInd1_(df3, day):
    for i in range(1, 10):
        if day in list(df3["Date"]):
            ind = 0
            # df3のDateをリスト化→dayと一致するインデックスを取得
            ind = (list(df3["Date"]).index(day))
            return ind+1
        else:
            day = (pd.to_datetime(day) - dt.timedelta(i)).strftime("%Y-%m-%d")
    return -1


def import_corrDf():
    results = pd.read_csv(g.settings["corrDf_dir"])
    results["PF"] = results["PLUS"] / (-1 * results["MINUS"])
    results = results[results["PF"] > 0.7]
    results = results.sort_values('PF', ascending=False)
    results["CORR"] = results["PF"]
    results = results.reset_index()
    return results

# 設定変更後のリロード用


def import_settings():
    g.settings = import_setting()
    g.corrDf = import_corrDf()
    import_data(False)
    start_id = searchDayInd1_(
        g.dfSelectList[0].reset_index(), g.settings["start_date"])
    finish_id = searchDayInd1_(
        g.dfSelectList[0].reset_index(), g.settings["finish_date"])
    g.date_list = g.dfSelectList[0].iloc[start_id:finish_id].index


def import_setting():
    w_wide, w_high = view.MovePositionButton().move_position()
    print(f"モニター幅:{w_wide} モニター高さ:{w_high}")
    w_wide_half = int(w_wide / 2)
    w_high_half = int(w_high / 2)
    period = 1440
    start_date = "2017-01-05",
    finish_date = "2023-01-27",
    setting = {
        "period": str(period),
        "start_date": start_date,
        "finish_date": finish_date,
        "sequence": 700,
        "trade_line": 0.2,
        "pair": ["USDJPY", "GBPJPY", "AUDJPY", "EURJPY", "CADJPY", "NZDJPY", "CHFJPY", "SGDJPY", "MXNJPY", "ZARJPY", "TRYJPY", "SEKJPY", "EURUSD", "GBPUSD", "GBPAUD", "NZDUSD", "AUDUSD", "EURGBP", "EURAUD", "AUDNZD", "USDCAD", "USDCHF", "EURCHF", "GBPCHF"],
        "convert_currency": ["EURUSD", "GBPUSD", "GBPAUD", "NZDUSD", "AUDUSD", "EURGBP", "EURAUD", "AUDNZD", "USDCAD", "USDCHF", "EURCHF", "GBPCHF"],
        "data_dir": "./data/"+str(period)+"min/",
        "df_dir": "./data/calc_maxmin_df/",
        "corrDf_dir": "./data/SimulationResult_700_20100105-20171231_v1.csv",
        "w_wide": w_wide,
        "w_high": w_high,
        "w_wide_half": w_wide_half,
        "w_high_half": w_high_half,
    }
    return setting
