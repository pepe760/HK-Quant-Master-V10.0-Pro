#@title HK Quant Master V10.1 (The Holy Grail + HSI Market Dashboard)
import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import json
import warnings
import time
import math
from tqdm import tqdm

warnings.filterwarnings('ignore')

# ==============================================================================
# 1. 基礎設定與資料獲取
# ==============================================================================
START_DATE = "2000-01-01"
END_DATE = datetime.datetime.now().strftime('%Y-%m-%d')
UPDATE_TIME = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

WATCHLIST = [
    '0001.HK', '0002.HK', '0003.HK', '0005.HK', '0006.HK', '0011.HK', '0012.HK', '0016.HK', '0017.HK', '0020.HK',
    '0027.HK', '0066.HK', '0083.HK', '0101.HK', '0119.HK', '0135.HK', '0144.HK', '0151.HK', '0168.HK', '0175.HK',
    '0200.HK', '0241.HK', '0256.HK', '0267.HK', '0268.HK', '0270.HK', '0272.HK', '0285.HK', '0288.HK', '0291.HK',
    '0316.HK', '0322.HK', '0336.HK', '0345.HK', '0354.HK', '0358.HK', '0386.HK', '0388.HK', '0390.HK', '0460.HK',
    '0520.HK', '0522.HK', '0552.HK', '0576.HK', '0586.HK', '0598.HK', '0604.HK', '0656.HK', '0669.HK', '0688.HK',
    '0700.HK', '0728.HK', '0753.HK', '0762.HK', '0772.HK', '0778.HK', '0780.HK', '0813.HK', '0823.HK', '0836.HK',
    '0853.HK', '0857.HK', '0861.HK', '0868.HK', '0883.HK', '0902.HK', '0909.HK', '0914.HK', '0916.HK', '0934.HK',
    '0939.HK', '0941.HK', '0960.HK', '0968.HK', '0981.HK', '0992.HK', '0998.HK', '1024.HK', '1030.HK', '1038.HK',
    '1044.HK', '1055.HK', '1066.HK', '1071.HK', '1088.HK', '1093.HK', '1099.HK', '1109.HK', '1113.HK', '1119.HK',
    '1138.HK', '1157.HK', '1177.HK', '1193.HK', '1209.HK', '1211.HK', '1258.HK', '1299.HK', '1308.HK', '1313.HK',
    '1316.HK', '1336.HK', '1339.HK', '1347.HK', '1368.HK', '1378.HK', '1398.HK', '1516.HK', '1530.HK', '1658.HK',
    '1772.HK', '1787.HK', '1801.HK', '1810.HK', '1818.HK', '1833.HK', '1876.HK', '1898.HK', '1919.HK', '1928.HK',
    '1929.HK', '1997.HK', '2005.HK', '2007.HK', '2013.HK', '2015.HK', '2018.HK', '2020.HK', '2186.HK', '2192.HK',
    '2202.HK', '2238.HK', '2269.HK', '2313.HK', '2318.HK', '2319.HK', '2331.HK', '2333.HK', '2359.HK', '2380.HK',
    '2388.HK', '2600.HK', '2618.HK', '2628.HK', '2669.HK', '2688.HK', '2689.HK', '2727.HK', '2858.HK', '2866.HK',
    '2869.HK', '2877.HK', '2883.HK', '2899.HK', '3311.HK', '3319.HK', '3323.HK', '3328.HK', '3331.HK', '3606.HK',
    '3618.HK', '3633.HK', '3690.HK', '3692.HK', '3738.HK', '3800.HK', '3868.HK', '3888.HK', '3899.HK', '3900.HK',
    '3908.HK', '3933.HK', '3958.HK', '3968.HK', '3983.HK', '3988.HK', '3990.HK', '3993.HK', '6030.HK', '6098.HK',
    '6110.HK', '6160.HK', '6618.HK', '6690.HK', '6806.HK', '6837.HK', '6862.HK', '6865.HK', '6881.HK', '6969.HK',
    '9618.HK', '9633.HK', '9866.HK', '9868.HK', '9888.HK', '9922.HK', '9959.HK', '9988.HK', '9992.HK', '9999.HK'
]
WATCHLIST = list(set(WATCHLIST))

# 擴充版中文名稱字典
HK_STOCK_NAMES = {
    '0001.HK': '長和', '0002.HK': '中電控股', '0003.HK': '香港中華煤氣', '0005.HK': '匯豐控股', '0006.HK': '電能實業',
    '0011.HK': '恒生銀行', '0012.HK': '恆基地產', '0016.HK': '新鴻基地產', '0017.HK': '新世界發展', '0020.HK': '會德豐',
    '0027.HK': '銀河娛樂', '0066.HK': '港鐵公司', '0083.HK': '信和置業', '0101.HK': '恒隆地產', '0135.HK': '昆侖能源',
    '0144.HK': '招商局港口', '0151.HK': '中國旺旺', '0175.HK': '吉利汽車', '0241.HK': '阿里健康', '0267.HK': '中信股份',
    '0268.HK': '金蝶國際', '0285.HK': '比亞迪電子', '0288.HK': '萬洲國際', '0316.HK': '東方海外實業', '0322.HK': '康師傅控股',
    '0386.HK': '中國石化', '0388.HK': '香港交易所', '0522.HK': 'ASM太平洋', '0669.HK': '創科實業', '0688.HK': '中國海外發展',
    '0700.HK': '騰訊控股', '0728.HK': '中國電信', '0762.HK': '中國聯通', '0823.HK': '領展房產基金', '0836.HK': '華潤電力',
    '0857.HK': '中國石油股份', '0883.HK': '中國海洋石油', '0939.HK': '建設銀行', '0941.HK': '中國移動', '0960.HK': '龍湖集團',
    '0968.HK': '信義光能', '0981.HK': '中芯國際', '0992.HK': '聯想集團', '1038.HK': '長江基建集團', '1044.HK': '恆安國際',
    '1088.HK': '中國神華', '1093.HK': '石藥集團', '1099.HK': '國藥控股', '1109.HK': '華潤置地', '1113.HK': '長實集團',
    '1177.HK': '中國生物製藥', '1211.HK': '比亞迪股份', '1299.HK': '友邦保險', '1398.HK': '工商銀行', '1810.HK': '小米集團-W',
    '1876.HK': '百威亞太', '1928.HK': '金沙中國有限公司', '2018.HK': '瑞聲科技', '2020.HK': '安踏體育', '2269.HK': '藥明生物',
    '2313.HK': '申洲國際', '2318.HK': '中國平安', '2319.HK': '蒙牛乳業', '2331.HK': '李寧', '2382.HK': '舜宇光學科技',
    '2388.HK': '中銀香港', '2600.HK': '中國鋁業', '2628.HK': '中國人壽', '2688.HK': '新奧能源', '2899.HK': '紫金礦業',
    '3328.HK': '交通銀行', '3618.HK': '重慶農商行', '3690.HK': '美團-W', '3968.HK': '招商銀行', '3988.HK': '中國銀行',
    '6098.HK': '碧桂園服務', '6618.HK': '京東健康', '6862.HK': '海底撈', '9618.HK': '京東集團-SW', '9888.HK': '百度集團-SW',
    '9988.HK': '阿里巴巴-SW', '9999.HK': '網易-S'
}

print(f"⏳ 1/5 啟動下載 Agent 獲取市場大數據 (從 2000 年至今)...")

hsi_df = yf.download(["2800.HK", "^HSI", "^VIX"], start=START_DATE, end=END_DATE, progress=False, threads=True)
hsi_c = hsi_df['Close']['2800.HK'].ffill()
if hsi_c.isna().all(): hsi_c = hsi_df['Close']['^HSI'].ffill()

hsi_v = hsi_df['Volume']['2800.HK'].ffill()
if hsi_v.isna().all(): hsi_v = hsi_df['Volume']['^HSI'].ffill()

vix_c = hsi_df['Close']['^VIX'].ffill()

def secured_download_agent(tickers, period_start, period_end):
    prices_dict = {'Open': {}, 'High': {}, 'Low': {}, 'Close': {}}
    for i in range(0, len(tickers), 30):
        batch = tickers[i:i + 30]
        data = yf.download(batch, start=period_start, end=period_end, progress=False, threads=True, group_by='ticker')
        for ticker in batch:
            try:
                df_t = data if len(batch) == 1 else data[ticker]
                if not df_t.empty and not df_t.isna().all().all():
                    prices_dict['Open'][ticker] = df_t['Open']
                    prices_dict['High'][ticker] = df_t['High']
                    prices_dict['Low'][ticker] = df_t['Low']
                    prices_dict['Close'][ticker] = df_t['Close']
            except Exception: pass
        time.sleep(0.5)
    return (pd.DataFrame(prices_dict['Open']).ffill(),
            pd.DataFrame(prices_dict['High']).ffill(),
            pd.DataFrame(prices_dict['Low']).ffill(),
            pd.DataFrame(prices_dict['Close']).ffill())

opens, highs, lows, closes = secured_download_agent(WATCHLIST, START_DATE, END_DATE)

valid_idx = closes.index.drop_duplicates(keep='first').sort_values()
opens = opens.reindex(valid_idx)
highs = highs.reindex(valid_idx)
lows = lows.reindex(valid_idx)
closes = closes.reindex(valid_idx)

hsi_c = hsi_c.reindex(closes.index).ffill()
hsi_v = hsi_v.reindex(closes.index).ffill()
vix_c = vix_c.reindex(closes.index).ffill()

print("⏳ 2/5 計算技術指標、BOLL布林通道與大盤 FTD...")

hsi_200ma = hsi_c.rolling(200).mean()
sma20_all = closes.rolling(20).mean()
std20_all = closes.rolling(20).std()
upper_bb_all = sma20_all + (2 * std20_all)
lower_bb_all = sma20_all - (2 * std20_all)
donchian_high_all = highs.rolling(20).max().shift(1)

ret_120d = closes.pct_change(120)

# RSI 28
rsi_period = 28
delta = closes.diff()
gain = delta.where(delta > 0, 0).ewm(alpha=1/rsi_period, adjust=False).mean()
loss = (-delta.where(delta < 0, 0)).ewm(alpha=1/rsi_period, adjust=False).mean()
rs = gain / loss.replace(0, np.nan)
rsi_all = 100 - (100 / (1 + rs))

# 計算近 1.5 年大盤數據與 FTD (Follow-Through Day)
recent_days = int(252 * 1.5)
recent_hsi_c = hsi_c.iloc[-recent_days:]
recent_hsi_sma = hsi_200ma.iloc[-recent_days:]
recent_hsi_v = hsi_v.iloc[-recent_days:]
recent_hsi_dates = recent_hsi_c.index.strftime('%Y-%m-%d').tolist()

ftd_signals = []
for i in range(1, len(recent_hsi_c)):
    prev_c = recent_hsi_c.iloc[i-1]
    cur_c = recent_hsi_c.iloc[i]
    if pd.isna(prev_c) or pd.isna(cur_c): continue
    pct_change = ((cur_c - prev_c) / prev_c) * 100
    vol_increase = recent_hsi_v.iloc[i] > recent_hsi_v.iloc[i-1]
    
    # 簡易 FTD 判定：單日漲幅大於 1.5% 且成交量放大
    if pct_change >= 1.5 and vol_increase:
        ftd_signals.append({
            "date": recent_hsi_dates[i], 
            "price": round(cur_c, 2),
            "label": f"+{pct_change:.1f}% 量增"
        })

hsi_json_data = {
    "dates": recent_hsi_dates,
    "closes": [round(x, 2) if not pd.isna(x) else null for x in recent_hsi_c],
    "sma200": [round(x, 2) if not pd.isna(x) else null for x in recent_hsi_sma],
    "ftds": ftd_signals
}

fin_cache = {}
def get_fundamentals(ticker):
    if ticker in fin_cache: return fin_cache[ticker]
    try:
        tk_info = yf.Ticker(ticker).info
        raw_div = tk_info.get('dividendYield') or tk_info.get('trailingAnnualDividendYield') or 0
        div = round(raw_div, 2) if raw_div > 1 else round(raw_div * 100, 2)
        earn_growth = tk_info.get('earningsGrowth') or tk_info.get('revenueGrowth') or 0
        earn_pct = round(earn_growth * 100, 2)

        if earn_pct >= 15: earn_label = f"強勁 (+{earn_pct}%)"
        elif earn_pct > 0: earn_label = f"復甦 (+{earn_pct}%)"
        elif earn_pct < 0: earn_label = f"衰退 ({earn_pct}%)"
        else: earn_label = "無"

        pe = round(tk_info.get('trailingPE'), 2) if tk_info.get('trailingPE') else "N/A"
        pb = round(tk_info.get('priceToBook'), 2) if tk_info.get('priceToBook') else "N/A"
        roe = round(tk_info.get('returnOnEquity') * 100, 2) if tk_info.get('returnOnEquity') else "N/A"

        fin_cache[ticker] = {"div": div, "earn_label": earn_label, "pe": pe, "pb": pb, "roe": roe}
    except:
        fin_cache[ticker] = {"div": 0, "earn_label": "無", "pe": "N/A", "pb": "N/A", "roe": "N/A"}
    return fin_cache[ticker]

def safe_list(series):
    return [None if pd.isna(x) else round(float(x), 2) for x in series.tolist()]

def clean_nans(obj):
    if isinstance(obj, dict): return {k: clean_nans(v) for k, v in obj.items()}
    if isinstance(obj, list): return [clean_nans(v) for v in obj]
    if isinstance(obj, float):
        if pd.isna(obj) or math.isnan(obj) or np.isnan(obj) or np.isinf(obj): return None
    return obj

# ==============================================================================
# 3. 實盤回測引擎模組化
# ==============================================================================
print("⏳ 3/5 啟動多重情境回測引擎 (RSI 28/25 + Turtle)...")

def run_backtest(scenario_name, max_pos_limit, entry_price_df, slippage=0.0):
    start_idx = 250
    real_portfolio = {}
    completed_trades = []
    pnl_history = []

    is_t_plus_1 = (entry_price_df is opens)
    end_idx = len(closes) - 1 if is_t_plus_1 else len(closes)

    def process_exits(current_date_str, i_idx):
        tickers_to_remove = []
        for ticker, trade in real_portfolio.items():
            trade['Bars_Held'] += 1
            h, l, c = highs[ticker].iloc[i_idx], lows[ticker].iloc[i_idx], closes[ticker].iloc[i_idx]
            if pd.isna(h) or pd.isna(l) or pd.isna(c): continue

            is_closed = False
            if h >= trade['TP']:
                trade['Exit_Date'], trade['Exit_Price'], trade['Status'], trade['Exit_Reason'] = current_date_str, trade['TP'], 'Win', 'TP'
                trade['PnL_%'] = round(((trade['TP'] - trade['Entry_Price']) / trade['Entry_Price']) * 100, 2)
                is_closed = True
            elif l <= trade['SL']:
                trade['Exit_Date'], trade['Exit_Price'], trade['Status'], trade['Exit_Reason'] = current_date_str, trade['SL'], 'Loss', 'SL'
                trade['PnL_%'] = round(((trade['SL'] - trade['Entry_Price']) / trade['Entry_Price']) * 100, 2)
                is_closed = True
            elif "RSI" in trade['Type']:
                if trade['Bars_Held'] >= 15 and c <= trade['Entry_Price']:
                    trade['Exit_Date'], trade['Exit_Price'], trade['Status'], trade['Exit_Reason'] = current_date_str, c, 'Loss', 'Time_SL'
                    trade['PnL_%'] = round(((c - trade['Entry_Price']) / trade['Entry_Price']) * 100, 2)
                    is_closed = True
                elif trade['Bars_Held'] >= 30:
                    trade['Exit_Date'], trade['Exit_Price'] = current_date_str, c
                    trade['Status'] = 'Win' if c > trade['Entry_Price'] else 'Loss'
                    trade['Exit_Reason'] = 'Max_Hold'
                    trade['PnL_%'] = round(((c - trade['Entry_Price']) / trade['Entry_Price']) * 100, 2)
                    is_closed = True
            elif "海龜" in trade['Type']:
                if trade['Bars_Held'] >= 60:
                    trade['Exit_Date'], trade['Exit_Price'] = current_date_str, c
                    trade['Status'] = 'Win' if c > trade['Entry_Price'] else 'Loss'
                    trade['Exit_Reason'] = 'Max_Hold'
                    trade['PnL_%'] = round(((c - trade['Entry_Price']) / trade['Entry_Price']) * 100, 2)
                    is_closed = True

            if is_closed:
                completed_trades.append(trade)
                pnl_history.append({"Date": current_date_str, "Type": trade['Type'], "PnL": trade['PnL_%']})
                tickers_to_remove.append(ticker)

        for tid in tickers_to_remove:
            del real_portfolio[tid]

    todays_all_signals = []

    for i in tqdm(range(start_idx, end_idx), desc=scenario_name):
        current_date = closes.index[i]
        date_str = current_date.strftime('%Y-%m-%d')
        cur_hsi, cur_hsi_200 = hsi_c.iloc[i], hsi_200ma.iloc[i]
        if pd.isna(cur_hsi) or pd.isna(cur_hsi_200): continue

        is_bull = cur_hsi > cur_hsi_200
        cur_vix = round(vix_c.iloc[i] if not pd.isna(vix_c.iloc[i]) else 18.0, 2)

        day_120_rets = ret_120d.iloc[i].dropna()
        pqr_ranks = day_120_rets.rank(pct=True) * 100 if not day_120_rets.empty else pd.Series()

        process_exits(date_str, i)
        daily_signals = []

        if cur_vix < 15:
            continue

        for ticker in closes.columns:
            if ticker in real_portfolio: continue
            c = closes[ticker].iloc[i]
            if pd.isna(c) or c < 5.0: continue

            pqr_score = round(pqr_ranks.get(ticker, 0), 2)
            dh = donchian_high_all[ticker].iloc[i]
            rsi_val = rsi_all[ticker].iloc[i]
            
            signal = None
            if 15 <= cur_vix <= 35 and is_bull and c > dh and pqr_score >= 80:
                signal = {"Type": "PQR 海龜突破", "Priority": 1, "SL": c * 0.90, "TP": c * 1.30}
            elif cur_vix >= 15 and rsi_val < 25:
                signal = {"Type": "RSI 均值回歸 (28/25)", "Priority": 2, "SL": c * 0.90, "TP": c * 1.15}

            if signal:
                if is_t_plus_1:
                    raw_price = entry_price_df[ticker].iloc[i+1]
                    entry_date_str = closes.index[i+1].strftime('%Y-%m-%d')
                else:
                    raw_price = entry_price_df[ticker].iloc[i]
                    entry_date_str = date_str

                if pd.isna(raw_price): continue
                final_entry_price = raw_price * (1 + slippage)
                fin = get_fundamentals(ticker)
                
                daily_signals.append({
                    "Trade_ID": f"{ticker}_{entry_date_str}", "Ticker": ticker, "Stock_Name": HK_STOCK_NAMES.get(ticker, "港股"),
                    "TV_Ticker": f"HKEX:{int(ticker.split('.')[0])}" if ticker.split('.')[0].isdigit() else ticker,
                    "Type": signal['Type'], "Priority": signal['Priority'], "PQR_Score": pqr_score,
                    "Entry_Date": entry_date_str, "Entry_Price": round(final_entry_price, 2), "Entry_VIX": cur_vix,
                    "SL": round(signal['SL'], 2), "TP": round(signal['TP'], 2), "Status": "Active",
                    "Exit_Date": "-", "Exit_Price": 0.0, "Bars_Held": 0, "PnL_%": 0.0, "Exit_Reason": "-",
                    "financial_data": f"股息: {fin['div']}% | 動能: {fin['earn_label']}<br>P/E: {fin['pe']} | P/B: {fin['pb']} | ROE: {fin['roe']}%"
                })

        if i == end_idx - 1:
            todays_all_signals = daily_signals.copy()

        if daily_signals:
            slots_available = max_pos_limit - len(real_portfolio)
            if slots_available > 0:
                daily_signals.sort(key=lambda x: (x['Priority'], -x['PQR_Score']))
                for sig in daily_signals[:slots_available]:
                    real_portfolio[sig['Ticker']] = sig

    for sig in todays_all_signals:
        if sig['Ticker'] not in real_portfolio:
            sig['Status'] = 'Active'
            real_portfolio[sig['Ticker']] = sig

    all_res_trades = completed_trades + list(real_portfolio.values())
    all_res_trades.sort(key=lambda x: x['Entry_Date'], reverse=True)
    return all_res_trades, pnl_history

# ==============================================================================
# 4. 執行 4 大情境並比較
# ==============================================================================
print("\n⏳ 4/5 執行情境比較與效能測試...")

trades_A, pnl_A = run_backtest("Scenario A", 3, opens, slippage=0.002)
trades_B, pnl_B = run_backtest("Scenario B", 3, closes, slippage=0.0)
trades_C, pnl_C = run_backtest("Scenario C", 100, opens, slippage=0.002)
trades_D, pnl_D = run_backtest("Scenario D", 100, closes, slippage=0.0)

def get_metrics(trades):
    closed = [t for t in trades if t['Status'] != 'Active']
    if not closed: return 0, 0, 0
    wins = sum(1 for t in closed if t['Status'] == 'Win')
    win_rate = (wins / len(closed)) * 100
    avg_pnl = sum(t['PnL_%'] for t in closed) / len(closed)
    total_trades = len(closed)
    return total_trades, round(win_rate, 2), round(avg_pnl, 2)

results = [
    {"Scenario": "A (殘酷現實 - 3檔/T+1/有滑價)", **dict(zip(['Trades', 'WinRate(%)', 'AvgPnL(%)'], get_metrics(trades_A)))},
    {"Scenario": "B (前視偏誤 - 3檔/T收/無滑價)", **dict(zip(['Trades', 'WinRate(%)', 'AvgPnL(%)'], get_metrics(trades_B)))},
    {"Scenario": "C (錯失飆股 - 無限/T+1/有滑價)", **dict(zip(['Trades', 'WinRate(%)', 'AvgPnL(%)'], get_metrics(trades_C)))},
    {"Scenario": "D (完美幻覺 - 無限/T收/無滑價)", **dict(zip(['Trades', 'WinRate(%)', 'AvgPnL(%)'], get_metrics(trades_D)))}
]

print("\n📊 V10.1 終極情境對比報告：")
print(pd.DataFrame(results).to_string(index=False))
print("\n")

all_trades = trades_A
pnl_history = pnl_A

# ==============================================================================
# 5. 生成 HTML Dashboard 報告 (以 Scenario A 為準)
# ==============================================================================
today_dt = datetime.datetime.now()
valid_dates_list = [d.strftime('%Y-%m-%d') for d in closes.index]

for t in all_trades:
    ticker = t['Ticker']
    t['current_price'] = round(float(closes[ticker].iloc[-1]), 2)

    if t['Status'] == 'Active':
        t['Hold_Days'] = (today_dt - pd.to_datetime(t['Entry_Date'])).days
    else:
        t['Hold_Days'] = (pd.to_datetime(t['Exit_Date']) - pd.to_datetime(t['Entry_Date'])).days

    entry_idx = valid_dates_list.index(t['Entry_Date'])
    exit_idx_to_use = valid_dates_list.index(t['Exit_Date']) if t['Status'] != 'Active' else len(closes) - 1

    start_chart_idx = max(0, entry_idx - 150)
    end_chart_idx = min(len(closes), exit_idx_to_use + 40)
    if t['Status'] == 'Active': end_chart_idx = len(closes)

    t['chart_dates'] = closes.index[start_chart_idx:end_chart_idx].strftime('%Y-%m-%d').tolist()
    t['chart_prices'] = safe_list(closes[ticker].iloc[start_chart_idx:end_chart_idx])
    t['chart_sma20'] = safe_list(sma20_all[ticker].iloc[start_chart_idx:end_chart_idx])
    t['chart_ubb'] = safe_list(upper_bb_all[ticker].iloc[start_chart_idx:end_chart_idx])
    t['chart_lbb'] = safe_list(lower_bb_all[ticker].iloc[start_chart_idx:end_chart_idx])

def get_vix(d_str):
    try: return round(float(vix_c.loc[pd.to_datetime(d_str)]), 2)
    except: return 18.0

pnl_df = pd.DataFrame(pnl_history)
pnl_json_all = {"dates": [], "vix": [], "total": [], "turtle": [], "rsi": []}
pnl_json_5y = {"dates": [], "vix": [], "total": [], "turtle": [], "rsi": []}

if not pnl_df.empty:
    pnl_df['Date'] = pd.to_datetime(pnl_df['Date'])
    pnl_df = pnl_df.sort_values('Date').reset_index(drop=True)
    pnl_df['Real_PnL'] = pnl_df['PnL'] * 0.10

    unique_dates_all = sorted(pnl_df['Date'].unique())
    total_cum_all = pnl_df.groupby('Date')['Real_PnL'].sum().cumsum()
    t_df_all = pnl_df[pnl_df['Type'].str.contains('PQR|海龜')].groupby('Date')['Real_PnL'].sum().cumsum()
    r_df_all = pnl_df[pnl_df['Type'].str.contains('RSI')].groupby('Date')['Real_PnL'].sum().cumsum()

    pnl_json_all["dates"] = [d.strftime('%Y-%m-%d') for d in unique_dates_all]
    pnl_json_all["vix"] = [get_vix(d) for d in unique_dates_all]
    pnl_json_all["total"] = [round(total_cum_all.get(d, 0), 2) for d in unique_dates_all]
    pnl_json_all["turtle"] = [round(t_df_all[t_df_all.index <= d].iloc[-1], 2) if not t_df_all[t_df_all.index <= d].empty else 0 for d in unique_dates_all]
    pnl_json_all["rsi"] = [round(r_df_all[r_df_all.index <= d].iloc[-1], 2) if not r_df_all[r_df_all.index <= d].empty else 0 for d in unique_dates_all]

    five_years_ago = pd.to_datetime(END_DATE) - pd.DateOffset(years=5)
    pnl_df_5y = pnl_df[pnl_df['Date'] >= five_years_ago]
    unique_dates_5y = sorted(pnl_df_5y['Date'].unique())

    if len(unique_dates_5y) > 0:
        total_cum_5y = pnl_df_5y.groupby('Date')['Real_PnL'].sum().cumsum()
        t_df_5y = pnl_df_5y[pnl_df_5y['Type'].str.contains('PQR|海龜')].groupby('Date')['Real_PnL'].sum().cumsum()
        r_df_5y = pnl_df_5y[pnl_df_5y['Type'].str.contains('RSI')].groupby('Date')['Real_PnL'].sum().cumsum()

        pnl_json_5y["dates"] = [d.strftime('%Y-%m-%d') for d in unique_dates_5y]
        pnl_json_5y["vix"] = [get_vix(d) for d in unique_dates_5y]
        pnl_json_5y["total"] = [round(total_cum_5y.get(d, 0), 2) for d in unique_dates_5y]
        pnl_json_5y["turtle"] = [round(t_df_5y[t_df_5y.index <= d].iloc[-1], 2) if not t_df_5y[t_df_5y.index <= d].empty else 0 for d in unique_dates_5y]
        pnl_json_5y["rsi"] = [round(r_df_5y[r_df_5y.index <= d].iloc[-1], 2) if not r_df_5y[r_df_5y.index <= d].empty else 0 for d in unique_dates_5y]

five_years_ago_str = (pd.to_datetime(END_DATE) - pd.DateOffset(years=5)).strftime('%Y-%m-%d')
trades_5y_for_js = [t for t in all_trades if t['Status'] == 'Active' or t['Entry_Date'] >= five_years_ago_str]

print("⏳ 5/5 正在生成 V10.1 HTML...")
all_chart_data = clean_nans(trades_5y_for_js)
json_str = json.dumps(all_chart_data, ensure_ascii=False).replace('</', '<\\/')
dates_json_str = json.dumps(valid_dates_list, ensure_ascii=False)
pnl_json_all_str = json.dumps(pnl_json_all, ensure_ascii=False)
pnl_json_5y_str = json.dumps(pnl_json_5y, ensure_ascii=False)
hsi_json_str = json.dumps(clean_nans(hsi_json_data), ensure_ascii=False)

html_content = f"""
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <title>HK Quant Master V10.1 - 終極打擊面板</title>
    <style>
        body {{ background-color: #0f172a; color: #e2e8f0; font-family: 'Segoe UI', sans-serif; }}
        .card {{ background-color: #1e293b; border: 1px solid #334155; border-radius: 12px; }}
        .tab-active {{ background-color: #2563eb; color: white; border-bottom: 2px solid #60a5fa; }}
        .tab-inactive {{ background-color: transparent; color: #94a3b8; border-bottom: 2px solid transparent; }}
        .tab-inactive:hover {{ color: white; background-color: rgba(255,255,255,0.05); }}
        th.sortable:hover {{ color: #ffffff; background-color: #334155; cursor: pointer; }}
        .row-selected {{ background-color: rgba(59, 130, 246, 0.2) !important; border-left: 4px solid #3b82f6; }}
    </style>
</head>
<body class="p-4">
    <div class="max-w-6xl mx-auto w-full">
        <div class="card p-6 mb-6 flex flex-col md:flex-row justify-between items-start md:items-center shadow-lg border-b-4 border-blue-500">
            <div>
                <h1 class="text-3xl font-black text-white mb-1">HK Quant Master <span class="text-blue-500">V10.1 Pro</span></h1>
                <p class="text-slate-400 text-sm">VIX 領域精確打擊 | RSI(28/25) + Turtle 雙引擎</p>
                <div class="text-xs mt-1 text-slate-500 font-bold">最後更新時間：{UPDATE_TIME}</div>
                
                <div class="flex flex-wrap gap-3 mt-4">
                    <a href="https://www.patreon.com/c/teachthe66yearsoldmominvest" target="_blank" class="flex items-center bg-[#FF424D] hover:bg-[#FF424D]/80 text-white text-xs font-bold py-1.5 px-3 rounded shadow transition-colors">
                        🔥 Patreon 支持: 每日一篇教66歲丫媽學投資
                    </a>
                    <a href="https://www.threads.net/@teachthe66yearsoldmominvest" target="_blank" class="flex items-center bg-zinc-800 hover:bg-zinc-700 text-white text-xs font-bold py-1.5 px-3 rounded shadow transition-colors border border-zinc-600">
                        🧵 Threads: @teachthe66yearsoldmominvest
                    </a>
                </div>
            </div>
            <div class="mt-4 md:mt-0 text-right bg-slate-900 p-4 rounded-lg border border-slate-700 self-stretch md:self-auto flex flex-col justify-center">
                <div class="text-sm text-slate-300">最新 VIX 指數：<span class="text-xl font-bold text-yellow-400 block mt-1">{vix_c.iloc[-1]:.2f}</span></div>
            </div>
        </div>

        <div class="flex border-b border-slate-700 mb-6 space-x-1 overflow-x-auto">
            <button onclick="switchTab('tab-scan')" id="btn-scan" class="tab-btn tab-active px-4 py-3 font-bold rounded-t-lg whitespace-nowrap">🎯 活躍推薦持倉</button>
            <button onclick="switchTab('tab-hsi')" id="btn-hsi" class="tab-btn tab-inactive px-4 py-3 font-bold rounded-t-lg whitespace-nowrap text-cyan-400">📊 大盤環境 (HSI)</button>
            <button onclick="switchTab('tab-all')" id="btn-all" class="tab-btn tab-inactive px-4 py-3 font-bold rounded-t-lg whitespace-nowrap">💯 近 5 年歷史覆盤</button>
            <button onclick="switchTab('tab-pnl-5y')" id="btn-pnl-5y" class="tab-btn tab-inactive px-4 py-3 font-bold rounded-t-lg whitespace-nowrap text-yellow-400">📈 近 5 年資金曲線</button>
            <button onclick="switchTab('tab-pnl-all')" id="btn-pnl-all" class="tab-btn tab-inactive px-4 py-3 font-bold rounded-t-lg whitespace-nowrap text-green-400">🌍 2000-2026 總資金</button>
            <button onclick="switchTab('tab-manual')" id="btn-manual" class="tab-btn tab-inactive px-4 py-3 font-bold rounded-t-lg whitespace-nowrap text-purple-400">📖 系統說明書</button>
        </div>

        <div id="tab-scan" class="tab-content block">
            <div class="sticky top-0 z-40 bg-[#0f172a] pt-2 pb-4 border-b border-slate-700 shadow-2xl mb-4">
                <div class="card p-4 flex flex-col relative border-t-4 border-blue-500">
                    <div class="flex justify-between items-center mb-2">
                        <h3 id="chart_title_scan" class="text-lg font-bold text-white">點擊表格並使用鍵盤 ↑ ↓ 極速切換圖表</h3>
                    </div>
                    <div class="h-[250px] w-full relative bg-[#0f172a] rounded"><canvas id="myChartScan" class="w-full h-full"></canvas></div>
                </div>
            </div>

            <div class="overflow-x-auto border border-slate-700 rounded-lg shadow-lg">
                <table class="w-full text-left border-collapse whitespace-nowrap">
                    <thead class="bg-slate-800">
                        <tr class="text-slate-300 text-sm border-b border-slate-700">
                            <th class="p-3 sortable" onclick="sortActiveTable(0)">進場日 ↕</th>
                            <th class="p-3 sortable" onclick="sortActiveTable(1)">標的 ↕</th>
                            <th class="p-3 sortable" onclick="sortActiveTable(2)">策略與 PQR ↕</th>
                            <th class="p-3">基本面快照</th>
                            <th class="p-3 text-right sortable" onclick="sortActiveTable(4)">進場價 ↕</th>
                            <th class="p-3 text-right">SL / TP</th>
                            <th class="p-3 text-right sortable" onclick="sortActiveTable(6)">最新價 ↕</th>
                            <th class="p-3 text-center sortable" onclick="sortActiveTable(7)">持倉天數 ↕</th>
                            <th class="p-3 text-right sortable" onclick="sortActiveTable(8)">浮動損益 ↕</th>
                            <th class="p-3 text-center">狀態</th>
                        </tr>
                    </thead>
                    <tbody class="text-sm text-slate-300" id="activeTableBody"></tbody>
                </table>
            </div>
        </div>

        <div id="tab-hsi" class="tab-content hidden">
            <div class="card p-6 border-t-4 border-cyan-400 shadow-xl mb-6">
                <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-4">
                    <div>
                        <h2 class="text-2xl font-bold text-white">📊 恆生指數 (HSI) 近 1.5 年大盤環境分析</h2>
                        <p class="text-slate-400 text-sm mt-1">趨勢判定 (SMA200) 與 強勢放量日 (Follow-Through Day) 追蹤</p>
                    </div>
                    <div class="flex gap-4 text-xs font-bold mt-4 md:mt-0 bg-slate-900 p-3 rounded border border-slate-700">
                        <div class="flex items-center"><span class="w-4 h-1 bg-cyan-400 mr-2 rounded"></span> HSI 收盤價</div>
                        <div class="flex items-center"><span class="w-4 h-1 bg-purple-500 mr-2 rounded border-dashed border-t-2"></span> SMA200 (牛熊分界)</div>
                        <div class="flex items-center"><span class="text-yellow-400 text-lg mr-1">★</span> FTD (單日漲幅>1.5%且量增)</div>
                    </div>
                </div>
                <div class="h-[500px] w-full bg-[#0f172a] rounded p-2 border border-slate-700 mt-4 relative">
                    <canvas id="hsiChart" class="w-full h-full"></canvas>
                </div>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="card p-5 bg-slate-800">
                    <h3 class="text-lg font-bold text-white mb-2">🐢 海龜突破發動條件 (順勢)</h3>
                    <ul class="space-y-2 text-sm text-slate-300 mt-3">
                        <li class="flex items-center"><span class="mr-2">✅</span> VIX 位於 15 ~ 35 之間</li>
                        <li class="flex items-center"><span class="mr-2">✅</span> 大盤指數 (HSI) <strong class="text-green-400 ml-1">大於</strong> SMA200</li>
                        <li class="flex items-center text-slate-500"><span class="mr-2">💡</span> <span class="italic">大盤走多時發動，突破前高進場，追求波段爆發。</span></li>
                    </ul>
                </div>
                <div class="card p-5 bg-slate-800">
                    <h3 class="text-lg font-bold text-white mb-2">🛡️ RSI 均值回歸發動條件 (逆勢)</h3>
                    <ul class="space-y-2 text-sm text-slate-300 mt-3">
                        <li class="flex items-center"><span class="mr-2">✅</span> VIX <strong class="text-red-400 ml-1">大於 15</strong> (不可在死水區)</li>
                        <li class="flex items-center"><span class="mr-2">✅</span> 個股 RSI(28) <strong class="text-red-400 ml-1">小於 25</strong> (極度恐慌)</li>
                        <li class="flex items-center text-slate-500"><span class="mr-2">💡</span> <span class="italic">無視大盤趨勢，專挑恐慌錯殺股搶反彈，見好就收。</span></li>
                    </ul>
                </div>
            </div>
        </div>

        <div id="tab-all" class="tab-content hidden">
            <div class="card p-6 mb-6 bg-gradient-to-r from-slate-800 to-slate-900 border-l-4 border-yellow-400 shadow-xl">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-xl font-bold text-white">⚙️ 篩選器動態績效評估 (僅計算近 5 年數據)</h2>
                    <span class="text-xs bg-blue-900 text-blue-300 px-2 py-1 rounded">基準: 單筆 10% 資金配置</span>
                </div>
                <div class="grid grid-cols-2 md:grid-cols-5 gap-4 text-center">
                    <div class="bg-slate-900 p-3 rounded border border-slate-700">
                        <div class="text-xs text-slate-400 mb-1">符合筆數</div>
                        <div id="dyn-count" class="text-xl font-bold text-white">0</div>
                    </div>
                    <div class="bg-slate-900 p-3 rounded border border-slate-700">
                        <div class="text-xs text-slate-400 mb-1">勝率 (Win Rate)</div>
                        <div id="dyn-wr" class="text-xl font-bold text-blue-400">0%</div>
                    </div>
                    <div class="bg-slate-900 p-3 rounded border border-slate-700">
                        <div class="text-xs text-slate-400 mb-1">年化報酬 (Ann. Return)</div>
                        <div id="dyn-ann" class="text-xl font-bold text-green-400">0%</div>
                    </div>
                    <div class="bg-slate-900 p-3 rounded border border-slate-700">
                        <div class="text-xs text-slate-400 mb-1">最大回撤 (MDD)</div>
                        <div id="dyn-mdd" class="text-xl font-bold text-red-400">0%</div>
                    </div>
                    <div class="bg-slate-900 p-3 rounded border border-slate-700">
                        <div class="text-xs text-slate-400 mb-1">夏普值 (Sharpe)</div>
                        <div id="dyn-sharpe" class="text-xl font-bold text-yellow-400">0.00</div>
                    </div>
                </div>
            </div>

            <div class="flex flex-wrap gap-3 mb-4 p-4 card items-center">
                <select id="filterYear" onchange="filterTable()" class="bg-slate-900 text-white p-2 border border-slate-600 rounded text-sm focus:outline-none focus:border-blue-500">
                    <option value="">📆 所有年份 (近5年)</option>
                </select>
                <select id="filterType" onchange="filterTable()" class="bg-slate-900 text-white p-2 border border-slate-600 rounded text-sm focus:outline-none focus:border-blue-500">
                    <option value="">🎯 所有策略 (All Strategies)</option>
                    <option value="海龜">🐢 PQR 海龜突破</option>
                    <option value="RSI">🛡️ RSI 均值回歸</option>
                </select>
                <select id="filterStatus" onchange="filterTable()" class="bg-slate-900 text-white p-2 border border-slate-600 rounded text-sm focus:outline-none focus:border-blue-500">
                    <option value="">⚡ 所有狀態 (All Status)</option>
                    <option value="Win">🟢 獲利出場 (Win)</option>
                    <option value="Loss">🔴 停損出場 (SL)</option>
                    <option value="Time_SL">🟠 時間停損 (Time SL)</option>
                    <option value="Max_Hold">⏳ 時間極限強制平倉 (Max Hold)</option>
                </select>
                <input type="text" id="searchInput" onkeyup="filterTable()" placeholder="🔍 搜尋股票代碼..." class="bg-slate-900 text-white p-2 border border-slate-600 rounded text-sm w-40 focus:outline-none focus:border-blue-500">
            </div>

            <div class="sticky top-0 z-40 bg-[#0f172a] pt-2 pb-4 border-b border-slate-700 shadow-2xl mb-4">
                <div class="card p-4 flex flex-col relative border-t-4 border-blue-500">
                    <div class="flex justify-between items-center mb-2">
                        <h3 id="chart_title_all" class="text-lg font-bold text-white">點擊表格並使用鍵盤 ↑ ↓ 極速切換圖表</h3>
                    </div>
                    <div class="h-[250px] w-full relative bg-[#0f172a] rounded"><canvas id="myChartAll" class="w-full h-full"></canvas></div>
                </div>
            </div>

            <div class="overflow-x-auto border border-slate-700 rounded-lg shadow-lg">
                <table id="logTable" class="w-full text-left border-collapse whitespace-nowrap">
                    <thead class="bg-slate-800">
                        <tr class="text-slate-300 text-sm border-b border-slate-700">
                            <th class="p-3 sortable" onclick="sortTable(0)">進場日 ↕</th>
                            <th class="p-3 sortable" onclick="sortTable(1)">標的 ↕</th>
                            <th class="p-3 sortable" onclick="sortTable(2)">策略與 PQR ↕</th>
                            <th class="p-3">基本面快照</th>
                            <th class="p-3 text-right sortable" onclick="sortTable(4)">進場價 ↕</th>
                            <th class="p-3 text-right sortable" onclick="sortTable(5)">出場價 ↕</th>
                            <th class="p-3 text-center sortable" onclick="sortTable(6)">天數 ↕</th>
                            <th class="p-3 text-right sortable" onclick="sortTable(7)">淨利 ↕</th>
                            <th class="p-3 text-center">狀態</th>
                        </tr>
                    </thead>
                    <tbody class="text-sm text-slate-300" id="logTableBody"></tbody>
                </table>
            </div>
        </div>

        <div id="tab-pnl-5y" class="tab-content hidden">
            <div class="card p-6 border-t-4 border-yellow-400 shadow-xl">
                <div class="flex justify-between items-center mb-2">
                    <h2 class="text-2xl font-bold text-white">📈 近 5 年實盤資金曲線與 VIX 區間標示</h2>
                    <div class="flex gap-4 text-xs font-bold">
                        <div class="flex items-center"><span class="w-3 h-3 bg-red-500/20 mr-1 rounded"></span> VIX > 35 (極度恐慌)</div>
                        <div class="flex items-center"><span class="w-3 h-3 bg-green-500/10 mr-1 rounded"></span> VIX 15~35 (順勢黃金區)</div>
                        <div class="flex items-center"><span class="w-3 h-3 bg-slate-500/20 mr-1 rounded"></span> VIX < 15 (死水)</div>
                    </div>
                </div>
                <p class="text-slate-400 text-sm">資金基準: 嚴格遵守單筆 10% 資金排擠限制 (情境A)</p>
                <div class="h-[500px] w-full bg-[#0f172a] rounded p-2 border border-slate-700 mt-4">
                    <canvas id="pnlChart5y" class="w-full h-full"></canvas>
                </div>
            </div>
        </div>

        <div id="tab-pnl-all" class="tab-content hidden">
            <div class="card p-6 border-t-4 border-green-500 shadow-xl">
                <div class="flex justify-between items-center mb-2">
                    <h2 class="text-2xl font-bold text-white">🌍 2000-2026 全歷史大週期資金曲線與 VIX 標示</h2>
                    <div class="flex gap-4 text-xs font-bold">
                        <div class="flex items-center"><span class="w-3 h-3 bg-red-500/20 mr-1 rounded"></span> VIX > 35 (極度恐慌)</div>
                        <div class="flex items-center"><span class="w-3 h-3 bg-green-500/10 mr-1 rounded"></span> VIX 15~35 (順勢黃金區)</div>
                        <div class="flex items-center"><span class="w-3 h-3 bg-slate-500/20 mr-1 rounded"></span> VIX < 15 (死水)</div>
                    </div>
                </div>
                <p class="text-slate-400 text-sm">橫跨多個牛熊週期的終極實力檢驗 (單筆 10% Size)</p>
                <div class="h-[500px] w-full bg-[#0f172a] rounded p-2 border border-slate-700 mt-4">
                    <canvas id="pnlChartAll" class="w-full h-full"></canvas>
                </div>
            </div>
        </div>

        <div id="tab-manual" class="tab-content hidden card p-8 leading-relaxed text-slate-300">
            <h2 class="text-2xl font-bold text-blue-400 mb-6 border-b border-slate-700 pb-2">📖 V10.1 系統說明書 (User Manual)</h2>

            <div class="mb-6">
                <h3 class="text-lg font-bold text-white mb-2">⚙️ 1. 核心邏輯與風控 (Core Engine & Risk)</h3>
                <ul class="list-disc pl-6 space-y-2">
                    <li><strong class="text-blue-300">防仙股濾網：</strong> 系統自動排除所有股價 <strong>低於 $5 港幣</strong> 的標的，避免流動性風險。</li>
                    <li><strong class="text-blue-300">PQR 搶位戰：</strong> 當訊號超過剩餘資金空位時，將依據 120 日動能評分 (PQR Score) 排序，優先買入最強勢的股票。</li>
                    <li><strong class="text-blue-300">TV 快速查閱：</strong> 表格內的代碼皆為 <strong>TradingView 超連結</strong>，點擊即可進行人工圖表驗證。</li>
                </ul>
            </div>

            <div class="mb-6">
                <h3 class="text-lg font-bold text-white mb-2">⚔️ 2. 雙引擎與 VIX 區間發動條件</h3>
                <p class="mb-3">雙獨立引擎，各自適應不同的市場波動率：</p>
                <ul class="list-disc pl-6 space-y-3">
                    <li><span class="bg-slate-700 text-slate-300 px-2 py-0.5 rounded text-xs font-bold mr-2">VIX < 15</span><strong class="text-white">⚪ 死水區間強制空倉：</strong><br>市場缺乏波動，所有策略勝率極低，系統無條件保留現金。</li>
                    <li><span class="bg-green-900 text-green-400 px-2 py-0.5 rounded text-xs font-bold mr-2">VIX 15~35</span><strong class="text-white">🟢 順勢引擎 (PQR 海龜突破)：</strong><br>尋找突破 20 日高點且 PQR > 80 的強勢股 (大盤需站上 200MA)。停利 +30%，停損 -10%。</li>
                    <li><span class="bg-red-900 text-red-400 px-2 py-0.5 rounded text-xs font-bold mr-2">VIX >= 15</span><strong class="text-white">🔴 逆勢引擎 (RSI 均值回歸)：</strong><br>只要脫離死水區皆可發動。尋找長週期 <strong>RSI(28) < 25</strong> 的極端超跌股。停利 +15%，停損 -10%。</li>
                </ul>
            </div>

            <div>
                <h3 class="text-lg font-bold text-white mb-2">🛡️ 3. 雙重防死魚機制 (Anti-Stagnation)</h3>
                <ul class="list-disc pl-6 space-y-2">
                    <li><strong class="text-orange-400">🟠 快速停損 (Time SL)：</strong> 若 <strong>RSI 策略</strong>進場後達到 <strong>15 個交易日</strong>，且最新股價仍低於成本，系統無條件認錯平倉。</li>
                    <li><strong class="text-blue-400">⏳ 極限強制平倉 (Max Hold)：</strong> <strong>海龜最多抱 60 天</strong>，<strong>RSI 最多抱 30 天</strong>。時間一到強制結算，釋放資金。</li>
                </ul>
            </div>
        </div>

    </div>

    <script>
        const signalsData = {json_str};
        const allDates = {dates_json_str};
        const pnlDataAll = {pnl_json_all_str};
        const pnlData5y = {pnl_json_5y_str};
        const hsiData = {hsi_json_str};

        let chartInstanceScan = null;
        let chartInstanceAll = null;
        let pnlChart5y = null;
        let pnlChartAll = null;
        let hsiChart = null;
        let currentRowIndex = -1;

        const exitReasonPlugin = {{
            id: 'exitReasonPlugin',
            afterDraw: (chart) => {{
                const ctx = chart.ctx;
                const tradeData = chart.config.data.customTradeData;
                if(!tradeData || tradeData.Status === 'Active') return;

                chart.data.datasets.forEach((dataset, i) => {{
                    if (dataset.label === '出場') {{
                        const meta = chart.getDatasetMeta(i);
                        meta.data.forEach((point) => {{
                            if (!point.skip) {{
                                ctx.save();
                                ctx.fillStyle = tradeData.Status === 'Win' ? '#4ade80' : '#f87171';
                                ctx.font = 'bold 13px "Segoe UI"';
                                ctx.textAlign = 'left';
                                ctx.fillText(tradeData.Exit_Reason, point.x + 10, point.y - 12);
                                ctx.restore();
                            }}
                        }});
                    }}
                }});
            }}
        }};

        const vixBackgroundPlugin = {{
            id: 'vixBackgroundPlugin',
            beforeDraw: (chart) => {{
                const ctx = chart.ctx;
                const xAxis = chart.scales.x;
                const yAxis = chart.scales.y;
                const vixData = chart.config.data.vixData;
                if(!vixData || vixData.length === 0) return;

                ctx.save();
                const topY = yAxis.top;
                const bottomY = yAxis.bottom;

                for(let i = 0; i < vixData.length - 1; i++) {{
                    let v = vixData[i];
                    let color = 'rgba(0,0,0,0)';
                    if(v > 35) color = 'rgba(239, 68, 68, 0.1)';
                    else if(v < 15) color = 'rgba(100, 116, 139, 0.2)';
                    else color = 'rgba(34, 197, 94, 0.05)';

                    let xStart = xAxis.getPixelForValue(i);
                    let xEnd = xAxis.getPixelForValue(i+1);

                    ctx.fillStyle = color;
                    ctx.fillRect(xStart, topY, xEnd - xStart, bottomY - topY);
                }}
                ctx.restore();
            }}
        }};

        Chart.register(exitReasonPlugin, vixBackgroundPlugin);

        function populateYearFilter() {{
            let years = [...new Set(signalsData.filter(s => s.Status !== 'Active').map(s => s.Entry_Date.substring(0,4)))].sort().reverse();
            let sel = document.getElementById("filterYear");
            years.forEach(y => {{
                let opt = document.createElement('option');
                opt.value = y; opt.innerText = "📆 " + y + " 年";
                sel.appendChild(opt);
            }});
        }}

        function renderActiveTable() {{
            const tbody = document.getElementById('activeTableBody');
            tbody.innerHTML = "";
            const actives = signalsData.filter(s => s.Status === 'Active');

            if(actives.length === 0) {{
                tbody.innerHTML = `<tr><td colspan="10" class="p-6 text-center text-slate-500">目前空手，無活躍觸發標的。</td></tr>`;
                return;
            }}

            actives.forEach(row => {{
                let pnl = ((row.current_price - row.Entry_Price) / row.Entry_Price) * 100;
                let pnlClr = pnl > 0 ? "text-green-400" : "text-red-400";
                let pnlStr = `<span class="${{pnlClr}} font-bold">${{pnl>0?'+':''}}${{pnl.toFixed(2)}}%</span>`;
                let statusBadge = `<span class="px-2 py-1 bg-yellow-900/50 text-yellow-400 rounded text-xs animate-pulse">Active</span>`;
                let pqrBadge = `<span class="text-[10px] ml-1 bg-purple-900/50 text-purple-300 border border-purple-700 px-1 rounded">PQR: ${{row.PQR_Score}}</span>`;
                
                // TradingView 超連結
                let tvLink = `<a href="https://www.tradingview.com/chart/?symbol=${{row.TV_Ticker}}" target="_blank" class="text-blue-400 hover:text-blue-300 underline underline-offset-2" onclick="event.stopPropagation()">${{row.Ticker}}</a>`;

                let tr = document.createElement('tr');
                tr.className = "trade-row active-trade-row border-b border-slate-800 hover:bg-slate-700/50 cursor-pointer";
                tr.setAttribute('data-trade-id', row.Trade_ID);
                tr.onclick = function() {{
                    document.querySelectorAll('.active-trade-row').forEach(el => el.classList.remove('row-selected'));
                    tr.classList.add('row-selected');
                    const visibleRows = Array.from(document.querySelectorAll('.active-trade-row'));
                    currentRowIndex = visibleRows.indexOf(tr);
                    loadChart(row.Trade_ID, 'myChartScan');
                }};

                tr.innerHTML = `
                    <td class="p-3 text-blue-300 font-bold">${{row.Entry_Date}}</td>
                    <td class="p-3 font-bold">${{tvLink}}<br><span class="text-xs text-slate-400 font-normal">${{row.Stock_Name}}</span></td>
                    <td class="p-3 text-sm">${{row.Type}}<br>${{pqrBadge}}</td>
                    <td class="p-3 text-xs text-slate-400 leading-relaxed">${{row.financial_data}}</td>
                    <td class="p-3 text-right font-bold text-white">$${{row.Entry_Price}}</td>
                    <td class="p-3 text-right text-xs"><span class="text-red-400">SL: ${{row.SL}}</span><br><span class="text-green-400">TP: ${{row.TP}}</span></td>
                    <td class="p-3 text-right text-blue-300 font-bold">$${{row.current_price}}</td>
                    <td class="p-3 text-center text-yellow-400 font-bold">${{row.Hold_Days}}</td>
                    <td class="p-3 text-right bg-slate-900/30" data-pnl="${{pnl}}">${{pnlStr}}</td>
                    <td class="p-3 text-center">${{statusBadge}}</td>
                `;
                tbody.appendChild(tr);
            }});

            if(actives.length > 0) {{
                let firstRow = document.querySelector('#activeTableBody tr');
                firstRow.classList.add('row-selected');
                currentRowIndex = 0;
                loadChart(actives[0].Trade_ID, 'myChartScan');
            }}
        }}

        function renderTable(data) {{
            const tbody = document.getElementById('logTableBody');
            tbody.innerHTML = "";
            let closedTrades = data.filter(d => d.Status !== 'Active');

            closedTrades.forEach(row => {{
                let pnlClr = row['PnL_%'] > 0 ? "text-green-400" : "text-red-400";
                let pnlStr = `<span class="${{pnlClr}} font-bold">${{row['PnL_%']>0?'+':''}}${{row['PnL_%'].toFixed(2)}}%</span>`;

                let statusBadge;
                if(row.Exit_Reason === 'TP') statusBadge = `<span class="px-2 py-1 bg-green-900/50 text-green-400 rounded text-xs">Win (TP)</span>`;
                else if(row.Exit_Reason === 'Time_SL') statusBadge = `<span class="px-2 py-1 bg-orange-900/50 text-orange-400 rounded text-xs">Time SL</span>`;
                else if(row.Exit_Reason === 'Max_Hold') statusBadge = `<span class="px-2 py-1 bg-blue-900/50 text-blue-400 rounded text-xs">Max Hold</span>`;
                else statusBadge = `<span class="px-2 py-1 bg-red-900/50 text-red-400 rounded text-xs">Loss (SL)</span>`;

                let pqrBadge = `<span class="text-[10px] ml-1 bg-purple-900/50 text-purple-300 border border-purple-700 px-1 rounded">PQR: ${{row.PQR_Score}}</span>`;
                
                // TradingView 超連結
                let tvLink = `<a href="https://www.tradingview.com/chart/?symbol=${{row.TV_Ticker}}" target="_blank" class="text-blue-400 hover:text-blue-300 underline underline-offset-2" onclick="event.stopPropagation()">${{row.Ticker}}</a>`;

                let tr = document.createElement('tr');
                tr.className = "trade-row history-trade-row border-b border-slate-800 hover:bg-slate-700/50 cursor-pointer";
                tr.setAttribute('data-trade-id', row.Trade_ID);
                tr.onclick = function() {{
                    document.querySelectorAll('.history-trade-row').forEach(el => el.classList.remove('row-selected'));
                    tr.classList.add('row-selected');
                    const visibleRows = Array.from(document.querySelectorAll('.history-trade-row')).filter(el => el.style.display !== 'none');
                    currentRowIndex = visibleRows.indexOf(tr);
                    loadChart(row.Trade_ID, 'myChartAll');
                }};

                tr.innerHTML = `
                    <td class="p-3 text-blue-300 font-bold">${{row.Entry_Date}}</td>
                    <td class="p-3 font-bold">${{tvLink}}<br><span class="text-xs text-slate-400 font-normal">${{row.Stock_Name}}</span></td>
                    <td class="p-3 text-sm">${{row.Type}}<br>${{pqrBadge}}</td>
                    <td class="p-3 text-xs text-slate-400 leading-relaxed">${{row.financial_data}}</td>
                    <td class="p-3 text-right">$${{row.Entry_Price}}</td>
                    <td class="p-3 text-right text-slate-300">$${{row.Exit_Price}}</td>
                    <td class="p-3 text-center">${{row.Hold_Days}}</td>
                    <td class="p-3 text-right bg-slate-900/30" data-pnl="${{row['PnL_%']}}">${{pnlStr}}</td>
                    <td class="p-3 text-center">${{statusBadge}}</td>
                `;
                tbody.appendChild(tr);
            }});

            if(closedTrades.length > 0) {{
                let firstRow = document.querySelector('#logTableBody tr');
                if(firstRow) {{
                    firstRow.classList.add('row-selected');
                    currentRowIndex = 0;
                    loadChart(closedTrades[0].Trade_ID, 'myChartAll');
                }}
            }}
        }}

        function calculateDynamicMetrics(trades) {{
            let closedTrades = trades.filter(t => t.Status !== 'Active');
            document.getElementById('dyn-count').innerText = closedTrades.length;
            if(closedTrades.length === 0) {{
                document.getElementById('dyn-wr').innerText = "0%";
                document.getElementById('dyn-ann').innerText = "0%";
                document.getElementById('dyn-mdd').innerText = "0%";
                document.getElementById('dyn-sharpe').innerText = "0.00";
                return;
            }}

            let wins = closedTrades.filter(t => t.Status === 'Win').length;
            document.getElementById('dyn-wr').innerText = ((wins / closedTrades.length) * 100).toFixed(1) + "%";

            let dailyRet = new Float64Array(allDates.length);
            closedTrades.forEach(t => {{
                let sIdx = allDates.indexOf(t.Entry_Date);
                let eIdx = allDates.indexOf(t.Exit_Date);
                if(sIdx !== -1 && eIdx !== -1 && eIdx >= sIdx) {{
                    let days = eIdx - sIdx + 1;
                    let daily = (t['PnL_%'] / 100 * 0.10) / days;
                    for(let i=sIdx; i<=eIdx; i++) dailyRet[i] += daily;
                }}
            }});

            let equity = 1.0, peak = 1.0, mdd = 0.0, sum = 0, sumSq = 0, count = 0;
            let started = false;
            for(let i=0; i<dailyRet.length; i++) {{
                let r = dailyRet[i];
                if(r !== 0) started = true;
                if(started) {{
                    equity *= (1 + r);
                    if(equity > peak) peak = equity;
                    let dd = (equity - peak) / peak;
                    if(dd < mdd) mdd = dd;
                    sum += r;
                    sumSq += r * r;
                    count++;
                }}
            }}

            let years = count / 252;
            let ann = years > 0 ? (Math.pow(equity, 1/years) - 1) * 100 : 0;
            let mean = count > 0 ? sum / count : 0;
            let variance = count > 0 ? (sumSq / count) - (mean * mean) : 0;
            let std = Math.sqrt(variance);
            let sharpe = std > 0 ? (mean / std) * Math.sqrt(252) : 0;

            document.getElementById('dyn-ann').innerText = (ann>0?'+':'') + ann.toFixed(2) + "%";
            document.getElementById('dyn-mdd').innerText = (mdd*100).toFixed(2) + "%";
            document.getElementById('dyn-sharpe').innerText = sharpe.toFixed(2);
        }}

        function filterTable() {{
            let yearF = document.getElementById("filterYear").value;
            let typeF = document.getElementById("filterType").value;
            let statusF = document.getElementById("filterStatus").value;
            let searchF = document.getElementById("searchInput").value.toUpperCase();

            let filtered = signalsData.filter(s => {{
                if(s.Status === 'Active') return false;
                let matchYear = yearF === "" || s.Entry_Date.startsWith(yearF);
                let matchType = typeF === "" || s.Type.includes(typeF);

                let matchStatus = true;
                if(statusF !== "") {{
                    if(statusF === "Win") matchStatus = (s.Status === "Win");
                    else if(statusF === "Time_SL") matchStatus = (s.Exit_Reason === "Time_SL");
                    else if(statusF === "Max_Hold") matchStatus = (s.Exit_Reason === "Max_Hold");
                    else if(statusF === "Loss") matchStatus = (s.Status === "Loss" && s.Exit_Reason === "SL");
                }}

                let matchSearch = searchF === "" || s.Ticker.includes(searchF) || (s.Stock_Name && s.Stock_Name.includes(searchF));
                return matchYear && matchType && matchStatus && matchSearch;
            }});

            renderTable(filtered);
            calculateDynamicMetrics(filtered);
        }}

        let sortAscAll = true;
        let sortAscActive = true;

        function sortTable(colIdx) {{
            const tbody = document.getElementById("logTableBody");
            const rows = Array.from(tbody.querySelectorAll("tr"));
            sortAscAll = !sortAscAll;
            rows.sort((a, b) => {{
                let v1 = a.children[colIdx].innerText.replace(/[%$,浮動\+]/g, '').trim();
                let v2 = b.children[colIdx].innerText.replace(/[%$,浮動\+]/g, '').trim();
                if(colIdx === 7) {{ v1 = a.children[colIdx].getAttribute('data-pnl') || 0; v2 = b.children[colIdx].getAttribute('data-pnl') || 0; }}
                let n1 = parseFloat(v1), n2 = parseFloat(v2);
                if(!isNaN(n1) && !isNaN(n2)) return sortAscAll ? n1 - n2 : n2 - n1;
                return sortAscAll ? v1.localeCompare(v2) : v2.localeCompare(v1);
            }});
            tbody.innerHTML = "";
            rows.forEach(r => tbody.appendChild(r));
        }}

        function sortActiveTable(colIdx) {{
            const tbody = document.getElementById("activeTableBody");
            const rows = Array.from(tbody.querySelectorAll("tr"));
            sortAscActive = !sortAscActive;
            rows.sort((a, b) => {{
                let v1 = a.children[colIdx].innerText.replace(/[%$,浮動\+]/g, '').trim();
                let v2 = b.children[colIdx].innerText.replace(/[%$,浮動\+]/g, '').trim();
                if(colIdx === 8) {{ v1 = a.children[colIdx].getAttribute('data-pnl') || 0; v2 = b.children[colIdx].getAttribute('data-pnl') || 0; }}
                let n1 = parseFloat(v1), n2 = parseFloat(v2);
                if(!isNaN(n1) && !isNaN(n2)) return sortAscActive ? n1 - n2 : n2 - n1;
                return sortAscActive ? v1.localeCompare(v2) : v2.localeCompare(v1);
            }});
            tbody.innerHTML = "";
            rows.forEach(r => tbody.appendChild(r));
        }}

        function loadChart(tradeId, canvasId) {{
            const sig = signalsData.find(s => s.Trade_ID === tradeId);
            if (!sig) return;

            const titleEl = document.getElementById(canvasId === 'myChartScan' ? 'chart_title_scan' : 'chart_title_all');
            if(titleEl) titleEl.innerHTML = sig.Ticker + " " + sig.Stock_Name + " <span class='text-sm text-slate-400'>(" + sig.Type + ")</span>";

            const ctx = document.getElementById(canvasId).getContext('2d');
            let targetChart = canvasId === 'myChartScan' ? chartInstanceScan : chartInstanceAll;
            if (targetChart) targetChart.destroy();

            const entryIdx = sig.chart_dates.indexOf(sig.Entry_Date);
            const exitIdx = sig.Exit_Date !== "-" ? sig.chart_dates.indexOf(sig.Exit_Date) : sig.chart_dates.length - 1;

            const entryData = sig.chart_dates.map((d, idx) => (idx === entryIdx) ? sig.Entry_Price : null);
            const exitData = sig.chart_dates.map((d, idx) => (idx === exitIdx && sig.Status !== 'Active') ? sig.Exit_Price : null);

            let newChart = new Chart(ctx, {{
                type: 'line',
                data: {{
                    labels: sig.chart_dates.map(d => d.substring(5)),
                    customTradeData: sig,
                    datasets: [
                        {{ label: '進場', data: entryData, backgroundColor: '#eab308', pointStyle: 'triangle', pointRadius: 8, showLine: false, order: 0 }},
                        {{ label: '出場', data: exitData, backgroundColor: sig.Status === 'Win' ? '#4ade80' : '#f87171', pointStyle: 'crossRot', pointRadius: 8, showLine: false, order: 1 }},
                        {{ label: '價格', data: sig.chart_prices, borderColor: '#3b82f6', tension: 0.1, pointRadius: 0, order: 2 }},
                        {{ label: 'SMA20', data: sig.chart_sma20, borderColor: '#c084fc', borderDash: [2,2], borderWidth: 1.5, pointRadius: 0, order: 3 }},
                        {{ label: 'BOLL上軌', data: sig.chart_ubb, borderColor: '#64748b', borderDash: [4,4], borderWidth: 1, pointRadius: 0, order: 4 }},
                        {{ label: 'BOLL下軌', data: sig.chart_lbb, borderColor: '#64748b', borderDash: [4,4], borderWidth: 1, pointRadius: 0, order: 5 }}
                    ]
                }},
                options: {{
                    responsive: true, maintainAspectRatio: false,
                    interaction: {{ mode: 'index', intersect: false }},
                    scales: {{ x: {{ ticks: {{ color: '#94a3b8' }} }}, y: {{ ticks: {{ color: '#94a3b8' }} }} }},
                    plugins: {{
                        legend: {{ labels: {{ color: '#e2e8f0' }} }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    let label = context.dataset.label || '';
                                    if (label === '出場') return label + ': ' + context.parsed.y + ' (' + sig.Exit_Reason + ')';
                                    return label + ': ' + context.parsed.y;
                                }}
                            }}
                        }}
                    }}
                }}
            }});
            if (canvasId === 'myChartScan') chartInstanceScan = newChart; else chartInstanceAll = newChart;
        }}

        function renderPnLCharts() {{
            if(!pnlChart5y && pnlData5y.dates && pnlData5y.dates.length > 0) {{
                const ctx5y = document.getElementById('pnlChart5y').getContext('2d');
                pnlChart5y = new Chart(ctx5y, {{
                    type: 'line',
                    data: {{
                        labels: pnlData5y.dates,
                        vixData: pnlData5y.vix,
                        datasets: [
                            {{ label: '近5年總資金', data: pnlData5y.total, borderColor: '#eab308', borderWidth: 3, pointRadius: 0, tension: 0.1 }},
                            {{ label: 'PQR 突破貢獻', data: pnlData5y.turtle, borderColor: '#4ade80', borderWidth: 1, borderDash: [3,3], pointRadius: 0, tension: 0.1 }},
                            {{ label: 'RSI 逆勢貢獻', data: pnlData5y.rsi, borderColor: '#f87171', borderWidth: 1, borderDash: [3,3], pointRadius: 0, tension: 0.1 }}
                        ]
                    }},
                    options: {{ responsive: true, maintainAspectRatio: false, interaction: {{ mode: 'index', intersect: false }} }}
                }});
            }}

            if(!pnlChartAll && pnlDataAll.dates && pnlDataAll.dates.length > 0) {{
                const ctxAll = document.getElementById('pnlChartAll').getContext('2d');
                pnlChartAll = new Chart(ctxAll, {{
                    type: 'line',
                    data: {{
                        labels: pnlDataAll.dates,
                        vixData: pnlDataAll.vix,
                        datasets: [
                            {{ label: '歷史總資金 (2000-2026)', data: pnlDataAll.total, borderColor: '#22c55e', borderWidth: 3, pointRadius: 0, tension: 0.1 }},
                            {{ label: 'PQR 突破貢獻', data: pnlDataAll.turtle, borderColor: '#3b82f6', borderWidth: 1, borderDash: [3,3], pointRadius: 0, tension: 0.1 }},
                            {{ label: 'RSI 逆勢貢獻', data: pnlDataAll.rsi, borderColor: '#ef4444', borderWidth: 1, borderDash: [3,3], pointRadius: 0, tension: 0.1 }}
                        ]
                    }},
                    options: {{ responsive: true, maintainAspectRatio: false, interaction: {{ mode: 'index', intersect: false }} }}
                }});
            }}

            // 渲染 HSI 大盤圖表
            if(!hsiChart && hsiData.dates && hsiData.dates.length > 0) {{
                const ctxHsi = document.getElementById('hsiChart').getContext('2d');
                
                // 準備 FTD 訊號點
                let ftdData = new Array(hsiData.dates.length).fill(null);
                hsiData.ftds.forEach(f => {{
                    let idx = hsiData.dates.indexOf(f.date);
                    if (idx !== -1) ftdData[idx] = f.price;
                }});

                hsiChart = new Chart(ctxHsi, {{
                    type: 'line',
                    data: {{
                        labels: hsiData.dates,
                        datasets: [
                            {{ label: 'FTD (強勢放量日)', data: ftdData, backgroundColor: '#facc15', borderColor: '#ca8a04', pointStyle: 'star', pointRadius: 10, pointHoverRadius: 14, showLine: false, order: 0 }},
                            {{ label: 'HSI 指數', data: hsiData.closes, borderColor: '#22d3ee', borderWidth: 2, pointRadius: 0, tension: 0.1, order: 2 }},
                            {{ label: 'SMA200', data: hsiData.sma200, borderColor: '#a855f7', borderWidth: 2, borderDash: [5,5], pointRadius: 0, tension: 0.1, order: 1 }}
                        ]
                    }},
                    options: {{ 
                        responsive: true, maintainAspectRatio: false, 
                        interaction: {{ mode: 'index', intersect: false }},
                        plugins: {{
                            tooltip: {{
                                callbacks: {{
                                    label: function(context) {{
                                        let label = context.dataset.label || '';
                                        if (label.includes('FTD')) {{
                                            // 找對應的 FTD label
                                            let ftdObj = hsiData.ftds.find(f => f.date === context.label);
                                            return label + ': ' + context.parsed.y + ' (' + (ftdObj ? ftdObj.label : '') + ')';
                                        }}
                                        return label + ': ' + context.parsed.y;
                                    }}
                                }}
                            }}
                        }}
                    }}
                }});
            }}
        }}

        document.addEventListener('keydown', function(e) {{
            if (document.activeElement.tagName === 'INPUT' || document.activeElement.tagName === 'SELECT') return;

            let activeTabId = document.querySelector('.tab-content:not(.hidden)').id;
            let rowClass = activeTabId === 'tab-scan' ? '.active-trade-row' : (activeTabId === 'tab-all' ? '.history-trade-row' : null);
            if (!rowClass) return;

            const visibleRows = Array.from(document.querySelectorAll(rowClass)).filter(el => el.style.display !== 'none');
            if (visibleRows.length === 0) return;

            if (e.key === 'ArrowDown') {{
                e.preventDefault();
                currentRowIndex = (currentRowIndex + 1) % visibleRows.length;
                let nextRow = visibleRows[currentRowIndex];
                document.querySelectorAll(rowClass).forEach(el => el.classList.remove('row-selected'));
                nextRow.classList.add('row-selected');
                nextRow.scrollIntoView({{ block: 'nearest', behavior: 'smooth' }});
                loadChart(nextRow.getAttribute('data-trade-id'), activeTabId === 'tab-scan' ? 'myChartScan' : 'myChartAll');
            }}
            else if (e.key === 'ArrowUp') {{
                e.preventDefault();
                currentRowIndex = (currentRowIndex - 1 + visibleRows.length) % visibleRows.length;
                let prevRow = visibleRows[currentRowIndex];
                document.querySelectorAll(rowClass).forEach(el => el.classList.remove('row-selected'));
                prevRow.classList.add('row-selected');
                prevRow.scrollIntoView({{ block: 'nearest', behavior: 'smooth' }});
                loadChart(prevRow.getAttribute('data-trade-id'), activeTabId === 'tab-scan' ? 'myChartScan' : 'myChartAll');
            }}
        }});

        function switchTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.tab-btn').forEach(btn => {{ btn.classList.remove('tab-active'); btn.classList.add('tab-inactive'); }});
            document.getElementById(tabId).classList.remove('hidden');

            let btnId = tabId.replace('tab-', 'btn-');
            document.getElementById(btnId).classList.remove('tab-inactive');
            document.getElementById(btnId).classList.add('tab-active');

            if (tabId.includes('pnl') || tabId.includes('hsi')) renderPnLCharts();
        }}

        // Init
        populateYearFilter();
        renderActiveTable();
        renderTable(signalsData);
        calculateDynamicMetrics(signalsData.filter(s => s.Status !== 'Active'));

    </script>
</body>
</html>
"""

with open("index.html", 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"🎉 成功！生成 HK Quant Master V10.1 終極 Dashboard：index.html")
try:
    from google.colab import files
    files.download("index.html")
except:
    pass
