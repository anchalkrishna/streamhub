import requests


# 🔥 KICK FUNCTION (UNCHANGED)
def check_kick_live(username):
    url = f"https://kick.com/api/v2/channels/{username}"

    try:
        response = requests.get(url)
        data = response.json()

        livestream = data.get("livestream")
        user = data.get("user", {})

        profile_pic = user.get("profile_pic")

        if livestream:
            return {
                "is_live": True,
                "title": livestream.get("session_title"),
                "viewers": livestream.get("viewer_count"),
                "thumbnail": profile_pic,
                "url": f"https://kick.com/{username}"
            }

        else:
            return {
                "is_live": False,
                "thumbnail": profile_pic
            }

    except Exception as e:
        print("Kick Error:", e)
        return {"is_live": False}


def check_youtube_live_scrape(username):
    try:
        import re

        url = f"https://www.youtube.com/@{username}/live"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers)
        html = response.text

        # 🔍 Try to find video ID from embedded JSON
        video_match = re.search(r'"videoId":"(.*?)"', html)

        if video_match:
            video_id = video_match.group(1)

            # 🔍 Check if it's actually live
            if '"isLiveNow":true' in html or '"isLive":true' in html:

                return {
                    "is_live": True,
                    "title": "Live Now",
                    "thumbnail": f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
                    "viewers": None,
                    "url": f"https://www.youtube.com/watch?v={video_id}"
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