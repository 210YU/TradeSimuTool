import function
from view import *
import pandas as pd
import numpy as np
import global_value as g


def calc_maxmin_df():
    start_date = g.settings["start_date"]
    sequence = g.settings["sequence"]
    trade_line = g.settings["trade_line"]
    dfSelectList = []
    for l in range(len(g.corrDf)):
        # print(l,"/",len(corrDf))
        stockId1 = str((g.corrDf.iloc[l]["PAIR1"]))
        stockId2 = str((g.corrDf.iloc[l]["PAIR2"]))
        corr = g.corrDf.iloc[l]["CORR"]
        if stockId1 in g.settings["convert_currency"]:
            convert_1c = stockId1[3:]+"JPY"
        else:
            convert_1c = ""
        if stockId2 in g.settings["convert_currency"]:
            convert_2c = stockId2[3:]+"JPY"
        else:
            convert_2c = ""
        dfMulti1_ = pd.read_csv(
            g.settings["data_dir"] + stockId1 + str(g.settings["period"])+".csv")
        dfMulti1 = dfMulti1_.rename(columns={'Open': stockId1+'_Open', 'High': stockId1+'_High', 'Low': stockId1+'_Low',
                                    'Close': stockId1+'_Close', 'Volume': stockId1+'_Volume'}).iloc[:, [0, 1, 2, 3, 4, 5]].set_index("Date")
        dfMulti2_ = pd.read_csv(
            g.settings["data_dir"] + stockId2 + str(g.settings["period"])+".csv")
        dfMulti2 = dfMulti2_.rename(columns={'Open': stockId2+'_Open', 'High': stockId2+'_High', 'Low': stockId2+'_Low',
                                    'Close': stockId2+'_Close', 'Volume': stockId2+'_Volume'}).iloc[:, [0, 1, 2, 3, 4, 5]].set_index("Date")
        dfMulti3 = dfMulti1.join(dfMulti2)
        if stockId1 in g.settings["convert_currency"]:
            dfMulti1J = pd.read_csv(
                g.settings["data_dir"] + stockId1 + str(g.settings["period"])+"_.csv")
            dfMulti1J = dfMulti1J.rename(columns={'Open': stockId1+'_J_Open', 'High': stockId1+'_J_High', 'Low': stockId1+'_J_Low',
                                         'Close': stockId1+'_J_Close', 'Volume': stockId1+'_J_Volume'}).iloc[:, [0, 1, 2, 3, 4, 5]].set_index("Date")
            dfMulti3 = dfMulti3.join(dfMulti1J)
            if stockId2 != convert_1c and convert_1c != convert_2c:
                dfMulti1C = pd.read_csv(
                    g.settings["data_dir"] + convert_1c + str(g.settings["period"])+".csv")
                dfMulti1C = dfMulti1C.rename(columns={'Open': convert_1c+'_Open', 'High': convert_1c+'_High', 'Low': convert_1c+'_Low',
                                             'Close': convert_1c+'_Close', 'Volume': convert_1c+'_Volume'}).iloc[:, [0, 1, 2, 3, 4, 5]].set_index("Date")
                dfMulti3 = dfMulti3.join(dfMulti1C)
        else:
            dfMulti1J = dfMulti1_.rename(columns={'Open': stockId1+'_J_Open', 'High': stockId1+'_J_High', 'Low': stockId1+'_J_Low',
                                         'Close': stockId1+'_J_Close', 'Volume': stockId1+'_J_Volume'}).iloc[:, [0, 1, 2, 3, 4, 5]].set_index("Date")
            dfMulti3 = dfMulti3.join(dfMulti1J)
        if stockId2 in g.settings["convert_currency"]:
            dfMulti2J = pd.read_csv(
                g.settings["data_dir"] + stockId2 + str(g.settings["period"])+"_.csv")
            dfMulti2J = dfMulti2J.rename(columns={'Open': stockId2+'_J_Open', 'High': stockId2+'_J_High', 'Low': stockId2+'_J_Low',
                                         'Close': stockId2+'_J_Close', 'Volume': stockId2+'_J_Volume'}).iloc[:, [0, 1, 2, 3, 4, 5]].set_index("Date")
            dfMulti3 = dfMulti3.join(dfMulti2J)
            if stockId1 != convert_2c and convert_1c != convert_2c:
                dfMulti2C = pd.read_csv(
                    g.settings["data_dir"] + convert_2c + str(g.settings["period"])+".csv")
                dfMulti2C = dfMulti2C.rename(columns={'Open': convert_2c+'_Open', 'High': convert_2c+'_High', 'Low': convert_2c+'_Low',
                                             'Close': convert_2c+'_Close', 'Volume': convert_2c+'_Volume'}).iloc[:, [0, 1, 2, 3, 4, 5]].set_index("Date")
                dfMulti3 = dfMulti3.join(dfMulti2C)
        else:
            dfMulti2J = dfMulti2_.rename(columns={'Open': stockId2+'_J_Open', 'High': stockId2+'_J_High', 'Low': stockId2+'_J_Low',
                                         'Close': stockId2+'_J_Close', 'Volume': stockId2+'_J_Volume'}).iloc[:, [0, 1, 2, 3, 4, 5]].set_index("Date")
            dfMulti3 = dfMulti3.join(dfMulti2J)
        if convert_1c != "" and convert_2c != "" and convert_1c == convert_2c:
            dfMulti3C = pd.read_csv(
                g.settings["data_dir"] + convert_2c + str(g.settings["period"])+".csv")
            dfMulti3C = dfMulti3C.rename(columns={'Open': convert_2c+'_Open', 'High': convert_2c+'_High', 'Low': convert_2c+'_Low',
                                         'Close': convert_2c+'_Close', 'Volume': convert_2c+'_Volume'}).iloc[:, [0, 1, 2, 3, 4, 5]].set_index("Date")
            dfMulti3 = dfMulti3.join(dfMulti3C)
        dfMulti3 = dfMulti3.reset_index()
        dfMulti3['Date'] = dfMulti3['Date'].apply(
            lambda x: pd.to_datetime(x).strftime('%Y-%m-%d'))
        dfMulti3 = dfMulti3.set_index("Date")
        start_id = function.searchDayInd1_(dfMulti3.reset_index(), start_date)
        dfMulti3 = dfMulti3[start_id:]
        dfSelect = maxmin_normalization(
            dfMulti3, stockId1, stockId2, sequence, trade_line)
        dfSelect = calc_benefit_df(
            dfSelect, stockId1, stockId2, g.settings["convert_currency"])
        dfSelectList.append(dfSelect)
        dfSelect.to_pickle("../data/calc_maxmin_df/"+str(i)+".pickle")

    return dfSelectList


def maxmin_normalization(dfMulti3, stockId1, stockId2, sequence_length, trade_line_n=0.5, trade_line_z=0.5, delay=1):
    df = dfMulti3.copy()
    sma = 10
    mm1 = [0, ]*(sequence_length+delay)
    mm2 = [0, ]*(sequence_length+delay)
    zm1 = [0, ]*(sequence_length+delay)
    zm2 = [0, ]*(sequence_length+delay)
    rsi = [0, ]*(sequence_length+delay)
    rsi_z = [0, ]*(sequence_length+delay)
    for i in range(sequence_length+delay, len(df)):
        close_seq1 = df.iloc[i-sequence_length -
                             delay:i-delay][stockId1+"_Close"]
        close_seq2 = df.iloc[i-sequence_length -
                             delay:i-delay][stockId2+"_Close"]
        close_max1 = close_seq1.max()
        close_max2 = close_seq2.max()
        close_min1 = close_seq1.min()
        close_min2 = close_seq2.min()
        close_mean1 = close_seq1.mean()
        close_mean2 = close_seq2.mean()
        close_std1 = close_seq1.std()
        close_std2 = close_seq2.std()

        close_mm1 = (close_seq1 - close_min1) / (close_max1 - close_min1)
        close_mm2 = (close_seq2 - close_min2) / (close_max2 - close_min2)
        close_zm1 = (close_seq1 - close_mean1) / close_std1
        close_zm2 = (close_seq2 - close_mean2) / close_std2

        mm1.append(float(close_mm1[-1]))
        mm2.append(float(close_mm2[-1]))
        zm1.append(float(close_zm1[-1]))
        zm2.append(float(close_zm2[-1]))

    df[stockId1+"_CLOSE_NORM"] = mm1
    df[stockId2+"_CLOSE_NORM"] = mm2
    df[stockId1+"_CLOSE_ZSCORE"] = zm1
    df[stockId2+"_CLOSE_ZSCORE"] = zm2
    df["CLOSE_NORM_DIFF"] = np.abs(
        df[stockId1+"_CLOSE_NORM"] - df[stockId2+"_CLOSE_NORM"])
    df["CLOSE_NORM_DIFF_PREV"] = df["CLOSE_NORM_DIFF"].shift(1)
    df["CLOSE_NORM_DIFF_DIFF"] = df["CLOSE_NORM_DIFF"] - \
        df["CLOSE_NORM_DIFF_PREV"]
    df["CLOSE_ZSCORE_DIFF"] = np.abs(
        df[stockId1+"_CLOSE_ZSCORE"] - df[stockId2+"_CLOSE_ZSCORE"])
    df["CLOSE_ZSCORE_DIFF_PREV"] = df["CLOSE_ZSCORE_DIFF"].shift(1)
    df["CLOSE_ZSCORE_DIFF_DIFF"] = df["CLOSE_ZSCORE_DIFF"] - \
        df["CLOSE_ZSCORE_DIFF_PREV"]
    df["SIGNAL_NORM"] = np.where(df["CLOSE_NORM_DIFF"].shift(
        1) < trade_line_n, np.where(df["CLOSE_NORM_DIFF"] > trade_line_n, 1, 0), 0)
    df["SIGNAL_ZSCORE"] = np.where(df["CLOSE_ZSCORE_DIFF"].shift(
        1) < trade_line_z, np.where(df["CLOSE_ZSCORE_DIFF"] > trade_line_z, 1, 0), 0)
    df[stockId1+"_SMA_20"] = df[stockId1+"_Close"].rolling(sma).mean()
    df[stockId2+"_SMA_20"] = df[stockId2+"_Close"].rolling(sma).mean()
    df["SMA_DIFF"] = np.abs(
        np.log(df[stockId1+"_SMA_20"] / df[stockId2+"_SMA_20"]))
    df["CLOSE_DIFF"] = np.abs(df[stockId1+"_SMA_20"] - df[stockId2+"_SMA_20"])
    #df["SMA_DIFF"] = np.abs(np.log(df[stockId1+"_Close"] / df[stockId2+"_Close"]))
    df["SMA_DIFF_SMA"] = df["SMA_DIFF"].rolling(sma).mean()
    df["SMA_SMA_PREV"] = df["SMA_DIFF_SMA"].shift(1)
    df["STD"] = df["SMA_DIFF_SMA"].rolling(sma).std()
    df["BB+2"] = df["SMA_DIFF_SMA"]+(df["STD"]*2)
    df["BB+3"] = df["SMA_DIFF_SMA"]+(df["STD"]*3)
    df["BB+4"] = df["SMA_DIFF_SMA"]+(df["STD"]*4)
    df["BB+1"] = df["SMA_DIFF_SMA"]+(df["STD"]*1)
    df["BB-2"] = df["SMA_DIFF_SMA"]-(df["STD"]*2)
    df["BB-3"] = df["SMA_DIFF_SMA"]-(df["STD"]*3)
    df["BB-4"] = df["SMA_DIFF_SMA"]-(df["STD"]*4)
    df["BB-1"] = df["SMA_DIFF_SMA"]-(df["STD"]*1)
    df["BBUP"] = np.where(df["SMA_DIFF"] > df["BB+2"], 1, 0)
    df[stockId1+"_3UP"] = np.where(df[stockId1+"_Open"].shift(1) < df[stockId1+"_Close"].shift(
        1), np.where(df[stockId1+"_Open"] < df[stockId1+"_Close"], 1, 0), 0)
    df[stockId2+"_3UP"] = np.where(df[stockId2+"_Open"].shift(1) < df[stockId2+"_Close"].shift(
        1), np.where(df[stockId2+"_Open"] < df[stockId2+"_Close"], 1, 0), 0)
    df[stockId1+"_3DOWN"] = np.where(df[stockId1+"_Open"].shift(1) > df[stockId1+"_Close"].shift(
        1), np.where(df[stockId1+"_Open"] > df[stockId1+"_Close"], 1, 0), 0)
    df[stockId2+"_3DOWN"] = np.where(df[stockId2+"_Open"].shift(1) > df[stockId2+"_Close"].shift(
        1), np.where(df[stockId2+"_Open"] > df[stockId2+"_Close"], 1, 0), 0)
    """
    df[stockId1+"_3UP"] = np.where(df[stockId1+"_Open"].shift(2)<df[stockId1+"_Close"].shift(2),np.where(df[stockId1+"_Open"].shift(1)<df[stockId1+"_Close"].shift(1),np.where(df[stockId1+"_Open"]<df[stockId1+"_Close"],1,0),0),0)
    df[stockId2+"_3UP"] = np.where(df[stockId2+"_Open"].shift(1)<df[stockId2+"_Close"].shift(1),np.where(df[stockId2+"_Open"].shift(1)<df[stockId2+"_Close"].shift(1),np.where(df[stockId2+"_Open"]<df[stockId2+"_Close"],1,0),0),0)
    df[stockId1+"_3DOWN"] = np.where(df[stockId1+"_Open"].shift(2)>df[stockId1+"_Close"].shift(2),np.where(df[stockId1+"_Open"].shift(1)>df[stockId1+"_Close"].shift(1),np.where(df[stockId1+"_Open"]>df[stockId1+"_Close"],1,0),0),0)
    df[stockId2+"_3DOWN"] = np.where(df[stockId2+"_Open"].shift(2)>df[stockId2+"_Close"].shift(2),np.where(df[stockId2+"_Open"].shift(1)>df[stockId2+"_Close"].shift(1),np.where(df[stockId2+"_Open"]>df[stockId2+"_Close"],1,0),0),0)
    """
    return df


def calc_benefit_df(dfSelect, stockId1, stockId2, convert_currency):
    be = []
    be_sum = []
    sum_ = 0
    ################################
    # DFで格納して結合する
    if stockId1 in convert_currency:
        convert_1c = stockId1[3:]+"JPY"
    else:
        convert_1c = "None"
    if stockId2 in convert_currency:
        convert_2c = stockId2[3:]+"JPY"
    else:
        convert_2c = "None"
    for i in range(len(dfSelect)):
        if dfSelect.iloc[i][stockId1+"_CLOSE_NORM"] == 0 and dfSelect.iloc[i][stockId2+"_CLOSE_NORM"] == 0:
            be.append(0)
            be_sum.append(0)
            continue

        close1 = dfSelect.iloc[i][stockId1+"_J_Close"]
        close2 = dfSelect.iloc[i][stockId2+"_J_Close"]
        open1 = dfSelect.iloc[i-1][stockId1+"_J_Close"]
        open2 = dfSelect.iloc[i-1][stockId2+"_J_Close"]
        if convert_1c != "None":
            close3 = dfSelect.iloc[i][convert_1c+"_Close"]
            open3 = dfSelect.iloc[i-1][convert_1c+"_Close"]
        else:
            close3 = 0.0
        if convert_2c != "None":
            close4 = dfSelect.iloc[i][convert_2c+"_Close"]
            open4 = dfSelect.iloc[i-1][convert_2c+"_Close"]
        else:
            close4 = 0.0
        if np.isnan(close2) or np.isnan(close1):
            be.append(0)
            be_sum.append(0)
            continue

        if dfSelect.iloc[i][stockId1+"_CLOSE_NORM"] < dfSelect.iloc[i][stockId2+"_CLOSE_NORM"]:
            if close3 != 0:
                b1 = (close1 - open1) * close3 * 10000
                b3 = ((close3 - open3) * 10000)
            else:
                b1 = (close1 - open1) * 10000
                b3 = 0
            if close4 != 0:
                b2 = (open2 - close2) * close4 * 10000
                b4 = ((open4 - close4) * 10000)
            else:
                b2 = (open2 - close2) * 10000
                b4 = 0
        else:
            if close3 != 0:
                b1 = (open1 - close1) * close3 * 10000
                b3 = ((open3 - close3) * 10000)
            else:
                b1 = (open1 - close1) * 10000
                b3 = 0
            if close4 != 0:
                b2 = (close2 - open2) * close4 * 10000
                b4 = ((close4 - open4) * 10000)
            else:
                b2 = (close2 - open2) * 10000
                b4 = 0
        b = b1 + b2 + b3 + b4
        if np.isnan(b):
            b = 0
        sum_ += b
        be.append(b)
        be_sum.append(sum_)
    dfSelect["TODAY_BENEFIT"] = be
    dfSelect["TODAY_BENEFIT_TOTAL"] = be_sum
    dfSelect["TODAY_BENEFIT_AVG10"] = dfSelect["TODAY_BENEFIT_TOTAL"].rolling(
        10).mean()

    return dfSelect
