import requests
import streamlit as st

def save_to_notion(chat):
    import requests
    from datetime import datetime, timezone

    notion_token = st.secrets["notion"]["token"]
    database_id = st.secrets["notion"]["database_id"]
    url = "https://api.notion.com/v1/pages"

    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    lines = [line.strip() for line in chat["content"].split("\n") if line.strip()]
    content_blocks = []
    for i, line in enumerate(lines):
        block_type = "heading_2" if i == 0 else "paragraph"
        content_blocks.append({
            "object": "block",
            "type": block_type,
            block_type: {
                "rich_text": [{"text": {"content": line}}]
            }
        })

    now = datetime.now(timezone.utc).isoformat()

    data = {
        "parent": {"database_id": database_id},
        "properties": {
            "タイトル": {"title": [{"text": {"content": chat["title"]}}]},
            "チャットID": {"rich_text": [{"text": {"content": chat["id"]}}]},
            "保存日時": {"date": {"start": now}}
        },
        "children": content_blocks
    }

    response = requests.post(url, headers=headers, json=data)
    return response.status_code in [200, 201]


def get_existing_chat_info():
    notion_token = st.secrets["notion"]["token"]
    database_id = st.secrets["notion"]["database_id"]
    url = f"https://api.notion.com/v1/databases/{database_id}/query"

    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    response = requests.post(url, headers=headers)
    results = response.json().get("results", [])

    chat_info = []
    for page in results:
        props = page["properties"]

        if "チャットID" in props and "rich_text" in props["チャットID"]:
            id_parts = props["チャットID"]["rich_text"]
#           saved_at = props.get("保存日時", {}).get("date", {}).get("start", None)
            date_property = props.get("保存日時", None)
            saved_at = None

            if date_property and "date" in date_property and date_property["date"]:
                saved_at = date_property["date"].get("start", None)

            if id_parts:
                chat_id = id_parts[0]["text"]["content"]
                chat_info.append({
                    "id": chat_id,
                    "saved_at": saved_at  # ISO形式の文字列（例：2025-05-13T11:00:00Z）
                })

    return chat_info

def get_existing_chat_ids():
    notion_token = st.secrets["notion"]["token"]
    database_id = st.secrets["notion"]["database_id"]
    url = f"https://api.notion.com/v1/databases/{database_id}/query"

    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    response = requests.post(url, headers=headers)
    results = response.json().get("results", [])

    existing_ids = []
    for page in results:
        props = page["properties"]
        if "チャットID" in props and "rich_text" in props["チャットID"]:
            text_parts = props["チャットID"]["rich_text"]
            if text_parts:
                existing_ids.append(text_parts[0]["text"]["content"])

    return existing_ids

