import os
import sys
import json
import requests
from datetime import datetime, timezone

LEETCODE_USERNAME = os.environ["LEETCODE_USERNAME"]
NTFY_TOPIC = os.environ["NTFY_TOPIC"]

GRAPHQL_URL = "https://leetcode.com/graphql"

def get_today_submission_count():
    query = {
        "query": """
            query userProfileCalendar($username: String!) {
                matchedUser(username: $username) {
                    submissionCalendar
                }
            }
        """,
        "variables": {"username": LEETCODE_USERNAME},
    }
    headers = {
        "Content-Type": "application/json",
        "Referer": "https://leetcode.com",
    }
    resp = requests.post(GRAPHQL_URL, json=query, headers=headers, timeout=15)
    resp.raise_for_status()
    matched_user = resp.json()["data"]["matchedUser"]

    if matched_user is None:
        raise ValueError(f"LeetCode user '{LEETCODE_USERNAME}' not found — check the username secret.")

    calendar = json.loads(matched_user["submissionCalendar"])

    today_utc = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    today_key = str(int(today_utc.timestamp()))

    return calendar.get(today_key, 0)

def send_ntfy(title, message, priority="default"):
    requests.post(
        f"https://ntfy.sh/{NTFY_TOPIC}",
        data=message.encode("utf-8"),
        headers={
            "Title": title,
            "Priority": priority,
            "Tags": "warning" if priority == "high" else "fire",
        },
        timeout=10,
    )

def main():
    slot = sys.argv[1] if len(sys.argv) > 1 else "9:30pm"
    count = get_today_submission_count()

    if count > 0:
        print(f"Already made {count} submission(s) today — no reminder needed.")
        return

    if slot == "9:30pm":
        send_ntfy(
            "LeetCode Streak Reminder",
            "No submission yet today. You have until midnight (UTC-based day)!",
            priority="default",
        )
    else:
        send_ntfy(
            "LAST CALL - LeetCode Streak",
            "Still no submission today! ~90 min left before the day resets.",
            priority="high",
        )

if __name__ == "__main__":
    main()
