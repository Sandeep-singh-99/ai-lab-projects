import streamlit as st
from news_scraper import get_news
from summarizer import summarize_news

st.title("📰 Daily News Summarizer Bot")

choice = st.selectbox("Choose Category", ["Tech", "Finance"])
feed = "https://feeds.feedburner.com/TechCrunch/" if choice == "Tech" else "https://www.investing.com/rss/news_301.rss"

if st.button("Summarize Today's News"):
    news = get_news(feed)
    summary = summarize_news(news)
    st.subheader("Summary:")
    st.write(summary)
