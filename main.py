import streamlit as st
import json
import requests
import notion_utils
from datetime import datetime, timezone

st.title("ChatGPTチャット一覧ビューア")

# データ読み込み
with open("data/chats.json", "r", encoding="utf-8") as f:
    chats = json.load(f)

# チャットタイトル一覧を取得
chat_titles = [chat["title"] for chat in chats]

# チャット選択UI
selected_title = st.selectbox("チャットを選んでください", chat_titles)

# 選ばれたチャットを取得
selected_chat = next((chat for chat in chats if chat["title"] == selected_title), None)

if selected_chat:
    st.subheader("本文")
    st.text(selected_chat["content"])

existing_chat_ids = notion_utils.get_existing_chat_ids()

if selected_chat["id"] in existing_chat_ids:
    st.info("このチャットはすでに保存済みです。")
else:
    if st.button("📝 Notionに保存する"):
        if notion_utils.save_to_notion(selected_chat):
            st.success(f"「{selected_chat['title']}」を Notion に保存しました！")
        else:
            st.error("保存に失敗しました。")



