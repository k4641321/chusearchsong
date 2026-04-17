import toga
from loguru import logger
import json

#添加收藏    
async def 收藏(song,self):
    try:
        with open(self.配置文件路径,"r",encoding="utf-8") as f:
            配置文件=json.load(f)
            logger.info(配置文件)
            收藏目录=配置文件["favorites_path"]
        if 收藏目录!="":
            with open(收藏目录,"r",encoding="utf-8") as f:
                整个收藏文件=json.load(f)
                收藏列表=整个收藏文件["songs"]
            with open(收藏目录,"w",encoding="utf-8") as f:
                收藏列表.append(song)
                整个收藏文件["songs"]=收藏列表
                f.write(json.dumps(整个收藏文件,ensure_ascii=False,indent=2))
        elif 收藏目录=="":
            await 创建收藏目录(self)
            await 收藏(song,self)
            return None
    except Exception as e:
        await self.main_window.diglog(toga.ErrorDialog("错误",e))
async def 取消歌曲收藏(song,self):
    try:
        with open(self.配置文件路径,"r",encoding="utf-8") as f:
            配置文件=json.load(f)
            logger.info(配置文件)
            收藏目录=配置文件["favorites_path"]

        with open(收藏目录,"r",encoding="utf-8") as f:
                整个收藏文件=json.load(f)
                收藏列表=整个收藏文件["songs"]

        for i in 收藏列表:
            if song['id']==i["id"]:
                收藏列表.remove(i)
        with open(收藏目录,"w",encoding="utf-8") as f:
                整个收藏文件["songs"]=收藏列表
                f.write(json.dumps(整个收藏文件,ensure_ascii=False,indent=2))
    except Exception as e:
        await self.main_window.diglog(toga.ErrorDialog("错误",e))
async def 创建收藏目录(self):
    曲目数据路径=self.paths.app / 'resources' / 'list.json'
    with open(曲目数据路径,"r",encoding="utf-8") as f:
        曲目数据=json.load(f)
        版本数据=曲目数据["versions"]
        分类数据=曲目数据["genres"]
    with open(self.配置文件路径,"r",encoding="utf-8") as f:
        配置文件=json.load(f)
        logger.info(配置文件)
    await self.main_window.dialog(toga.InfoDialog("提示", "由于答辩toga外加安卓的限制，文件默认只能保存在 /data/user/0 这样无法访问的路径，请选择其他保存路径"))
    结果= await self.main_window.dialog(toga.SaveFileDialog("选择",suggested_filename="favorite.json"))
    if 结果:
        logger.info(结果)
        with open(结果, "w", encoding="utf-8") as f:
            data=json.dumps({"songs":[],"genres":分类数据,"versions":版本数据},ensure_ascii=False,indent=2)
            f.write(data)

        with open(self.配置文件路径,"w",encoding="utf-8") as f:
            配置文件["favorites_path"]=str(结果)
            f.write(json.dumps(配置文件,ensure_ascii=False,indent=2))
        await self.main_window.dialog(toga.InfoDialog("成功","成功"))
    else:
        await self.main_window.dialog(toga.ErrorDialog("错误","未选择路径"))

