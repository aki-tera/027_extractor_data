import json

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


class ExtractorData():
    """concatenate csv files, extract specific data and save the results to excel.
    """
    
    def __init__(self, json_file_path):
        """read json, set the variables, concatenate csv files and make dataframe.

        Args:
            json_file_path (str): path of the json file.
        """
        # パラメータの取り出し
        with open(json_file_path, "r", encoding="utf-8") as setting:
            self._setting_dict = json.load(setting)
        # 設定jsonから変数へ読み込み
        # ファイル名
        single_file_names = glob.glob(self._setting_dict["file"]["path"] + self._setting_dict["file"]["single"])
        double_file_names = glob.glob(self._setting_dict["file"]["path"] + self._setting_dict["file"]["double"])
        all_file_names = single_file_names + double_file_names
        # 初回プロットの範囲
        self._plot_range_start = self._setting_dict["plot"]["start"]
        self._plot_range_end = self._setting_dict["plot"]["end"]
        # ラベル
        self.label_index = self._setting_dict["label"]
        # 結果データの読み込み
        temp_df_list = []
        for i, j in enumerate(all_file_names):
            # 結果列の名前を判別するための辞書作成
            if i == 0:
                self.dict_label = {"key": "value"}
                with open(j, encoding="cp932")as f:
                    temp_label = f.readlines()[39:41]
                for ii, (m, n) in enumerate(zip(temp_label[0].split(","), temp_label[1].split(","))):
                    
                    if ii > 1:
                        self.dict_label[n.strip().strip('"')] = m.strip()
            temp_df = pd.read_csv(j, skiprows=70, encoding="cp932")
            temp_df_list.append(temp_df)
        # データフレームの結合
        self._df_csv = pd.concat(temp_df_list, ignore_index=False)
        self._df_csv.reset_index(drop=True, inplace=True)

    def confirm_data(self, label_name, display_graph=True):
        """confirm data

        Args:
            label_name (str): the label indicating the target data.
            display_graph (bool, optional): graph display on/off. Defaults to True.
        Returns:
            bool: The target label exists.
        """
        # 列の名称
        try:
            column_name = self.dict_label[label_name]
        except KeyError:
            return False
        else:
            if display_graph:
                # プロットする
                print("取得したデータの確認")
                plot_graph(self._df_csv.loc[self._plot_range_start:self._plot_range_end, column_name],
                           f"読み込んだデータの一部（{self._plot_range_start}～{self._plot_range_end}）を表示")
            return True

    def cut_out_data(self, label_name, display_graph=True):
        """cut out the data which you need.

        Args:
            label_name (str): the label indicating the target data.
            display_graph (bool, optional): graph display on/off. Defaults to True.
        """
        # 列の名称
        column_name = self.dict_label[label_name]
        # 閾値
        range_high = self.label_index[label_name]["high"]
        range_low = self.label_index[label_name]["low"]
        # データ切り分け
        df_temp = self._df_csv[(range_low < self._df_csv[column_name]) & (self._df_csv[column_name] < range_high)]
        # indexの抽出
        pandas_list = df_temp.index
        self.list_index = separate_index(list(pandas_list))
        # 確認用プロットを表示
        if display_graph:
            df_plot_temp = pd.DataFrame(index=[])
            for i, j in enumerate(self.list_index):
                if -1 < i < 9:
                    temp = self._df_csv[j[0]:j[-1]][column_name]
                    temp = temp.reset_index()
                    df_plot_temp[str(i)] = temp[column_name]
            # 一部の切り出した波形を表示
            print("おかしなグラフが無いか確認する")
            plot_graph(df_plot_temp, "おかしなグラフが無いか確認する", pg_plane=False)

    def output_mediun(self, label_name):
        """Calculate the median

        Args:
            label_name (str): the label indicating the target data.
        """
        # 列の名称
        column_name = self.dict_label[label_name]
        # 中央値の算出
        result_mediun = []
        result_endheader = []
        result_time = []
        for i in self.list_index:
            df_temp = self._df_csv.loc[i]
            temp_result = df_temp[column_name].median()
            temp_endheader = self._df_csv.iloc[i[0], 0]
            temp_time = self._df_csv.iloc[i[0], 1]
            result_mediun.append(temp_result)
            result_endheader.append(temp_endheader)
            result_time.append(temp_time)
        # 結果用データフレーム作成（時間、秒、結果）
        self._df_result = pd.DataFrame(list(zip(result_endheader, result_time, result_mediun)), columns=["#EndHeader", "日時(μs)", column_name])

    def write_xlsx(self, label_name, write_mode="w"):
        """write xlsx file.

        Args:
            label_name (str): the label indicating the target data.
            write_mode (str, optional): File mode to use (write or append). Defaults to "w".
        """
        # エクセルへの書き込み
        with pd.ExcelWriter("result.xlsx", engine="openpyxl", mode=write_mode) as writer:
            self._df_result.to_excel(writer, sheet_name=label_name, index=False)


def main():
    data = ExtractorData("setting.json")
    for i, n in enumerate(data.label_index):
        
        if data.confirm_data(n, display_graph=True):
            data.cut_out_data(n, display_graph=True)
            data.output_mediun(n)
            if i == 0:
                data.write_xlsx(n)
            else:
                data.write_xlsx(n, write_mode="a")


if __name__ == "__main__":
    main()
