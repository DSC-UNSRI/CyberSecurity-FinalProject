#!/usr/bin/env python3
import sys
import json
import requests

# ============ KONFIGURASI ============
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"
# Kalau server butuh proxy, isi di sini. Kalau tidak butuh, biarkan None.
PROXY = None
# Contoh kalau butuh proxy:
# PROXY = {"https": "http://PROXY_IP:PORT", "http": "http://PROXY_IP:PORT"}
# =====================================

LOG_FILE = "/var/ossec/logs/telegram_integration.log"


def log(msg):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(msg + "\n")
    except Exception:
        pass


def get_emoji(level):
    try:
        level = int(level)
    except Exception:
        return "⚪"
    if level >= 9:
        return "🔴"
    elif level >= 7:
        return "🟠"
    elif level >= 5:
        return "🟡"
    return "🟢"


def main():
    try:
        alert_file_path = sys.argv[1]
    except IndexError:
        log("ERROR: no alert file path passed as argv[1]")
        sys.exit(1)

    try:
        with open(alert_file_path) as f:
            alert_json = json.loads(f.read())
    except Exception as e:
        log(f"ERROR reading/parsing alert file: {e}")
        sys.exit(1)

    rule = alert_json.get("rule", {})
    agent = alert_json.get("agent", {})
    data = alert_json.get("data", {})

    alert_level = rule.get("level", "N/A")
    description = rule.get("description", "N/A")
    rule_id = rule.get("id", "N/A")
    agent_name = agent.get("name", "N/A")
    agent_ip = agent.get("ip", "N/A")
    timestamp = alert_json.get("timestamp", "N/A")
    src_ip = data.get("srcip", data.get("win", {}).get("eventdata", {}).get("ipAddress", "N/A"))
    user = data.get("dstuser", data.get("win", {}).get("eventdata", {}).get("targetUserName", "N/A"))

    emoji = get_emoji(alert_level)

    msg = (
        f"{emoji} *SECURITY ALERT*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📋 *Rule ID:* {rule_id}\n"
        f"⚠️ *Level:* {alert_level}\n"
        f"📌 *Description:* {description}\n"
        f"🖥️ *Agent:* {agent_name} ({agent_ip})\n"
        f"🌐 *Source IP:* {src_ip}\n"
        f"👤 *User:* {user}\n"
        f"🕐 *Time:* {timestamp}\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}

    try:
        if PROXY:
            resp = requests.post(url, json=payload, proxies=PROXY, timeout=10)
        else:
            resp = requests.post(url, json=payload, timeout=10)
        log(f"INFO: sent alert, status={resp.status_code}, body={resp.text[:200]}")
    except Exception as e:
        log(f"ERROR sending to telegram: {e}")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
