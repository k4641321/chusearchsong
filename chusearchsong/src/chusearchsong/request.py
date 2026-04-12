import aiohttp
import os
from loguru import logger
# import asyncio
async def 获取曲绘(id, 缓存路径):
    """获取曲目封面图片"""
    url = f"https://assets2.lxns.net/chunithm/jacket/{id}.png"
    logger.info(f"正在获取曲绘图片: {url}")
    
    # 确保缓存目录存在
    图片缓存目录 = os.path.join(缓存路径, 'pic')
    os.makedirs(图片缓存目录, exist_ok=True)
    
    图片文件路径 = os.path.join(图片缓存目录, f"{id}.png")
    
    # 如果缓存文件已存在，直接读取返回
    if os.path.exists(图片文件路径):
        try:
            with open(图片文件路径, "rb") as f:
                数据 = f.read()
            logger.info(f'从缓存加载: {图片文件路径}')
            return 数据
        except Exception as e:
            logger.info(f"读取缓存失败: {e}")
    
    # 从网络获取
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    数据 = await response.read()
                    # 保存到缓存
                    with open(图片文件路径, "wb") as f:
                        f.write(数据)
                    logger.info(f'已缓存到: {图片文件路径}')
                    return 图片文件路径
                else:
                    logger.info(f"HTTP错误: {response.status}")
                    return None
    except Exception as e:
        logger.info(f"获取曲绘失败: {type(e).__name__}: {e}")
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
                    logger.info(f"HTTP错误: {response.status}")
                    return None
    except Exception as e:
        logger.info(f"获取信息失败: {type(e).__name__}: {e}")
        return None