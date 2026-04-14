"""
答辩框架与史山代码写的中二查歌
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW,PACK,NONE,HIDDEN, VISIBLE
import json
#from chusearchsong.tool import 返回歌曲json
from toga import Key
from chusearchsong.request import 获取曲绘
import asyncio
from loguru import logger

class chusearchsong(toga.App):

    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN,flex=1))

        #命令绑定

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
        self.难度筛选前=toga.Selection(items=[
            {"name": "难度下限","level_value":0},
            {"name": "1","level_value":1},
            {"name": "2","level_value":2},
            {"name": "3","level_value":3},
            {"name": "4","level_value":4},
            {"name": "5","level_value":5},
            {"name": "6","level_value":6},
            {"name": "7","level_value":7},
            {"name": "7+","level_value":7.5},
            {"name": "8","level_value":8},
            {"name": "8+","level_value":8.5},
            {"name": "9","level_value":9},
            {"name": "9+","level_value":9.5},
            {"name": "10","level_value":10},
            {"name": "10+","level_value":10.5},
            {"name": "11","level_value":11},
            {"name": "11+","level_value":11.5},
            {"name": "12","level_value":12},
            {"name": "12+","level_value":12.5},
            {"name": "13","level_value":13},
            {"name": "13+","level_value":13.5},
            {"name": "14","level_value":14},
            {"name": "14+","level_value":14.5},
            {"name": "15","level_value":15},
            {"name": "15+","level_value":15.5},

        ], accessor="name", style=Pack(flex=1))
        self.难度筛选后=toga.Selection(items=[
            {"name": "难度上限","level_value":0},
            {"name": "1","level_value":1},
            {"name": "2","level_value":2},
            {"name": "3","level_value":3},
            {"name": "4","level_value":4},
            {"name": "5","level_value":5},
            {"name": "6","level_value":6},
            {"name": "7","level_value":7},
            {"name": "7+","level_value":7.9},
            {"name": "8","level_value":8},
            {"name": "8+","level_value":8.9},
            {"name": "9","level_value":9},
            {"name": "9+","level_value":9.9},
            {"name": "10","level_value":10},
            {"name": "10+","level_value":10.9},
            {"name": "11","level_value":11},
            {"name": "11+","level_value":11.9},
            {"name": "12","level_value":12},
            {"name": "12+","level_value":12.9},
            {"name": "13","level_value":13},
            {"name": "13+","level_value":13.9},
            {"name": "14","level_value":14},
            {"name": "14+","level_value":14.9},
            {"name": "15","level_value":15},
            {"name": "15+","level_value":15.9},

        ], accessor="name", style=Pack(flex=1))
        筛选容器.add(self.分类筛选)
        筛选容器.add(self.版本筛选)
        筛选容器.add(self.难度筛选前)
        筛选容器.add(self.难度筛选后)
        main_box.add(筛选容器)
        # 结果部分
        self.滑动条 = toga.ScrollContainer(content=self.结果容器, style=Pack(direction=COLUMN,flex=1))
        # main_box.add(滑动条)
        #页面暂存
        self.页面暂存 = []
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


    async def 曲目详情(self,widget,song):
        # 先保存当前页面到栈中（在检查之前）
        logger.info(self.commands.items)
        self.页面暂存.append(self.main_window.content)

        # self.main_window = toga.MainWindow(title="曲目详情")
        # print(f"进入详情页，页面栈深度: {len(self.页面暂存)}")
        
        # 定义返回按钮的回调函数
        
        def 返回按钮回调(widget=None):
            if self.页面暂存:
                previous_content = self.页面暂存.pop()
                self.main_window.content = previous_content
                # print(f"返回成功，剩余页面数: {len(self.页面暂存)}")
            # else:
                # print("已回到主页面")

        # 返回命令=toga.Command(返回按钮回调,text='返回',shortcut=Key.F)
        # self.commands.add(返回命令)
        # 创建新的详情页面
        from chusearchsong.songinfo import 曲目详情
        newbox = await 曲目详情(返回按钮回调,song,self.paths.cache)
        # tipdialog=toga.InfoDialog("提示", f"{self.paths.cache}")
        # await self.main_window.dialog(tipdialog)
        self.main_window.content = newbox
        # print("点击详情")

    def 点击搜索(self, widget=None):
        asyncio.create_task(self.执行搜索())
    async def 执行搜索(self):
        if self.搜索框.value == "" and self.分类筛选.value.id == None and self.版本筛选.value.version == None:
            # print("空")
            return
        main_box = self.main_window.content
        if self.滑动条 in main_box.children:
            main_box.remove(self.滑动条)
        self.结果容器.clear()
        from chusearchsong.search import 曲目搜索
        曲目数据路径= self.paths.app / 'resources' / 'list.json'
        曲目盒子=await 曲目搜索(曲目数据路径,self.分类筛选.value.name,self.版本筛选.value.version,self.版本筛选.value.name,self.难度筛选前.value.level_value,self.难度筛选后.value.level_value,self.搜索框.value,self.曲目详情)
        main_box.add(self.滑动条)
        # main_box.add(self.结果容器)
        # self.结果框.value=结果
        self.结果容器.add(曲目盒子)
        self.结果容器.add(toga.Divider())

def main():
    return chusearchsong()
