import httpx

async def 获取曲绘(id):
    """获取曲目封面图片"""
    url = f"https://assets2.lxns.net/chunithm/jacket/{id}.png"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            return response.content
    except httpx.HTTPError as e:
        print(f"获取曲绘失败 (ID: {id}): {e}")
        return None
    except Exception as e:
        print(f"未知错误 (ID: {id}): {e}")
        return None