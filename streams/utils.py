import requests


# 🔥 KICK FUNCTION (UNCHANGED)
def check_kick_live(username):
    try:
        url = f"https://kick.com/api/v2/channels/{username}"

        response = requests.get(url, timeout=5)
        data = response.json()

        livestream = data.get("livestream")
        playback = data.get("playback_url")

        # 🔥 CORRECT LOGIC
        if livestream:
            return {
                "is_live": True,
                "title": livestream.get("session_title"),
                "viewers": livestream.get("viewer_count") or 0,
                "thumbnail": data.get("user", {}).get("profile_pic"),
                "url": f"https://kick.com/{username}"
            }

        # playback exists but no livestream → NOT LIVE
        return {"is_live": False}

    except Exception as e:
        print("Kick Error:", e)
        return {"is_live": False}


def check_youtube_live_scrape(username):
    try:
        import re

        url = f"https://www.youtube.com/@{username}/live"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }

        response = requests.get(url, headers=headers, timeout=5)
        html = response.text

        # 🔴 QUICK CHECK (MOST IMPORTANT)
        if '"isLiveNow":true' not in html and '"isLive":true' not in html:
            return {"is_live": False}

        # 🔍 Extract video ID (more reliable)
        matches = re.findall(r'"videoId":"(.*?)"', html)

        if matches:
            video_id = matches[0]

            return {
                "is_live": True,
                "title": "Live Now",
                "thumbnail": f"https://unavatar.io/youtube/{username}",
                "viewers": 0,
                # 🔥 IMPORTANT CHANGE
                "url": f"https://www.youtube.com/@{username}/live"
            }

        return {"is_live": False}

    except Exception as e:
        print("YT Scrape Error:", e)
        return {"is_live": False}


# 🔥 MAIN ROUTER (UPDATED)
def get_stream_status(streamer):
    if streamer.platform == "kick":
        return check_kick_live(streamer.channel_id)

    elif streamer.platform == "youtube":
        return check_youtube_live_scrape(streamer.channel_id)

    else:
        return {"is_live": False}