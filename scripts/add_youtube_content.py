import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

try:
    from pytube import YouTube
except:
    print("Did you forget to source pytube env?")
    print("source ~/Projects/download_youtube/venv/bin/activate")
    exit()

_KEEP_CHARACTERS = {".", "_", " ", "-"}
_REPLACE_CHARACTERS = {" ": "_"}


def safe_str(unsafe: str) -> str:
    if not isinstance(unsafe, str):
        raise ValueError(f"{unsafe} ({type(unsafe)}) not a string")
    return "".join(
        _REPLACE_CHARACTERS.get(c, c)
        for c in unsafe
        if c.isalnum() or c in _KEEP_CHARACTERS
    ).rstrip()


TEMPLATE = """
---
title: "{title}"
date: "{date}"
draft: false
tags:
{tags}
cover:
  image: "https://img.youtube.com/vi/{youtube_id}/0.jpg"
  alt: "{title}"
  relative: false
---

{{{{< youtube id={youtube_id} >}}}}

"""

DATESTR_FORMAT = "%Y-%m-%dT%H:%M:%S+02:00"
FILE_DATE_FORMAT = "%Y-%m-%d"
TAG_LINE_FORMAT = " - {tag}"


def join_tags(tags: list[str]) -> str:
    return os.linesep.join([TAG_LINE_FORMAT.format(tag=t) for t in tags])


def main(youtube: str, tags: list[str]):
    if not youtube.startswith("http"):
        youtube = f"https://www.youtube.com/watch?v={youtube}"
    v = YouTube(url=youtube)

    publish_date = v.publish_date
    if not isinstance(publish_date, datetime):
        publish_date = datetime.now()

    tag_str = join_tags(tags)
    content = TEMPLATE.format(
        youtube_id=v.video_id,
        date=publish_date.strftime(DATESTR_FORMAT),
        tags=tag_str,
        title=v.title,
    )
    destination = Path(
        f"content/posts/{publish_date.strftime(FILE_DATE_FORMAT)}_{safe_str(v.title).lower()}.md"
    )
    destination.write_text(content)

    print(f"Stored {destination}")
    print("Remember to add description from YouTube.")


if __name__ == "__main__":
    import sys

    video = sys.argv[1]
    tags = sys.argv[2:]
    main(video, tags)
