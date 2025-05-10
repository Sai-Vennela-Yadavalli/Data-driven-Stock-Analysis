import os
import pandas as pd
import numpy as np

stock_folder = '/Users/jagadeeshsaivennela/Documents/Data Analysis - mini projects/Data-Driven Stock Analysis Project/Project#2/stock_csvs'
data_folder = 'data'
os.makedirs(data_folder, exist_ok=True)

# Load and clean sector mapping
sector_df = pd.read_csv("/Users/jagadeeshsaivennela/Downloads/Sector_data - Sheet1.csv")
sector_df['Symbol'] = sector_df['Symbol'].apply(lambda x: x.split(":")[-1].strip())
sector_map = dict(zip(sector_df['Symbol'], sector_df['sector']))

returns = []
volatility_data = []
sector_returns = []
monthly_returns = []
cumulative_df = pd.DataFrame()
price_df = pd.DataFrame()
all_prices = []
all_volumes = []
green_stocks = red_stocks = 0

for file in os.listdir(stock_folder):
    if file.endswith('.csv'):
        df = pd.read_csv(os.path.join(stock_folder, file)).sort_values(by='date')

        if df.empty or len(df) < 2:
            continue

        ticker = df['Ticker'].iloc[0]
        first_close = df['close'].iloc[0]
        last_close = df['close'].iloc[-1]
        yearly_return = (last_close - first_close) / first_close * 100
        returns.append({'Ticker': ticker, 'Yearly Return (%)': yearly_return})

        if last_close > first_close:
            green_stocks += 1
        else:
            red_stocks += 1

        avg_price = df[['open', 'high', 'low', 'close']].mean(axis=1)
        all_prices.extend(avg_price.tolist())
        all_volumes.extend(df['volume'].tolist())

        # Volatility
        df['daily_return'] = df['close'].pct_change()
        volatility = df['daily_return'].std()
        if pd.notnull(volatility):
            volatility_data.append({'Ticker': ticker, 'Volatility': volatility})

        # Cumulative return
        df['cumulative_return'] = (1 + df['daily_return']).cumprod()
        cumulative_df[ticker] = df['cumulative_return'].values
        cumulative_df['date'] = df['date'].values

        # Sector return
        if ticker in sector_map:
            sector_returns.append({'Sector': sector_map[ticker], 'Return': yearly_return})

        # Monthly return
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M')
        for month, group in df.groupby('month'):
            if len(group) < 2:
                continue
            m_return = (group['close'].iloc[-1] - group['close'].iloc[0]) / group['close'].iloc[0] * 100
            monthly_returns.append({'Month': str(month), 'Ticker': ticker, 'Monthly Return (%)': m_return})

        # Price correlation
        close_df = df[['date', 'close']].rename(columns={'close': ticker})
        if price_df.empty:
            price_df = close_df
        else:
            price_df = pd.merge(price_df, close_df, on='date', how='outer')

# Process and save
top_10_green = pd.DataFrame(returns).sort_values(by='Yearly Return (%)', ascending=False).head(10)
top_10_red = pd.DataFrame(returns).sort_values(by='Yearly Return (%)').head(10)
top_10_volatility = pd.DataFrame(volatility_data).sort_values(by='Volatility', ascending=False).head(10)
sector_avg_return = pd.DataFrame(sector_returns).groupby('Sector')['Return'].mean().reset_index().sort_values(by='Return', ascending=False)
monthly_df = pd.DataFrame(monthly_returns)

price_df['date'] = pd.to_datetime(price_df['date'])
price_df.set_index('date', inplace=True)
price_df.sort_index(inplace=True)
price_df.fillna(method='ffill', inplace=True)
correlation_matrix = price_df.corr()

# Save everything
top_10_green.to_csv(f'{data_folder}/top_10_green.csv', index=False)
top_10_red.to_csv(f'{data_folder}/top_10_red.csv', index=False)
top_10_volatility.to_csv(f'{data_folder}/top_10_volatility.csv', index=False)
cumulative_df.to_csv(f'{data_folder}/cumulative_df.csv', index=False)
sector_avg_return.to_csv(f'{data_folder}/sector_avg_return.csv', index=False)
monthly_df.to_csv(f'{data_folder}/monthly_df.csv', index=False)
correlation_matrix.to_csv(f'{data_folder}/correlation_matrix.csv')

with open(f'{data_folder}/metrics.txt', 'w') as f:
    f.write(f'green_stocks={green_stocks}\n')
    f.write(f'red_stocks={red_stocks}\n')
    f.write(f'average_price={np.mean(all_prices):.2f}\n')
    f.write(f'average_volume={int(np.mean(all_volumes))}\n')
print('✅ Data prepared and saved in "data/" folder.')
