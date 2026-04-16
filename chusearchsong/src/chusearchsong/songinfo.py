import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW,PACK,NONE,HIDDEN, VISIBLE
import json
from chusearchsong.request import 获取歌曲详细信息,获取曲绘,获取歌曲预览
import asyncio
from loguru import logger
async def 曲目详情(返回按钮回调,song,缓存路径,self):
    rootbox = toga.Box(style=Pack(direction=COLUMN,flex=1))

    newbox = toga.Box(style=Pack(direction=COLUMN, flex=1))
    滚动条=toga.ScrollContainer(content=newbox,style=Pack(direction=COLUMN,flex=1))
    rootbox.add(滚动条)
    # 标题栏容器
    标题栏容器 = toga.Box(style=Pack(direction=ROW))
    返回按钮 = toga.Button(
        text="返回",
        style=Pack(flex=1),
        on_press=返回按钮回调
    )
    标题栏容器.add(返回按钮)
    newbox.add(标题栏容器)
    
    曲绘容器=toga.Box(style=Pack(direction=ROW,flex=1))
    newbox.add(曲绘容器)

    # 歌曲预览容器=toga.Box(style=Pack(direction=COLUMN,flex=1))
    # newbox.add(歌曲预览容器)

    # 曲目详情容器
    曲目详情容器 = toga.Box(style=Pack(direction=COLUMN, flex=1))
    newbox.add(曲目详情容器)
    
    async def 切换收藏状态(song, self, 收藏按钮):
        from chusearchsong.tool import 收藏, 取消歌曲收藏
        
        if 收藏按钮.text == "添加收藏":
            await 收藏(song, self)
            收藏按钮.text = "取消收藏"
            收藏按钮.on_press = lambda widget: asyncio.create_task(切换收藏状态(song, self, 收藏按钮))
        else:
            await 取消歌曲收藏(song, self)
            收藏按钮.text = "添加收藏"
            收藏按钮.on_press = lambda widget: asyncio.create_task(切换收藏状态(song, self, 收藏按钮))
    
    async def 加载曲绘():
        #图片容器 = toga.Box(style=Pack(direction=COLUMN, flex=1))
        try:
            图片路径 = await 获取曲绘(song['id'],缓存路径)
            图片= toga.Image(src=图片路径)
            图片容器=toga.ImageView(图片)
            曲绘容器.add(图片容器)
        except Exception as e:
            print(f"加载图片失败: {e}")
            曲绘容器.add(toga.Label(text=f"加载图片失败：{e}"))
            #曲目详情容器.add(图片容器)

    # 上半部分
    # 上半部分 = toga.Box(style=Pack(direction=ROW))

    分割线=toga.Divider()
    曲目详情容器.add(分割线)

    曲目id=toga.Label(text=f"id: {song['id']}",style=Pack(flex=1))
    曲目详情容器.add(曲目id)
    分类=toga.Label(text=f"分类: {song['genre']}",style=Pack(flex=1))
    曲目详情容器.add(分类)
    # 曲目详情容器.add(上半部分)
    
    #下半部分
    # 下半部分 = toga.Box(style=Pack(direction=ROW))
    曲师=toga.Label(text=f"曲师: {song['artist']}",style=Pack(flex=1))
    曲目详情容器.add(曲师)
    版本=toga.Label(text=f"版本: {song['zhversion']}",style=Pack(flex=1))
    曲目详情容器.add(版本)
    # 曲目详情容器.add(下半部分)
    a=""
    for i in song["difficulties"]:
        a=a+i['level']+r" \ "

    难度=toga.Label(text=f"难度: {a}")
    曲目详情容器.add(难度)
    分割线2=toga.Divider()
    曲目详情容器.add(分割线2)
    曲目信息表格容器=toga.Box(style=Pack(direction=COLUMN, flex=1))
    曲目详情容器.add(曲目信息表格容器)

    with open(self.配置文件路径,"r",encoding="utf-8") as f:
        收藏目录路径=json.load(f)["favorites_path"]
    
    已收藏 = False
    if 收藏目录路径:
        try:
            with open(收藏目录路径,"r",encoding="utf-8") as f:
                收藏目录=json.load(f)["songs"]
                for i in 收藏目录:
                    if i["id"]==song["id"]:
                        已收藏 = True
                        break
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            已收藏 = False
    
    if 已收藏:
        添加收藏按钮=toga.Button(
            text="取消收藏",
            style=Pack(flex=1),
            on_press=lambda widget:asyncio.create_task(切换收藏状态(song,self,添加收藏按钮))
        )
    else:
        添加收藏按钮=toga.Button(
            text="添加收藏",
            style=Pack(flex=1),
            on_press=lambda widget:asyncio.create_task(切换收藏状态(song,self,添加收藏按钮))
        )
            
    曲目详情容器.add(添加收藏按钮)

    #曲目详细信息表格
    async def 加载曲目详细信息():
        try:
            曲目详细数据=json.loads(await 获取歌曲详细信息(song['id']))
            #print(曲目详细数据)
            曲目详细数据=曲目详细数据['difficulties']
            曲目各难度数据=[]
            for i in 曲目详细数据:
                单难度=(i['level_value'],i['notes']['total'],i['notes']['tap'],i['notes']['hold'],i['notes']['slide'],i['notes']['air'],i['notes']['flick'],i['note_designer'])
                曲目各难度数据.append(单难度)
            曲目信息表格=toga.Table(
                headings=['难度','total','tap','hold','slide','air','flick','谱师'],
                data=曲目各难度数据
            )
            曲目信息表格容器.add(曲目信息表格)
        except Exception as e:
            print(f"获取歌曲详细信息失败: {e}")
            错误提示 = toga.Label(text=f"获取歌曲详细信息失败: {str(e)}", style=Pack(padding=10))
            曲目详情容器.add(错误提示)

    # async def 加载歌曲预览():
    #     try:
    #         歌曲预览 = toga.WebView()
    #         歌曲路径=await 获取歌曲预览(song["id"],缓存路径)
    #         await 歌曲预览.load_url(f"{歌曲路径}")
    #     except Exception as e:
    #         logger.error(f"获取歌曲预览失败: {e}")
    #         错误提示 = toga.Label(text=f"获取歌曲预览失败: {str(e)}")
    #         歌曲预览容器.add(错误提示)
    asyncio.create_task(加载曲绘())
    asyncio.create_task(加载曲目详细信息())
    # asyncio.create_task(加载歌曲预览())
    
    # 切换窗口内容
    return rootbox