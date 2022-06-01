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