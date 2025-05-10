import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates 


# Load pre-processed data
data_folder = "data"
top_10_green = pd.read_csv(f"{data_folder}/top_10_green.csv")
top_10_red = pd.read_csv(f"{data_folder}/top_10_red.csv")
top_10_volatility = pd.read_csv(f"{data_folder}/top_10_volatility.csv")
cumulative_df = pd.read_csv(f"{data_folder}/cumulative_df.csv")
sector_avg_return = pd.read_csv(f"{data_folder}/sector_avg_return.csv")
monthly_df = pd.read_csv(f"{data_folder}/monthly_df.csv")
correlation_matrix = pd.read_csv(f"{data_folder}/correlation_matrix.csv", index_col=0)

# Load summary metrics
def load_metrics(filepath):
    metrics = {}
    with open(filepath) as f:
        for line in f:
            key, value = line.strip().split("=")
            metrics[key] = float(value) if "." in value else int(value)
    return metrics

metrics = load_metrics(f"{data_folder}/metrics.txt")
green_stocks = metrics['green_stocks']
red_stocks = metrics['red_stocks']
average_price = metrics['average_price']
average_volume = metrics['average_volume']
top_5_tickers = top_10_green['Ticker'].head(5).tolist()

# Streamlit app
st.set_page_config(layout="wide")
st.title("📈 Data-Driven Stock Analysis Dashboard")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Market Summary", "Top Gainers/Losers", "Volatility",
    "Cumulative Return", "Sector Performance", "Correlation Heatmap",
    "Monthly Gainers/Losers"
])

with tab1:
    st.header("📊 Market Summary")
    col1, col2 = st.columns(2)
    col1.metric("✅ Green Stocks", green_stocks)
    col2.metric("❌ Red Stocks", red_stocks)
    col1.metric("📈 Average Price", f"₹{average_price:.2f}")
    col2.metric("📊 Average Volume", f"{average_volume:,.0f}")

with tab2:
    st.header("📈 Top 10 Gainers & ❌ Losers")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top 10 Gainers")
        st.bar_chart(top_10_green.set_index("Ticker")["Yearly Return (%)"])
    with col2:
        st.subheader("Top 10 Losers")
        st.bar_chart(top_10_red.set_index("Ticker")["Yearly Return (%)"])

with tab3:
    st.header("📉 Most Volatile Stocks")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=top_10_volatility, x="Volatility", y="Ticker", palette="flare", ax=ax)
    st.pyplot(fig)

with tab4:
    st.header("📈 Cumulative Return (Top 5 Stocks)")
    cumulative_df['date'] = pd.to_datetime(cumulative_df['date'])

    fig, ax = plt.subplots(figsize=(14, 6))

    for ticker in top_5_tickers:
        ax.plot(cumulative_df['date'], cumulative_df[ticker], label=ticker)

    ax.set_title("Top 5 Performing Stocks - Cumulative Return")
    ax.set_xlabel("Date")
    ax.set_ylabel("Cumulative Return (Growth Factor)")

# Apply date formatting and spacing
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))  # show one tick per month
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))  # format like Jan 2024
    plt.xticks(rotation=45)

    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)



with tab5:
    st.header("🏢 Sector-Wise Performance")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=sector_avg_return, x='Return', y='Sector', palette='Spectral', ax=ax)
    ax.set_title("Average Yearly Return by Sector")
    st.pyplot(fig)

with tab6:
    st.header("🔗 Correlation Heatmap")
    fig, ax = plt.subplots(figsize=(15, 12))
    sns.heatmap(correlation_matrix, cmap="coolwarm", center=0, linewidths=0.5, ax=ax)
    st.pyplot(fig)

with tab7:
    st.header("📅 Monthly Top Gainers & Losers")
    months = monthly_df['Month'].unique()
    selected_month = st.selectbox("Select Month", sorted(months))
    monthly_data = monthly_df[monthly_df['Month'] == selected_month]
    top_5 = monthly_data.sort_values(by='Monthly Return (%)', ascending=False).head(5)
    bottom_5 = monthly_data.sort_values(by='Monthly Return (%)').head(5)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"Top 5 Gainers - {selected_month}")
        st.bar_chart(top_5.set_index("Ticker")["Monthly Return (%)"])
    with col2:
        st.subheader(f"Top 5 Losers - {selected_month}")
        st.bar_chart(bottom_5.set_index("Ticker")["Monthly Return (%)"])

st.success("✅ Dashboard loaded successfully.")
