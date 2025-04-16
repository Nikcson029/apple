import streamlit as st 
import pandas as pd 
import yfinance as yf 
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Анализ акций Apple",
    layout="wide"
)

st.title(" Анализ котировок Apple")


st.write("""
Это приложение показывает исторические данные о котировках акций компании Apple.
Используйте настройки ниже для выбора периода анализа.
""")


with st.sidebar:
    st.header(" Настройки")
    start_date = st.date_input("Начальная дата", pd.to_datetime("2020-01-01"))
    end_date = st.date_input("Конечная дата", pd.to_datetime("today"))
    period = st.selectbox("Период", ["1d", "1wk", "1mo"], index = 2)


@st.cache_data(ttl=3600)
def load_data(start, end, interval):
    try:
        data = yf.download('AAPL', start=str(start), end=str(end), interval=interval, progress=False)
        if data.empty:
            data = yf.Ticker("AAPL").history(start=str(start), end=str(end), interval=interval)
        return data
    except Exception as e:
        st.error(f"Ошибка загрузки данных: {e}")
        return pd.DataFrame()

try:
    data = load_data(start_date, end_date, period)
    
    if data.empty:
        st.warning("Не удалось загрузить данные. Попробуйте изменить параметры.")
    else:
    
        st.subheader("Последние данные")
        st.dataframe(data.tail().style.format("{:.2f}"), use_container_width = True)
          
        st.subheader("График цен закрытия")
        st.line_chart(data['Close'])
              
        st.subheader("Основные статистики")
        st.table(data.describe().style.format("{:.2f}"))
               
        st.subheader("Информация о компании")
        info = yf.Ticker("AAPL").info
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Текущая цена", f"${info.get('regularMarketPrice', 'N/A')}")
            st.metric("Рыночная капитализация", f"${info.get('marketCap', 'N/A'):,}")
        
        with col2:
            st.metric("P/E (Коэф. P/E)", info.get('trailingPE', 'N/A'))
            dividend_yield = info.get('dividendYield', 0)
            st.metric("Дивидендная доходность", f"{dividend_yield*100:.2f}%" if dividend_yield else '0%')

except Exception as e:
    st.error(f"Произошла ошибка: {str(e)}")