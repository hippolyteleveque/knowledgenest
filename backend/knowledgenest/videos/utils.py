from pytube import YouTube


def extract_info_from_url(url: str):
    yt = YouTube(url)
    infos = {
        "title": yt.title or "Unknown",
        "description": yt.description or "Unknown",
        "imageUrl": yt.thumbnail_url or "Unknown",
        "publishDate": (
            yt.publish_date.strftime("%Y-%m-%d %H:%M:%S") if yt.publish_date else None
        ),
        "author": yt.author or "Unknown",
    }
    return infos
