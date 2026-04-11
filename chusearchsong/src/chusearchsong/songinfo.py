import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW,PACK,NONE,HIDDEN, VISIBLE
import json
from chusearchsong.request import 获取歌曲详细信息

async def 曲目详情(返回按钮回调,song):

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
    
    # 曲目详情容器
    曲目详情容器 = toga.Box(style=Pack(direction=COLUMN, flex=1))
    newbox.add(曲目详情容器)
    
    # 上半部分
    # 上半部分 = toga.Box(style=Pack(direction=ROW))
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
        a=a+i['level']+" "

    难度=toga.Label(text=f"难度: {a}")
    曲目详情容器.add(难度)
    分割线=toga.Divider()
    曲目详情容器.add(分割线)

    #曲目详细信息表格
    # 曲目详细数据=await 获取歌曲详细信息(song['id'])
    # 曲目详细数据=曲目详细数据['difficulties']
    # 曲目各难度数据=[]
    # for i in 曲目详细数据:
    #     曲目各难度数据.append(i['notes'],i['note_designer'])
    # 曲目信息表格=toga.Table(
    #     headings=['难度','total','tap','hold','slide','air','flick','谱师'],
    #     data=曲目各难度数据
    # )
    # 曲目详情容器.add(曲目信息表格)
    # try:
    #     图片数据 = await 获取曲绘(song['id'])
    #     if 图片数据:
    #         import io
    #         图片流 = io.BytesIO(图片数据)
    #         图片 = toga.Image(src=图片流)
    #         图片视图 = toga.ImageView(image=图片, style=Pack(width=200, height=200, alignment='center'))
    #         曲目详情容器.add(图片视图)
    #     else:
    #         错误提示 = toga.Label(text="无法加载曲绘图片", style=Pack(padding=10))
    #         曲目详情容器.add(错误提示)
    # except Exception as e:
    #     print(f"加载图片失败: {e}")
    #     错误提示 = toga.Label(text=f"图片加载失败: {str(e)}", style=Pack(padding=10))
    #     曲目详情容器.add(错误提示)
    # 切换窗口内容
    return newbox