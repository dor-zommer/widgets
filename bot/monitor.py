import json
import os
import time
from pathlib import Path

import anthropic

from sources import get_cbs_recent, get_package_details, get_recent_packages
from telegram_bot import send_message

STATE_FILE = Path(__file__).parent / "state.json"
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL_MINUTES", 10)) * 60

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"datagov_ids": [], "cbs_ids": []}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def summarize(publication):
    """Ask Claude to write a short Hebrew summary of a new government publication."""
    prompt = (
        "אתה עוזר שמסכם פרסומים ממשלתיים בעברית בצורה קצרה וברורה.\n\n"
        "להלן מידע על פרסום חדש במאגרי הנתונים הממשלתיים של ישראל:\n\n"
        f"{json.dumps(publication, ensure_ascii=False, indent=2)}\n\n"
        "כתוב סיכום של 2-3 משפטים בעברית: מה הנתונים, מי פרסם, ולמה זה עשוי לעניין."
    )
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()


def format_datagov_notification(pkg, summary):
    title = pkg.get("title_translated", {}).get("he") or pkg.get("title", "ללא כותרת")
    org = pkg.get("organization", {}).get("title", "")
    url = f"https://data.gov.il/dataset/{pkg.get('name', '')}"
    text = (
        f"📢 <b>פרסום חדש ב-data.gov.il</b>\n\n"
        f"<b>{title}</b>\n"
        f"ארגון: {org}\n\n"
        f"{summary}\n\n"
        f'<a href="{url}">קישור למאגר</a>'
    )
    return text


def format_cbs_notification(item, summary):
    title = item.get("title", "ללא כותרת")
    text = (
        f"📊 <b>עדכון חדש מהלמ״ס</b>\n\n"
        f"<b>{title}</b>\n\n"
        f"{summary}"
    )
    return text


def check_datagov(state):
    packages = get_recent_packages(limit=50)
    known_ids = set(state["datagov_ids"])
    new_packages = [p for p in packages if p["id"] not in known_ids]

    for pkg in new_packages:
        details = get_package_details(pkg["id"])
        summary = summarize(details)
        message = format_datagov_notification(pkg, summary)
        send_message(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, message)
        print(f"[data.gov.il] sent: {pkg.get('title', pkg['id'])}")

    # Keep last 500 IDs to avoid unbounded growth
    all_ids = list(known_ids | {p["id"] for p in packages})
    state["datagov_ids"] = all_ids[-500:]


def check_cbs(state):
    items = get_cbs_recent(limit=20)
    known_ids = set(state["cbs_ids"])
    new_items = [i for i in items if str(i.get("id", "")) not in known_ids]

    for item in new_items:
        summary = summarize(item)
        message = format_cbs_notification(item, summary)
        send_message(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, message)
        print(f"[CBS] sent: {item.get('title', item.get('id', '?'))}")

    all_ids = list(known_ids | {str(i.get("id", "")) for i in items})
    state["cbs_ids"] = all_ids[-500:]


def run():
    print(f"Bot started. Polling every {POLL_INTERVAL // 60} minutes.")
    state = load_state()

    # On first run, seed known IDs without sending notifications
    if not state["datagov_ids"] and not state["cbs_ids"]:
        print("First run: seeding known IDs (no notifications sent).")
        packages = get_recent_packages(limit=50)
        state["datagov_ids"] = [p["id"] for p in packages]
        cbs_items = get_cbs_recent(limit=20)
        state["cbs_ids"] = [str(i.get("id", "")) for i in cbs_items]
        save_state(state)
        print(f"Seeded {len(state['datagov_ids'])} data.gov.il IDs and {len(state['cbs_ids'])} CBS IDs.")

    while True:
        try:
            check_datagov(state)
            check_cbs(state)
            save_state(state)
        except Exception as e:
            print(f"Error during poll: {e}")
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    run()
