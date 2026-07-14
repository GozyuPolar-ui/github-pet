import os
import re
import sys
import requests
from datetime import datetime, timezone

GITHUB_TOKEN = os.environ.get("GH_TOKEN")
USERNAME = os.environ.get("GH_USERNAME")

GRAPHQL_URL = "https://api.github.com/graphql"

ASSET_MAP = {
    "happy": "assets/dog_happy.png",
    "walk": "assets/dog_Walk.png",
    "idle": "assets/dog_Idle.png",
    "dead": "assets/dog_dead.png",
}


def fetch_contributions(username, token):
    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            weeks {
              contributionDays {
                date
                contributionCount
              }
            }
          }
        }
      }
    }
    """
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.post(
        GRAPHQL_URL,
        json={"query": query, "variables": {"login": username}},
        headers=headers,
    )
    resp.raise_for_status()
    data = resp.json()
    weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    days = []
    for week in weeks:
        for day in week["contributionDays"]:
            days.append((day["date"], day["contributionCount"]))
    days.sort(key=lambda x: x[0])
    return days


def compute_state(days):
    if not days:
        return "idle", 0

    today_str = datetime.now(timezone.utc).date().isoformat()
    today_count = 0
    for date_str, count in days:
        if date_str == today_str:
            today_count = count
            break

    streak = 0
    for date_str, count in reversed(days):
        if date_str == today_str:
            continue
        if count > 0:
            streak += 1
        else:
            break

    if today_count > 0 and streak >= 3:
        return "happy", streak
    elif today_count > 0:
        return "walk", streak

    gap = 0
    for date_str, count in reversed(days):
        if date_str == today_str:
            continue
        if count == 0:
            gap += 1
        else:
            break

    if gap >= 5:
        return "dead", streak
    return "idle", streak


def update_readme(state, streak):
    """Update baris gambar pet di README.md, plus cache-buster biar GitHub gak nampilin gambar lama."""
    asset_path = ASSET_MAP[state]
    timestamp = int(datetime.now(timezone.utc).timestamp())
    new_line = f"![pet]({asset_path}?t={timestamp})"

    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    if "![pet](" in content:
        content = re.sub(r"!\[pet\]\([^)]*\)", new_line, content)
    else:
        content = new_line + "\n\n" + content

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

    print(f"State: {state}, streak: {streak} hari. README diupdate ke {asset_path}.")


def main():
    if not GITHUB_TOKEN or not USERNAME:
        print("GH_TOKEN atau GH_USERNAME belum di-set di environment variable.")
        sys.exit(1)

    days = fetch_contributions(USERNAME, GITHUB_TOKEN)
    state, streak = compute_state(days)
    update_readme(state, streak)


if __name__ == "__main__":
    main()