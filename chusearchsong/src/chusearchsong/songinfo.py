import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW,PACK,NONE,HIDDEN, VISIBLE
import json
from chusearchsong.request import 获取歌曲详细信息,获取曲绘
import asyncio

async def 曲目详情(返回按钮回调,song,缓存路径):

    newbox = toga.Box(style=Pack(direction=COLUMN, flex=1))
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
    # 曲目详情容器
    曲目详情容器 = toga.Box(style=Pack(direction=COLUMN, flex=1))
    newbox.add(曲目详情容器)
    
    #图片
    async def 加载曲绘():
        #图片容器 = toga.Box(style=Pack(direction=COLUMN, flex=1))
        try:
            图片路径 = await 获取曲绘(song['id'],缓存路径)
            图片= toga.Image(图片路径)
            图片容器=toga.ImageView(图片)
            曲绘容器.add(图片容器)
        except Exception as e:
            print(f"加载图片失败: {e}")
            曲绘容器.add(toga.Label(text="加载图片失败"))
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
            曲目详情容器.add(曲目信息表格)
        except Exception as e:
            print(f"获取歌曲详细信息失败: {e}")
            错误提示 = toga.Label(text=f"获取歌曲详细信息失败: {str(e)}", style=Pack(padding=10))
            曲目详情容器.add(错误提示)

    asyncio.create_task(加载曲绘())
    asyncio.create_task(加载曲目详细信息())
    
    # 切换窗口内容
    return newbox