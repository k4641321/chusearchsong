import aiohttp
import os
# import asyncio
async def 获取曲绘(id,缓存路径):
    """获取曲目封面图片"""
    url = f"https://assets2.lxns.net/chunithm/jacket/{id}.png"
    print(url)
    # if os.path.dirname(缓存路径):
    #     os.makedirs(os.path.dirname(缓存路径), exist_ok=True)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    数据 = await response.read()
                    with open(f"{缓存路径}\{id}.png", "wb") as f:
                        f.write(数据)
                    print(f'路径:{缓存路径}')
                    return 数据
                else:
                    print(f"HTTP错误: {response.status}")
                    return None
    except Exception as e:
        print(f"获取曲绘失败: {type(e).__name__}: {e}")
        return None

# if __name__ == "__main__":
#     asyncio.run(获取曲绘(3))

async def 获取歌曲详细信息(id):
    url = f"https://maimai.lxns.net/api/v0/chunithm/song/{id}"
    #print(url)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    数据 = await response.text()
                    return 数据
                else:
                    print(f"HTTP错误: {response.status}")
                    return None
    except Exception as e:
        print(f"获取信息失败: {type(e).__name__}: {e}")
        return None