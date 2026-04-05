import aiohttp
# import asyncio
async def 获取曲绘(id):
    """获取曲目封面图片"""
    url = f"https://assets2.lxns.net/chunithm/jacket/{id}.png"
    print(url)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    数据 = await response.read()
                    return 数据
                else:
                    print(f"HTTP错误: {response.status}")
                    return None
    except Exception as e:
        print(f"获取曲绘失败: {type(e).__name__}: {e}")
        return None

# if __name__ == "__main__":
#     asyncio.run(获取曲绘(3))