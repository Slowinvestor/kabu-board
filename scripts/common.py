"""
config/stocks.csv を読み込む共通モジュール。fetch.py と build.py の両方から使う。

CSVの各列の意味：
- code           … 証券コード（4桁）。CSVファイル名やグラフのラベルに使う。例）8035
- ticker         … データ取得用の記号。東証は「コード.T」。例）8035.T（空欄ならコードから自動で .T を付ける）
- name           … 表示名。グラフのタイトルや凡例に出る。例）東京エレクトロン
- watch          … ①様子見ライン（円）。現在値の下に引く注意ライン。空欄なら線を引かない
- exit           … ②撤退ライン（円）。構造的な支持線。空欄なら線を引かない
- diagnosis_date … その①②を決めた診断日。記録用（グラフには出さない）。例）2026-08-04
- memo           … 自由メモ。記録用（グラフには出さない）

数字（watch/exit）は「52500」のようにカンマなしで書くこと（CSVはカンマ区切りのため）。
"""

import os
import pandas as pd


def _to_number(v):
    """文字列を数値に。空欄や不正値は None。整数ならintで返す。"""
    v = str(v).strip().replace(",", "")
    if v == "" or v.lower() == "nan":
        return None
    try:
        f = float(v)
    except ValueError:
        return None
    return int(f) if f.is_integer() else f


def load_stocks(base):
    """config/stocks.csv を読み、銘柄ごとの辞書のリストを返す。"""
    path = os.path.join(base, "config", "stocks.csv")
    # utf-8-sig にしておくとExcel保存（BOM付き）でも文字化けしない
    df = pd.read_csv(path, dtype=str, encoding="utf-8-sig").fillna("")
    df.columns = [c.strip() for c in df.columns]

    stocks = []
    for _, row in df.iterrows():
        code = str(row.get("code", "")).strip()
        if not code:
            continue  # 空行はスキップ
        ticker = str(row.get("ticker", "")).strip() or f"{code}.T"
        stocks.append({
            "code": code,
            "ticker": ticker,
            "name": str(row.get("name", "")).strip() or code,
            "watch": _to_number(row.get("watch", "")),
            "exit": _to_number(row.get("exit", "")),
            "diagnosis_date": str(row.get("diagnosis_date", "")).strip(),
            "memo": str(row.get("memo", "")).strip(),
        })
    if not stocks:
        raise RuntimeError("config/stocks.csv に有効な銘柄がありません")
    return stocks
