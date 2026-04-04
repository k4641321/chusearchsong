"""
a app search chusong
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import json

class chusearchsong(toga.App):
    

    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))
        #搜索部分
        搜索容器=toga.Box(style=Pack(direction=ROW))
        self.搜索框=toga.TextInput(placeholder="搜索...",style=Pack(flex=1))
        搜索容器.add(self.搜索框)
        搜索容器.add(toga.Button('搜索',style=Pack(width=75),on_press=self.点击搜索))
        self.结果容器=toga.Box(style=Pack(direction=COLUMN,flex=1))
        main_box.add(搜索容器)
        #筛选
        筛选容器=toga.Box(style=Pack(direction=ROW,flex=1,height=75))
        # ... existing code ...
        self.分类筛选=toga.Selection(items=[
            {"name": "分类", "id": None},
            {"name": "流行 & 动漫", "id": 0},
            {"name": "niconico", "id": 2},
            {"name": "东方Project", "id": 3},
            {"name": "原创", "id": 5},
            {"name": "其他游戏", "id": 6},
            {"name": "彩绿", "id": 7},
            {"name": "音击舞萌", "id": 9}
        ],accessor="name",style=Pack(flex=1))
# ... existing code ...
        # ... existing code ...
        self.版本筛选=toga.Selection(items=[
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
        ],accessor="name",style=Pack(flex=1))
# ... existing code ...
        筛选容器.add(self.分类筛选)
        筛选容器.add(self.版本筛选)
        main_box.add(筛选容器)
        #结果部分
        main_box.add(self.结果容器)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    async def 点击搜索(self,widget=None):
        if self.搜索框.value=="" and self.分类筛选.value.id==None and self.版本筛选.value.version==None:
            print("空")
            return
        self.结果容器.clear()
        资源目录=self.paths.app/ "resources"
        曲目列表路径=资源目录/"list.json"
        with open(曲目列表路径,"r",encoding="UTF-8") as f:
            曲目列表=json.load(f)
            f.close()
        结果=[]
        print(self.版本筛选.value.version)
        for i in 曲目列表["songs"]:
            if self.搜索框.value.lower() in i["title"].lower():
                if self.分类筛选.value.id==None and i["version"]==self.版本筛选.value.version:
                    单首曲目={
                            "icon":None,
                            "title":f"{i['id']} - {i['title']}",
                            "orther":f"{i['genre']} - {self.版本筛选.value.name}"
                        }
                    结果.append(单首曲目)
                elif self.分类筛选.value.name==i["genre"] and self.版本筛选.value.version==None:
                    for j in 曲目列表["versions"]:
                        if i["version"]==j["version"]:
                            单首曲目={
                                    "icon":None,
                                    "title":f"{i['id']} - {i['title']}",
                                    "orther":f"{i['genre']} - {j['title']}"
                                }
                    结果.append(单首曲目)
                elif self.分类筛选.value.name==i["genre"] and i["version"]==self.版本筛选.value.version:
                    单首曲目={
                            "icon":None,
                            "title":f"{i['id']} - {i['title']}",
                            "orther":f"{i['genre']} - {self.版本筛选.value.name}"
                        }
                    结果.append(单首曲目)
                elif self.版本筛选.value.version==None and self.分类筛选.value.id==None:
                    for j in 曲目列表["versions"]:
                        if i["version"]==j["version"]:
                            单首曲目={
                                    "icon":None,
                                    "title":f"{i['id']} - {i['title']}",
                                    "orther":f"{i['genre']} - {j['title']}"
                                }
                    结果.append(单首曲目)
        print(结果)
        self.结果容器.add(toga.DetailedList(accessors=("title","orther","icon"),data=结果))
        # self.结果框.value=结果


def main():
    return chusearchsong()
