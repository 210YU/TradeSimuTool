import global_value as g
import calculation
import pandas as pd
import view
import datetime as dt
import numpy as np
# 設定変更後のリロード用


def import_settings():
    g.settings = import_setting()
    g.corrDf = import_corrDf()
    import_data(False)
    start_id = searchDayInd1_(
        g.dfSelectList[0].reset_index(), g.settings["start_date"])
    finish_id = searchDayInd1_(
        g.dfSelectList[0].reset_index(), g.settings["finish_date"])
    g.date_list = g.dfSelectList[0].copy().iloc[start_id:finish_id].index
    g.ind = 0
    g.today_df, g.sort_diff = merge_df_today()
    g.positions = pd.DataFrame()
    g.result = pd.DataFrame()
    g.total_list = []
    g.total_all_list = []
    # 途中から開始する場合
    # if load_dir != "":
    #   g.settings = load_settings()


def import_setting():
    w_wide, w_high = view.MovePositionButton().move_position()
    w_wide = int(w_wide * 0.99)
    w_high = int(w_high * 0.98)
    print(f"モニター幅:{w_wide} モニター高さ:{w_high}")
    w_wide_half = int(w_wide / 2)
    w_high_half = int(w_high / 2)
    period = 1440
    start_date = "2017-01-05",
    finish_date = "2023-01-27",
    initial_money = 300000
    total_benefit = 0
    up_lot_money = 100000
    base_lot = 1000
    target_profit = 200
    setting = {
        "initial_money": initial_money,
        "money": initial_money,
        "total_benefit": total_benefit,
        "period": str(period),
        "base_lot": base_lot,
        "up_lot_money": up_lot_money,
        "target_profit": target_profit,
        "start_date": start_date,
        "finish_date": finish_date,
        "sequence": 700,
        "trade_line": 0.2,
        "pair": ["USDJPY", "GBPJPY", "AUDJPY", "EURJPY", "CADJPY", "NZDJPY", "CHFJPY", "SGDJPY", "MXNJPY", "ZARJPY", "TRYJPY", "SEKJPY", "EURUSD", "GBPUSD", "GBPAUD", "NZDUSD", "AUDUSD", "EURGBP", "EURAUD", "AUDNZD", "USDCAD", "USDCHF", "EURCHF", "GBPCHF"],
        "convert_currency": ["EURUSD", "GBPUSD", "GBPAUD", "NZDUSD", "AUDUSD", "EURGBP", "EURAUD", "AUDNZD", "USDCAD", "USDCHF", "EURCHF", "GBPCHF"],
        "data_dir": "./data/"+str(period)+"min/",
        "df_dir": "./data/calc_maxmin_df/"+str(period)+"min/",
        "corrDf_dir": "./data/SimulationResult_700_20100105-20171231_v1.csv",
        "w_wide": w_wide,
        "w_high": w_high,
        "w_wide_half": w_wide_half,
        "w_high_half": w_high_half,
    }
    g.buy_swap = {"None": 0, "USDJPY": 0.0151, "GBPJPY": 0.0125, "AUDJPY": 0.0065, "EURJPY": 0.0075, "CADJPY": 0.0100, "NZDJPY": 0.0080, "CHFJPY": 0.0035, "SGDJPY": 0.0070, "EURUSD": -0.0073, "GBPUSD": -0.0016,
                  "GBPAUD": -0.0015, "NZDUSD": -0.0013, "AUDUSD": -0.0014, "EURGBP": -0.0042, "EURAUD": -0.0050, "AUDNZD": 0, "USDCAD": 0, "USDCHF": 0.0109, "EURCHF": -0.0018, "GBPCHF": 0.0064}
    g.sell_swap = {"None": 0, "USDJPY": -0.0151, "GBPJPY": -0.0125, "AUDJPY": -0.0065, "EURJPY": -0.0075, "CADJPY": -0.0100, "NZDJPY": -0.0080, "CHFJPY": -0.0035, "SGDJPY": -0.0070, "EURUSD": 0.0072, "GBPUSD": 0.0015,
                   "GBPAUD": 0.0014, "NZDUSD": 0.0012, "AUDUSD": 0.0013, "EURGBP": 0.0041, "EURAUD": 0.0049, "AUDNZD": 0, "USDCAD": 0, "USDCHF": -0.0110, "EURCHF": 0.0017, "GBPCHF": -0.0065}
    return setting


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


def merge_df_today():
    today_df = []
    norm_list = []
    for i in range(len(g.dfSelectList)):
        a = g.dfSelectList[i].loc[g.date_list[g.ind]]
        a["Date"] = g.date_list[g.ind]
        a["No"] = i
        today_df.append(dict(a))
        norm_list.append(a["CLOSE_NORM_DIFF"])
    sort_diff = list(reversed(np.argsort(norm_list)))
    return today_df, sort_diff
