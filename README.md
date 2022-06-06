# 027_extractor_data

![python3](https://img.shields.io/badge/type-python3-brightgreen)  ![passing](https://img.shields.io/badge/windows%20build-passing-brightgreen) ![MIT](https://img.shields.io/badge/license-MIT-brightgreen)  

## DEMO

**Output Data  <-**  
<img src="https://user-images.githubusercontent.com/44888139/172100508-a9327c7c-4f92-4c51-bb7f-9780c049f6b9.png" width="500px">

**INPUT Data and Setting  ->**  
<img src="https://user-images.githubusercontent.com/44888139/172106787-ce672d0f-887b-40db-b875-8de2133c856c.png" width="500px"> 

**Progress can be checked with graphs**

- Display graphs within the range of values set in setting.json  
<img src="https://user-images.githubusercontent.com/44888139/172105932-a8bd6c5c-63b0-45d0-b8dc-1ce4b97944d6.png" width="300px">   
- And then display a graph of the targets for which the median is calculated.  
- However, only the first 9 items.  
<img src="https://user-images.githubusercontent.com/44888139/172106153-71021afb-9e28-4ab0-be67-23e05965e5e4.png" width="300px"> 

## Features

You can get an excel file that records the median values.

### specification

- You get the median values by some columns from the ranges which you want between high and low.
- You can change the settings by setting file.

### original csv files

- The data needs to be stable data outside the range for a certain period of time.

### output data

- You get an excel file with the median of the column indicated on the label.

## Requirement  

Python 3

- I ran this program with the following execution environment.
  - Python 3.9
  - Windows 10

Python Library

- pandas
- matplotlib
- glob
- json

## Usage

1. You place the csv files in the same folder as this program.
1. Run this program.
1. A few graphs is displayed for confirmation.
1. And then generate result's excell files.

## Note

Nothing in particular

## License

This program is under MIT license.

## 【日本語】

## 機能

複数のcsvファイルから中央値を取得して、エクセルファイルとして出力します。

- 仕様
  - ある範囲のデータを切り出して中央値をまとめて取得します。
  - 設定で列の名称や範囲を指定できます。
- 元のcsvファイル
  - 一定期間の範囲外があるデータが必要です。
- 出力する内容
  - ラベルで指示した名称をシート名にして、エクセルファイルで出力します。