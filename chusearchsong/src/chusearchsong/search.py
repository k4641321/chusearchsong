import toga
import json
from toga.style.pack import COLUMN, ROW,PACK,NONE,HIDDEN, VISIBLE
from toga.style import Pack
import asyncio
#from chusearchsong.app import 曲目详情

def 返回歌曲json(id,title,artist,genre,bpm,version,zhversion,difficulties):
    data = {
        "id": id,
        "title": title,
        "artist":artist,
        "genre": genre,
        "bpm": bpm,
        "version": version,
        "zhversion":zhversion,
        "difficulties":difficulties,
        "isappend":False,
    }
    return data
async def 曲目搜索(曲目列表路径:str,分类筛选:str,版本筛选:str,版本筛选中文名,难度筛选前:float or int ,难度筛选后:float or int ,搜索框:str,曲目详情):
    #资源目录 = paths.app / "resources"
    #曲目列表路径 = Path(资源目录),"resources\list.json"
    with open(曲目列表路径, "r", encoding="UTF-8") as f:
        曲目列表 = json.load(f)
        f.close()
    结果 = []
    if 分类筛选=="分类":
        分类筛选=None
    #print(版本筛选,'error')
    # if 版本筛选==None or 分类筛选==None or 曲目列表路径==None:
    #     曲目盒子 = toga.Box(style=Pack(direction=COLUMN))
    #     曲目盒子.add(toga.Label(text=f"错误", style=Pack(flex=1)))
    #     return 曲目盒子
    for i in 曲目列表["songs"]:
        if 搜索框.lower() in i["title"].lower():
            if 分类筛选 == None and i["version"] == 版本筛选:
                单首曲目 = 返回歌曲json(i["id"],i["title"],i["artist"],i["genre"],i["bpm"],i["version"],版本筛选中文名,i["difficulties"])
                结果.append(单首曲目)
            elif 分类筛选 == i["genre"] and 版本筛选 == None:
                for j in 曲目列表["versions"]:
                    if i["version"] == j["version"]:
                        单首曲目 = 返回歌曲json(i["id"],i["title"],i["artist"],i["genre"],i["bpm"],i["version"],j["title"],i["difficulties"])
                结果.append(单首曲目)
            elif 分类筛选 == i["genre"] and i["version"] == 版本筛选:
                单首曲目 = 返回歌曲json(i["id"],i["title"],i["artist"],i["genre"],i["bpm"],i["version"],版本筛选中文名,i["difficulties"])
                结果.append(单首曲目)
            elif 版本筛选 == None and 分类筛选 == None:
                for j in 曲目列表["versions"]:
                    if i["version"] == j["version"]:
                        单首曲目 = 返回歌曲json(i["id"],i["title"],i["artist"],i["genre"],i["bpm"],i["version"],j["title"],i["difficulties"])
                结果.append(单首曲目)
    # print(结果)
    结果2=[]
    for i in 结果:
        if not i["isappend"]:
            continue
        for j in i["difficulties"]:
            if 难度筛选前==0 or 难度筛选后==0:
                break
            elif 难度筛选前 <= j["level_value"] <= 难度筛选后:
                结果2.append(i)
        i["isappend"]==True
    # print(结果2)
    曲目盒子 = toga.Box(style=Pack(direction=COLUMN))
    if not 结果2==[]:
        结果=结果2
    for i in 结果:
        单曲盒子=toga.Box(id=f"box{i['id']}",style=Pack(direction=ROW))
        单曲盒子.add(toga.Label(id=i['id'],text=f"{i['id']}  -  {i['title']}    {i['genre']}  -  {i['zhversion']}", style=Pack(flex=1)))
        单曲盒子.add(toga.Button(id=f"button{i['id']}",text="详情",style=Pack(flex=1,width=75),on_press=lambda widget,song=i:asyncio.create_task(曲目详情(widget, song))))
        曲目盒子.add(单曲盒子)
    return 曲目盒子
