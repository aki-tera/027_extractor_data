import json
import csv

import glob
import pandas as pd
from pandas.core.series import Series
from pandas.core.frame import DataFrame
import matplotlib.pyplot as plt
from matplotlib import cm

# 日本語フォント設定
from matplotlib import rc
jp_font = "Yu Gothic"
rc('font', family=jp_font)

# PEP8に準拠するとimportが先頭に行くので苦肉の策
while True:
    import sys
    sys.path.append("../000_mymodule/")
    import logger
    from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
    DEBUG_LEVEL = DEBUG
    break

def separate_index(list):
    """Split a chunk of index into a list.
    Args:
        list (list): a chunk of index
    Return:
        list:((1, 2, 3), (5, 6)) <-- (1, 2, 3, 5, 6)
    """
    result = []
    val_pre = 0
    for i, val in enumerate(list):
        if i == 0:
            # 1回目は値を保持するのみ
            temp = [val]
        elif val - val_pre < 2:
            # 値が連続している場合、値を連続で保持する
            temp.append(val)
        else:
            # 値が連続していない場合、結果を取り出す
            result.append(temp)
            temp = [val]
        # 前の値として保存する
        val_pre = val
    # 最後のみ残りの部分を保存する
    result.append(temp)

    return(result)

def plot_graph(pg_df, pg_title_text, pg_plane=True):
    """plot pandas DataFrame on the graph(s).
    Args:
        pg_df (pandas.DataFrame or pandas.Series): Data to be graphed.
        pg_title_text (str): title
        pg_plane (bool, optional): Choose between a single graph or multiple graphs.
                                   Defaults to True.
    """
    fig = plt.figure(figsize=(10, 6))
    if pg_plane:
        if type(pg_df) == DataFrame:
            ax_1 = fig.add_subplot()
            ax_2 = ax_1.twinx()
            # 色の設定
            color_1 = cm.Set1.colors[1]
            color_2 = cm.Set1.colors[4]
            # 表示
            # 色はcm, 前後の指示はzorder, 線幅はlinewidth
            # エラーが発生した場合はグラフは1個のみ表示
            pg_df.iloc[:, 0].plot(ax=ax_1, color=color_1, zorder=-2, linewidth=2)
            pg_df.iloc[:, 1].plot(ax=ax_2, color=color_2, zorder=-1, linewidth=0.5)
            # グラフの凡例をまとめる
            handler_1, label_1 = ax_1.get_legend_handles_labels()
            handler_2, label_2 = ax_2.get_legend_handles_labels()
            _ = ax_2.legend(handler_1 + handler_2, label_1 + label_2)
            # タイトルとグリッド表示
            _ = ax_1.set_title(pg_title_text)
            _ = ax_1.grid(True)
        elif type(pg_df) == Series:
            ax = fig.add_subplot()
            pg_df.plot(ax=ax)
            _ = ax.legend()
            # タイトルとグリッド表示
            _ = ax.set_title(pg_title_text)
            _ = ax.grid(True)
        else:
            raise Exception("pandasの型式ではありません。")
        
    else:
        ax = fig.subplots(3, 3)
        plt.suptitle(pg_title_text)
        ax_f = ax.flatten()
        for i, m in enumerate(pg_df):
            ax_f[i].plot(pg_df[m])
            _ = ax_f[i].set_title(m)
            _ = ax_f[i].grid(True)
        # グラフの重なりをなくす為に必要
        plt.tight_layout()
    plt.show()