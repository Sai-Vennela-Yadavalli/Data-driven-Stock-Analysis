
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Data-driven Stock Analysis Dashboard", layout="wide")

# --- DB Connection ---
engine = create_engine("mysql+mysqlconnector://2jJrpvjwrA9Wt2x.root:0ZT6EVmzzpAYMnUB@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/Stock_Analysis")

# --- Sidebar Navigation ---
st.sidebar.title("📌 Navigation")
selection = st.sidebar.radio("Go to", [
    "Home",
    "Volatility Analysis",
    "Cumulative Returns",
    "Sector Performance",
    "Stock Correlation",
    "Gainers & Losers"
])

# --- Home Page ---
def home():
    st.title("📊 Data-driven Stock Analysis Dashboard")
    st.markdown("""
        <div style='padding: 1.5rem; background-color: #f8f9fa; border-radius: 10px;'>
            <h4 style='color: #343a40;'>Welcome to Sai's interactive Stock Analysis Dashboard powered by SQL + Streamlit + Plotly.</h4>
            <p style='color: #6c757d; font-size: 15px;'>
                This tool helps you:
                <ul>
                    <li>🔍 Analyze top-performing and underperforming stocks</li>
                    <li>⚡ Identify most volatile stocks in the market</li>
                    <li>🏭 Compare sector-wise yearly returns</li>
                    <li>📈 Track cumulative performance trends</li>
                    <li>📊 Understand stock correlation via heatmaps</li>
                    <li>📉 Review monthly gainers & losers dynamically</li>
                </ul>
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔎 Explore the Dashboard Sections:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**Volatility Analysis**\n\nDiscover the most unstable stocks by price swings.", icon="🔄")
    with col2:
        st.success("**Cumulative Returns**\n\nVisualize long-term performance of top 5 stocks.", icon="📈")
    with col3:
        st.warning("**Sector Performance**\n\nCompare average returns across all stock sectors.", icon="🏭")

    col4, col5, col6 = st.columns(3)
    with col4:
        st.error("**Gainers & Losers**\n\nSpot top movers and droppers month-by-month.", icon="📅")
    with col5:
        st.info("**Correlation Matrix**\n\nUnderstand how stocks move in relation to each other.", icon="🔗")
    
# --- Volatility ---
def volatility_analysis():
    st.header("🔄 Top 10 Most Volatile Stocks")
    query = "SELECT * FROM volatility_analysis ORDER BY volatility DESC LIMIT 10"
    df = pd.read_sql(query, engine)
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("📌 Most Volatile", df.iloc[0]["symbol"], f'{df.iloc[0]["volatility"]:.2f}')
        st.dataframe(df.style.format({"volatility": "{:.4f}"}))
    with col2:
        fig = px.bar(df, x='symbol', y='volatility', text='volatility', color='volatility',
                     color_continuous_scale=['#ffe0b2', '#fb8c00', '#e65100'],
                     title="🔥 Volatility: Top 10 Most Unstable Stocks", template='plotly_white')
        fig.update_traces(marker_line_width=1.5, marker_line_color='black',
                          texttemplate='%{text:.4f}', textposition='outside')
        fig.update_layout(font=dict(family="Segoe UI", size=13))
        st.plotly_chart(fig, use_container_width=True)

# --- Cumulative Returns ---
def cumulative_return():
    st.header("📈 Top 5 Cumulative Returns Over Time")
    query = "SELECT * FROM top_5_cumulative_return"
    df = pd.read_sql(query, engine)
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        final_returns = df.groupby('symbol')['cumulative_return'].last().reset_index()
        top5_symbols = final_returns.sort_values(by='cumulative_return', ascending=False).head(5)['symbol']
        top5_df = df[df['symbol'].isin(top5_symbols)]
        fig = px.line(top5_df, x='date', y='cumulative_return', color='symbol',
                      title="📈 Cumulative Return Trends (Top 5)", template='plotly_white')
        fig.update_layout(xaxis_title="Date", yaxis_title="Cumulative Return", font=dict(family="Segoe UI"))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("❌ 'date' column not found.")

# --- Sector-wise Performance ---
def sector_performance():
    st.header("🏭 Sector-wise Average Yearly Return")
    query = "SELECT sector, AVG(yearly_return) AS avg_return FROM sectorwise_performance GROUP BY sector"
    df = pd.read_sql(query, engine)
    st.subheader("📊 Sector Performance")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.dataframe(df)
    with col2:
        fig = px.bar(df, x='sector', y='avg_return', color='avg_return', text='avg_return',
                     title="Sector-wise Avg Return", template='plotly_white', color_continuous_scale='purples')
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

# --- Correlation ---
def stock_correlation():
    st.header("📊 Stock Price Correlation Heatmap")
    query = "SELECT * FROM correlation_matrix"
    df = pd.read_sql(query, engine)
    fig, ax = plt.subplots(figsize=(25, 20))
    sns.heatmap(df.set_index("symbol"), cmap="coolwarm", annot=True, fmt=".2f", linewidths=0.5, ax=ax)
    st.pyplot(fig)

# --- Gainers & Losers ---
def gainers_losers():
    st.header("📅 Monthly Gainers & Losers")
    months_query = "SELECT DISTINCT month FROM monthly_returns ORDER BY FIELD(month, 'January','February','March','April','May','June','July','August','September','October','November','December')"
    months = pd.read_sql(months_query, engine)["month"].tolist()
    selected_month = st.selectbox("Select a Month", months)
    query = f"SELECT * FROM monthly_returns WHERE month = '{selected_month}'"
    df = pd.read_sql(query, engine)
    if df.empty:
        st.warning("No data available for selected month.")
        return
    top5_gainers = df.sort_values('monthly_return', ascending=False).head(5)
    top5_losers = df.sort_values('monthly_return', ascending=True).head(5)
    st.subheader("📈 Top 5 Gainers")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.dataframe(top5_gainers)
    with col2:
        fig_gain = px.bar(top5_gainers, x='symbol', y='monthly_return', color='monthly_return', text='monthly_return',
                          title=f"Top Gainers – {selected_month}", template='seaborn', color_continuous_scale='Greens')
        fig_gain.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        st.plotly_chart(fig_gain, use_container_width=True)
    st.subheader("📉 Top 5 Losers")
    col3, col4 = st.columns([1, 2])
    with col3:
        st.dataframe(top5_losers)
    with col4:
        fig_lose = px.bar(top5_losers, x='symbol', y='monthly_return', color='monthly_return', text='monthly_return',
                          title=f"Top Losers – {selected_month}", template='seaborn', color_continuous_scale='Reds')
        fig_lose.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        st.plotly_chart(fig_lose, use_container_width=True)

# --- Routing ---
pages = {
    "Home": home,
    "Volatility Analysis": volatility_analysis,
    "Cumulative Returns": cumulative_return,
    "Sector Performance": sector_performance,
    "Stock Correlation": stock_correlation,
    "Gainers & Losers": gainers_losers
}
pages[selection]()
