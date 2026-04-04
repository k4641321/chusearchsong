async def 返回歌曲json(id,title,artist,genre,bpm,version,zhversion,difficulties):
    data = {
        "id": id,
        "title": title,
        "artist":artist,
        "genre": genre,
        "bpm": bpm,
        "version": version,
        "zhversion":zhversion,
        "difficulties":difficulties
    }
    return data