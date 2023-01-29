
import global_value as g
import setting
import calculation
import pandas as pd
from tkinter import messagebox
import warnings
warnings.simplefilter('ignore')


def import_df(file):
    df = pd.DataFrame()
    df["T1"] = [0, 1, 2, 3]
    df["T2"] = ["a", "b", "c", "d"]
    df["T3"] = ["#", "$", "%", "&"]
    return df


def next_func(mes="Push Next Button"):
    g.ind += 1
    print("Click button : next_func")
    insert_log(mes)
    g.today_df, g.sort_diff = setting.merge_df_today()
    update_benefit()
    # 保持ポジションウィンドウ更新
    update_position()
    # 候補ウィンドウ更新
    update_candidate()


def next_multi_func():
    print("Click button : next_multi_func")
    print_log = f"Push {g.step}step-Next Button"
    insert_log(print_log)
    for i in range(g.step):
        mes = f" ->{i}step"
        next_func(mes)


def insert_log(mes):
    mes = mes.replace(" ", "　")
    g.tree_log.insert("", "end", values=(mes))


def delete_tree(tree):
    for i in tree.get_children():
        tree.delete(i)


def insert_position(df):
    for i in range(len(df)):
        p = df.iloc[i]
        g.tree_position.insert("", "end", values=(
            p["flag"], p["corrDf_num"],  p["benefit"], p["close_tradeDiff"], p["target_profit"],  p["pair1"], p["pair2"], p["pair3"], p["pair4"], p["tradeDiff"], p["tradePrice1"], p["tradePrice2"], p["tradePrice3"], p["tradePrice4"], (p["swap1"]+p["swap2"]+p["swap3"]+p["swap4"]), p["close_norm1"], p["close_norm2"], p["tradeDay"], p["tradeLots1"], p["cost"], p["closeDay"], p["tradePeriod"], p["closePrice1"], p["closePrice2"], p["closePrice3"], p["closePrice4"], p["benefit1"], p["benefit2"], p["benefit3"], p["benefit4"]))


def update_position():
    print("update_position")
    delete_tree(g.tree_position)
    insert_position(g.positions)


def select_position(event):
    print("select_position")
    record_id = g.tree_position.focus()
    record_values = g.tree_position.item(record_id, 'values')
    position, check = searchPosition(
        int(float(record_values[1])), record_values[17])
    insert_df = g.dfSelectList[int(
        float(record_values[1]))].loc[g.date_list[g.ind]]

    g.positions = g.positions.append(position, ignore_index=True)
    pass


def select_candidate(event):
    print("select_candidate")
    # 選択行の判別
    record_id = g.tree_candidate.focus()
    # 選択行のレコードを取得
    record_values = g.tree_candidate.item(record_id, 'values')
    insert_df = g.dfSelectList[int(record_values[1])].loc[g.date_list[g.ind]]
    print(int(float(record_values[1])), g.date_list[g.ind])
    position, check = searchPosition(
        int(float(record_values[1])), g.date_list[g.ind])
    if check != 0:
        g.positions = g.positions.append(position, ignore_index=True)
        insert_log("同じ日に同じポジションをトレードすることはできません。")
        return
    ret = messagebox.askyesno('取引', f'{record_values[1]}を取引しますか')
    g.positions = g.positions.append(position, ignore_index=True)
    if ret == True:
        Lots = int(g.settings["initial_money"] / g.settings["up_lot_money"])
        close1 = insert_df[record_values[5]+"_J_Close"]
        close2 = insert_df[record_values[6]+"_J_Close"]
        if record_values[5] in g.settings["convert_currency"]:
            convert_1c = record_values[5][3:]+"JPY"
            close3 = insert_df[convert_1c+"_Close"]
        else:
            convert_1c = "None"
            close3 = 0
        if record_values[6] in g.settings["convert_currency"]:
            convert_2c = record_values[6][3:]+"JPY"
            close4 = insert_df[convert_2c+"_Close"]
        else:
            convert_2c = "None"
            close4 = 0
        if close3 != 0:
            if insert_df[record_values[5]+'_CLOSE_NORM'] > insert_df[record_values[6]+'_CLOSE_NORM']:
                close1 -= 0.00015
                close3 -= 0.015
            else:
                close1 += 0.00015
                close3 += 0.015
            cost1 = (close1 * close3 * Lots * g.settings["base_lot"] / 25)
            cost3 = (close3 * Lots*g.settings["base_lot"] / 25)
        else:
            if insert_df[record_values[5]+'_CLOSE_NORM'] > insert_df[record_values[6]+'_CLOSE_NORM']:
                close1 -= 0.015
            else:
                close1 += 0.015
            cost1 = (close1 * Lots * g.settings["base_lot"] / 25)
            cost3 = 0
        if close4 != 0:
            if insert_df[record_values[5]+'_CLOSE_NORM'] > insert_df[record_values[6]+'_CLOSE_NORM']:
                close2 += 0.00015
                close4 += 0.015
            else:
                close2 -= 0.00015
                close4 -= 0.015
            cost2 = (close2 * close4 * Lots * g.settings["base_lot"] / 25)
            cost4 = (close4 * Lots*g.settings["base_lot"] / 25)
        else:
            if insert_df[record_values[5]+'_CLOSE_NORM'] > insert_df[record_values[6]+'_CLOSE_NORM']:
                close2 += 0.015
            else:
                close2 -= 0.015
            cost2 = (close2 * Lots * g.settings["base_lot"] / 25)
            cost4 = 0
        cost = cost1 + cost2 + cost3 + cost4
        if insert_df[record_values[5]+'_CLOSE_NORM'] > insert_df[record_values[6]+'_CLOSE_NORM']:
            flag = 1
            s1s = "SELL"
            s2s = "BUY"
            swap1 = g.sell_swap[record_values[5]]
            swap2 = g.buy_swap[record_values[6]]
            swap3 = g.sell_swap[convert_1c]
            swap4 = g.buy_swap[convert_2c]
        else:
            flag = 2
            s1s = "BUY"
            s2s = "SELL"
            swap1 = g.buy_swap[record_values[5]]
            swap2 = g.sell_swap[record_values[6]]
            swap3 = g.buy_swap[convert_1c]
            swap4 = g.sell_swap[convert_2c]
        total_swap_prediction = (swap1*Lots*g.settings["base_lot"])+(swap2*Lots*g.settings["base_lot"])+(
            swap3*Lots*g.settings["base_lot"])+(swap4*Lots*g.settings["base_lot"])
        if g.settings["initial_money"]*0.3 < g.settings["money"]-cost:
            p = calculation.insert_position(record_values[5],
                                            record_values[6],
                                            convert_1c,
                                            convert_2c,
                                            insert_df['CLOSE_NORM_DIFF'],
                                            close1, close2, close3, close4,
                                            swap1, swap2, swap3, swap4,
                                            insert_df[record_values[5] +
                                                      '_CLOSE_NORM'],
                                            insert_df[record_values[6] +
                                                      '_CLOSE_NORM'],
                                            g.date_list[g.ind], Lots *
                                            g.settings["base_lot"],
                                            Lots *
                                            g.settings["base_lot"], Lots *
                                            g.settings["base_lot"],
                                            Lots * g.settings["base_lot"],
                                            int(record_values[1]),
                                            g.settings["target_profit"]*Lots,
                                            cost, flag
                                            )
            g.settings["money"] -= cost
            logs = "{}|Trade No.{} | S1-{}:{} S2-{}:{} S3-{}:{} S4-{}:{} | Cost:{}".format(
                g.date_list[g.ind], int(record_values[1]), s1s, record_values[5], s2s, record_values[6], s1s, convert_1c, s2s, convert_2c, int(cost))
            insert_log(logs)
            g.positions = g.positions.append(p, ignore_index=True)
            update_position()
        else:
            print("Out of money!")
            insert_log("Out of money!")
    else:
        return


def insert_candidate(df, sort_diff):
    show_limit = 30
    if show_limit == -1:
        show_limit = len(df)
    for i in (sort_diff[:show_limit]):
        df_ = df[i]
        key = list(df_.keys())
        S1 = key[0][:6]
        S2 = key[5][:6]
        if S1 in g.settings["convert_currency"]:
            convert_1c = S1[3:]+"JPY"
        else:
            convert_1c = "None"
        if S2 in g.settings["convert_currency"]:
            convert_2c = S2[3:]+"JPY"
        else:
            convert_2c = "None"
        if df_[S1+'_CLOSE_NORM'] > df_[S2+'_CLOSE_NORM']:
            swap1 = g.sell_swap[S1]
            swap2 = g.buy_swap[S2]
            swap3 = g.sell_swap[convert_1c]
            swap4 = g.buy_swap[convert_2c]
        else:
            swap1 = g.buy_swap[S1]
            swap2 = g.sell_swap[S2]
            swap3 = g.buy_swap[convert_1c]
            swap4 = g.sell_swap[convert_2c]
        g.tree_candidate.insert("", "end", values=(
            df_['Date'], df_['No'], df_[
                'CLOSE_NORM_DIFF'], df_['CLOSE_NORM_DIFF_PREV'],
            df_['CLOSE_NORM_DIFF_DIFF'], S1, S2, df_[S1+'_Close'],
            df_[S2+'_Close'], df_[S1+'_J_Close'], df_[S2 + '_J_Close'],
            swap1, swap2, swap3, swap4,
            df_['CLOSE_ZSCORE_DIFF'], df_['CLOSE_ZSCORE_DIFF_PREV'],
            df_['CLOSE_ZSCORE_DIFF_DIFF'], df_[S1+'_CLOSE_NORM'],
            df_[S2+'_CLOSE_NORM'], df_['TODAY_BENEFIT'], df_['TODAY_BENEFIT_TOTAL']))


def update_candidate():
    delete_tree(g.tree_candidate)
    insert_candidate(g.today_df, g.sort_diff)


def insert_result(df):
    for i in range(len(df)):
        g.tree_result.insert("", "end", values=(
            df['T1'][i], df['T2'][i], df['T3'][i]))


def update_result():
    delete_tree(g.tree_result)
    df = import_df("result")
    insert_result(df)


def searchPosition(id, day):
    print(id, day)
    if len(g.positions) == 0:
        return [], 0
    exist_check_df = g.positions[g.positions["flag"] != -1.0]
    exist_check_df = exist_check_df[exist_check_df["corrDf_num"] == id]
    exist_check_df = exist_check_df[exist_check_df["tradeDay"] == day]
    check = len(exist_check_df)
    g.positions = g.positions.drop(list(exist_check_df.index))
    return exist_check_df, check


def update_benefit():
    for i in range(len(g.positions)):
        id = int(float(g.positions.iloc[i]["corrDf_num"]))
        flag = g.positions.iloc[i]["flag"]
        calculation.update_benefit_calc(i, flag, id)
