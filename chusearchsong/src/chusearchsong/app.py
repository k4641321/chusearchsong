"""
a app search chusong
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import json
from chusearchsong.tool import 返回歌曲json
from toga import Key
from chusearchsong.request import 获取曲绘
# import asyncio

class chusearchsong(toga.App):

    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN,flex=1))
        # 搜索部分
        搜索容器 = toga.Box(style=Pack(direction=ROW))
        self.搜索框 = toga.TextInput(placeholder="搜索...", style=Pack(flex=1))
        搜索容器.add(self.搜索框)
        搜索容器.add(toga.Button('搜索', style=Pack(width=75), on_press=self.点击搜索))
        self.结果容器 = toga.Box(style=Pack(direction=COLUMN, flex=1))
        main_box.add(搜索容器)
        # 筛选
        筛选容器 = toga.Box(style=Pack(direction=ROW, flex=1, height=75))
        # ... existing code ...
        self.分类筛选 = toga.Selection(items=[
            {"name": "分类", "id": None},
            {"name": "流行 & 动漫", "id": 0},
            {"name": "niconico", "id": 2},
            {"name": "东方Project", "id": 3},
            {"name": "原创", "id": 5},
            {"name": "其他游戏", "id": 6},
            {"name": "彩绿", "id": 7},
            {"name": "音击舞萌", "id": 9}
        ], accessor="name", style=Pack(flex=1))
# ... existing code ...
        # ... existing code ...
        self.版本筛选 = toga.Selection(items=[
            {"name": "版本", "version": None},
            {"name": "CHUNITHM", "version": 10000},
            {"name": "CHUNITHM PLUS", "version": 10500},
            {"name": "CHUNITHM AIR", "version": 11000},
            {"name": "CHUNITHM STAR", "version": 11500},
            {"name": "CHUNITHM AMAZON", "version": 12000},
            {"name": "CHUNITHM CRYSTAL", "version": 12500},
            {"name": "CHUNITHM PARADISE", "version": 13000},
            {"name": "CHUNITHM NEW", "version": 13500},
            {"name": "CHUNITHM SUN", "version": 14000},
            {"name": "CHUNITHM LUMINOUS", "version": 14500},
            {"name": "CHUNITHM FESTiVAL", "version": 15000}
        ], accessor="name", style=Pack(flex=1))
# ... existing code ...
        筛选容器.add(self.分类筛选)
        筛选容器.add(self.版本筛选)
        main_box.add(筛选容器)
        # 结果部分
        滑动条 = toga.ScrollContainer(content=self.结果容器, style=Pack(direction=COLUMN,flex=1))
        main_box.add(滑动条)
        #页面暂存
        self.页面暂存 = []
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


    def 曲目详情(self,widget,song):
        # 先保存当前页面到栈中（在检查之前）
        self.页面暂存.append(self.main_window.content)
        print(f"进入详情页，页面栈深度: {len(self.页面暂存)}")
        
        # 定义返回按钮的回调函数
        def 返回按钮回调(widget=None):
            if self.页面暂存:
                previous_content = self.页面暂存.pop()
                self.main_window.content = previous_content
                print(f"返回成功，剩余页面数: {len(self.页面暂存)}")
            else:
                print("已回到主页面")
        
        # 创建新的详情页面
        newbox = toga.Box(style=Pack(direction=COLUMN, flex=1))
        
        # 标题栏容器
        标题栏容器 = toga.Box(style=Pack(direction=ROW))
        返回按钮 = toga.Button(
            text="返回",
            style=Pack(flex=1, width=75),
            on_press=返回按钮回调
        )
        标题栏容器.add(返回按钮)
        newbox.add(标题栏容器)
        
        # 曲目详情容器
        曲目详情容器 = toga.Box(style=Pack(direction=COLUMN, flex=1))
        newbox.add(曲目详情容器)
        
        # 上半部分
        上半部分 = toga.Box(style=Pack(direction=ROW))
        曲目id=toga.Label(text=f"id: {song['id']}",style=Pack(flex=1))
        上半部分.add(曲目id)
        分类=toga.Label(text=f"分类: {song['genre']}",style=Pack(flex=1))
        上半部分.add(分类)
        曲目详情容器.add(上半部分)
        
        #下半部分
        下半部分 = toga.Box(style=Pack(direction=ROW))
        曲师=toga.Label(text=f"曲师: {song['artist']}",style=Pack(flex=1))
        下半部分.add(曲师)
        版本=toga.Label(text=f"版本: {song['zhversion']}",style=Pack(flex=1))
        下半部分.add(版本)
        曲目详情容器.add(下半部分)
        a=""
        for i in song["difficulties"]:
            a=a+i['level']+" "

        难度=toga.Label(text=f"难度: {a}")
        # 图片数据=await 获取曲绘(song['id'])
        # 图片=toga.Image(图片数据)

        曲目详情容器.add(难度)
        # 曲目详情容器.add(图片)
        # 切换窗口内容
        self.main_window.content = newbox
        print("点击详情")

    async def 点击搜索(self, widget=None):
        if self.搜索框.value == "" and self.分类筛选.value.id == None and self.版本筛选.value.version == None:
            print("空")
            return
        self.结果容器.clear()
        资源目录 = self.paths.app / "resources"
        曲目列表路径 = 资源目录/"list.json"
        with open(曲目列表路径, "r", encoding="UTF-8") as f:
            曲目列表 = json.load(f)
            f.close()
        结果 = []
        print(self.版本筛选.value.version)
        for i in 曲目列表["songs"]:
            if self.搜索框.value.lower() in i["title"].lower():
                if self.分类筛选.value.id == None and i["version"] == self.版本筛选.value.version:
                    单首曲目 =await 返回歌曲json(i["id"],i["title"],i["artist"],i["genre"],i["bpm"],i["version"],self.版本筛选.value.name,i["difficulties"])
                    结果.append(单首曲目)
                elif self.分类筛选.value.name == i["genre"] and self.版本筛选.value.version == None:
                    for j in 曲目列表["versions"]:
                        if i["version"] == j["version"]:
                            单首曲目 =await 返回歌曲json(i["id"],i["title"],i["artist"],i["genre"],i["bpm"],i["version"],j["title"],i["difficulties"])
                    结果.append(单首曲目)
                elif self.分类筛选.value.name == i["genre"] and i["version"] == self.版本筛选.value.version:
                    单首曲目 =await 返回歌曲json(i["id"],i["title"],i["artist"],i["genre"],i["bpm"],i["version"],self.版本筛选.value.name,i["difficulties"])
                    结果.append(单首曲目)
                elif self.版本筛选.value.version == None and self.分类筛选.value.id == None:
                    for j in 曲目列表["versions"]:
                        if i["version"] == j["version"]:
                           单首曲目 = await 返回歌曲json(i["id"],i["title"],i["artist"],i["genre"],i["bpm"],i["version"],j["title"],i["difficulties"])
                    结果.append(单首曲目)
        print(type(结果))
        for i in 结果:
            曲目盒子=toga.Box(id=f"box{i['id']}",style=Pack(direction=ROW))
            曲目盒子.add(toga.Label(id=i['id'],text=f"{i['id']}  -  {i['title']}    {i['genre']}  -  {i['zhversion']}", style=Pack(flex=1)))
            # 曲目盒子.add(toga.Button(id=f"button{i['id']}",text="详情",style=Pack(flex=1,width=75),on_press=lambda widget,song=i:asyncio.create_task(self.曲目详情(widget, song))))
            曲目盒子.add(toga.Button(id=f"button{i['id']}",text="详情",style=Pack(flex=1,width=75),on_press=lambda widget,song=i:self.曲目详情(widget, song)))
            self.结果容器.add(曲目盒子)
            self.结果容器.add(toga.Divider())
        # self.结果框.value=结果


def main():
    return chusearchsong()
