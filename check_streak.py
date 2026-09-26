import os
import sys
import requests

LEETCODE_SESSION = os.environ["LEETCODE_SESSION"]
CSRF_TOKEN = os.environ["LEETCODE_CSRF"]
NTFY_TOPIC = os.environ["NTFY_TOPIC"]

GRAPHQL_URL = "https://leetcode.com/graphql"

def get_streak_status():
    query = {
        "query": """
            query getStreakCounter {
                streakCounter {
                    streakCount
                    daysSkipped
                    currentDayCompleted
                }
            }
        """
    }
    headers = {
        "Content-Type": "application/json",
        "Referer": "https://leetcode.com",
        "Cookie": f"LEETCODE_SESSION={LEETCODE_SESSION}; csrftoken={CSRF_TOKEN};",
        "X-CSRFToken": CSRF_TOKEN,
    }
    resp = requests.post(GRAPHQL_URL, json=query, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.json()["data"]["streakCounter"]

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
    status = get_streak_status()

    if status["currentDayCompleted"]:
        print("Already submitted today — no reminder needed.")
        return

    streak = status["streakCount"]
    if slot == "9:30pm":
        send_ntfy(
            "LeetCode Streak Reminder",
            f"No submission yet today. Current streak: {streak}. You have until midnight!",
            priority="default",
        )
    else:
        send_ntfy(
            "LAST CALL - LeetCode Streak",
            f"Still no submission! Streak of {streak} is about to break. ~90 min left.",
            priority="high",
        )

if __name__ == "__main__":
    main()
