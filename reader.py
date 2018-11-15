# -*- coding:utf-8 -*-
# from bs4 import BeautifulSoup
import re
import  os
from setuptools import setup, find_packages  
import subprocess

try:
    import bs4
except ImportError:        
    scmd="pip install bs4"
    p=subprocess.Popen(scmd,shell=True,stdout=subprocess.PIPE)
    p.wait()
    #os.system('pip install bs4')
   # setup(name = 'bs4',packages = find_packages(),include_package_data = True, platforms = "any",install_requires = [])
    
try:
    import requests
except ImportError:
    scmd="pip install requests"
    p=subprocess.Popen(scmd,shell=True,stdout=subprocess.PIPE)
    p.wait()
    print(' re-dsfdsf')
#scmd="pip install wxpython"
#p=subprocess.Popen(scmd,shell=True,stdout=subprocess.PIPE)
#p.wait() 
import wx


# 设置网址和cookie
web_BookShelf = 'https://m.biquge5200.cc/home/'  # 书架网址
pl_url = 'https://m.biquge5200.cc/u/pl.htm'  # 添加书签网址
cookie_str = r'Hm_lpvt_48b6bcf2e8ec326b3663e20bb30c3754=1539505120; ' \
             r'cax=72; ccu=4ab0bff7785673fab90ed8e9eefa9eb0; cids_AC1=159%2C10; ' \
             r'cac=45; Hm_lvt_48b6bcf2e8ec326b3663e20bb30c3754=1539504283; ' \
             r'cids_AC2=85; cal=31a4cbb6cfcaacfa897f92df891dd3c8; cids_AC6=95192; cv=4; pv=13'
header_str = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
Web_headers = {'User-Agent': header_str, 'Cookie': cookie_str}


# 获取网站内容
def setModel(str_cmd):
    os.system(str_cmd)

def GetWebCon(WebCon_url):
    resp_WebCon = requests.get(WebCon_url, headers=Web_headers)
    Web_encode = resp_WebCon.encoding
    webfile_WebCon = resp_WebCon.content.decode(Web_encode)
    return webfile_WebCon


# 获取书架的书名和编号存入BookoneDict
def GetBookShelfInfo(bookone_webfile):
    id_shuming = []
    m_name = []
    marksherf = []
    updataChapter = []
    id_updataChapter = []
    isupdata = []
    i = 0
    web_bookone = bs4.BeautifulSoup(bookone_webfile, "html.parser")
    for tag in web_bookone.find_all('table', class_='bookone'):
        m_name.append(tag.find('td', class_='case_name').get_text()[3:])
        updataChapter.append(tag.find('td', class_='case_last').get_text()[3:])
        id_n = tag.find_all('a')[0]['href'][6:]
        id_Chapter = tag.find_all('a')[1]['href'][9:]
        id_shuming.append(id_n[:len(id_n) - 1])
        id_updataChapter.append(id_Chapter[id_Chapter.index("-") + 1:len(id_Chapter) - 1])
        herf_marks = tag.find('td', class_='case_shuqian').find_all('a')[0]['href'][9:]
        marksherf.append(herf_marks[herf_marks.index("-") + 1:len(herf_marks) - 1])
        if tag.find('td', class_='case_shuqian').get_text() == "有更新":
            isupdata.append(1)
        else:
            isupdata.append(0)
        i = i + 1
    BookoneDict = dict(zip(m_name, id_shuming))
    updataChapterDict = dict(zip(updataChapter, id_updataChapter))
    BookshelfList = [BookoneDict, updataChapterDict, marksherf, isupdata]
    return BookshelfList


# 获取目录和链接的字典MuluDict{章节名:ID}
def GetMulu(BookDict):
    MuLu_name = []
    id_MuLu = []
    if isinstance(BookDict, str):
        Mulu_url = "https://m.biquge5200.cc/wapbook-" + BookDict
    else:
        Mulu_url = "https://m.biquge5200.cc/wapbook-" + BookDict[1]
    Mulu_con = GetWebCon(Mulu_url)
    web_MuLu = bs4.BeautifulSoup(Mulu_con, "html.parser")
    for tag in web_MuLu.find_all('ul', class_='chapter'):
        for tag2 in tag.find_all('a'):
            MuLu_name.append(tag2.contents[0])
            temp = tag2['href'][9:]
            id_MuLu.append(temp[temp.index("-") + 1:len(temp) - 1])
    MuluDict = dict(zip(MuLu_name, id_MuLu))
    return MuluDict


def GetMulu2(BookDict):
    MuLu_name = []
    id_MuLu = []
    if isinstance(BookDict, str):
        Mulu_url = "https://m.biquge5200.cc/wapbook-" + BookDict
    else:
        Mulu_url = "https://m.biquge5200.cc/wapbook-" + BookDict[1]
    Mulu_con = GetWebCon(Mulu_url)
    web_MuLu = bs4.BeautifulSoup(Mulu_con, "html.parser")
    tag = web_MuLu.find_all('div', class_='page')[0]
    pageNowStr = tag.find_all('a')[0].get('href')
    pageNow = int(pageNowStr[pageNowStr.find("_") + 1:len(pageNowStr) - 3]) - 1
    pageTotalStr = tag.find_all('a')[1].get('href')
    pageTotal = int(pageTotalStr[pageTotalStr.find("_") + 1:len(pageTotalStr) - 3])
    for i in range(1, pageTotal + 1):
        Mulu_url2 = Mulu_url + "_" + str(i) + "_1"
        Mulu_con = GetWebCon(Mulu_url2)
        web_MuLu = bs4.BeautifulSoup(Mulu_con, "html.parser")
        tag = web_MuLu.find('ul', class_='chapter')
        for tag2 in tag.find_all('a'):
            MuLu_name.append(tag2.contents[0])
            temp = tag2['href'][9:]
            id_MuLu.append(temp[temp.index("-") + 1:len(temp) - 1])
    MuluDict = dict(zip(MuLu_name, id_MuLu))
    return MuluDict


# 提取更新的小说内容存入context
def GetConTXT(url_ConTXT):
    con = requests.get(url_ConTXT).text
    s_con_txt = re.search(r'<div\Dclass="text">', con).end()
    e_con_txt = re.search(r'</div>', con[s_con_txt:]).start()
    # 把段落标记替换
    cc1 = con[s_con_txt:e_con_txt + s_con_txt].replace("<p>", "")
    cc = cc1.replace("</p>", "\n")
    return cc


###########################################################################

###########################################################################

import wx.xrc


###########################################################################
## Class BookInfo
###########################################################################

class BookInfo(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(-1, -1),
                          style=wx.TAB_TRAVERSAL)
        # 赋值
        self.parent12 = self.GetParent()
        self.nameBook = list(parent.nowBook.keys())[0]
        self.idBook = list(parent.nowBook.values())[0]
        webInfo = "https://m.biquge5200.cc/info-" + self.idBook
        web_Info = bs4.BeautifulSoup(GetWebCon(webInfo), "html.parser")
        tagAuthor = web_Info.find('div', class_='block_txt2').find_all('a')[1]
        self.author = tagAuthor.contents[0]
        self.Brief = web_Info.find('div', class_='intro_info').get_text()
        self.Chapters = list(self.parent12.nowChapters.keys())
        self.idChapters = list(self.parent12.nowChapters.values())

        # 布局
        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        self.nowBookName = wx.StaticText(self, wx.ID_ANY, self.nameBook, wx.DefaultPosition, wx.DefaultSize, 0)
        # self.nowBookName.Wrap(-1)
        self.nowBookName.SetFont(wx.Font(20, 70, 90, 92, False, wx.EmptyString))
        self.nowBookAuthor = wx.StaticText(self, wx.ID_ANY, "作者：" + self.author, wx.DefaultPosition, wx.DefaultSize, 0)
        # self.nowBookAuthor.Wrap(-1)
        self.nowBookBrief = wx.StaticText(self, wx.ID_ANY, "    小说简介：" + self.Brief, wx.DefaultPosition, size=(300, -1),
                                          style=wx.TE_MULTILINE)
        # self.nowBookBrief.Wrap(-1)
        self.nowBookChapters = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, size=(240, 700),
                                           style=wx.LC_VRULES | wx.LC_REPORT | wx.LC_HRULES | wx.NO_BORDER | wx.LC_NO_HEADER | wx.LC_AUTOARRANGE)
        self.nowBookChapters.InsertColumn(0, "章节目录")
        self.nowBookChapters.SetColumnWidth(0, 230)

        gSizer1 = wx.GridSizer(0, 2, 0, 0)
        self.BookShelf = wx.Button(self, wx.ID_ANY, u"书架", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer1.Add(self.BookShelf, 0, wx.ALIGN_CENTER | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        self.moreChapters = wx.Button(self, wx.ID_ANY, u"全部目录", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer1.Add(self.moreChapters, 0, wx.ALIGN_CENTER | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        for Chapter in self.Chapters:
            self.nowBookChapters.InsertItem(self.nowBookChapters.GetItemCount(), Chapter)
        bSizer1.AddMany([(self.nowBookName, 0, wx.ALIGN_CENTER | wx.ALL, 5),
                         (self.nowBookAuthor, 0, wx.ALIGN_CENTER | wx.ALL, 5),
                         (gSizer1, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.SHAPED, 5),
                         (self.nowBookBrief, 0, wx.ALIGN_CENTER | wx.ALL, 5),
                         (self.nowBookChapters, 0, wx.ALIGN_CENTER | wx.ALL, 5)])
        # self.SetSizerAndFit(bSizer1)
        self.SetSizer(bSizer1)

        # 文件操作

        # Connect Events
        self.nowBookChapters.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OpenAtricle2)
        # self.moreChapters.Bind(wx.EVT_BUTTON, self.GetChapters(parent=parent))
        self.BookShelf.Bind(wx.EVT_BUTTON, parent.GoHome)
        self.Layout()

    def __del__(self):
        pass

    def OpenAtricle2(self, event):
        selectNum = event.GetIndex()
        chapterName = self.nowBookChapters.GetItem(selectNum).GetText()
        self.parent12.nowChapter = {chapterName: str(self.idChapters[selectNum])}
        self.parent12.panel.Destroy()
        self.parent12.panel = ArticlePanel(self.parent12)
        self.parent12.sizer.Add(self.parent12.panel, 1, wx.EXPAND | wx.ALL, 1)
        self.parent12.SetSizerAndFit(self.parent12.sizer)
        self.parent12.panel.Hide()
        self.parent12.OpenAtricle(self.parent12)

    def GetChapters(self, parent):
        dictChapters = GetMulu2(list(parent.nowBook.values())[0])
        Chapters = list(dictChapters.keys())
        self.nowBookChapters.DeleteAllItems()
        for Chapter in Chapters:
            self.nowBookChapters.InsertItem(self.nowBookChapters.GetItemCount(), Chapter)


###########################################################################
## Class BookShelfPanel
###########################################################################
class BookShelfPanel(wx.Panel):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(-1, -1),
                          style=wx.TAB_TRAVERSAL)

        # 定一个网格布局,两行一列
        gbSizer1 = wx.GridBagSizer(0, 0)
        gbSizer1.SetFlexibleDirection(wx.BOTH)
        gbSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # 生成一个列表
        self.booknamelist = wx.ListCtrl(self, -1, size=(-1, 600),
                                        style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)  # | wx.LC_SINGLE_SEL
        # 列表有散列，分别是书本ID,书名，添加日期
        self.booknamelist.InsertColumn(0, "书名")
        self.chapterlist = wx.ListCtrl(self, -1, size=(-1, 600), name="最新章节",
                                       style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)  # | wx.LC_SINGLE_SEL
        self.chapterlist.InsertColumn(0, "最新章节")
        self.isupdatalist = wx.ListCtrl(self, -1, size=(-1, 600),
                                        style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)  # | wx.LC_SINGLE_SEL
        self.isupdatalist.InsertColumn(0, "是否更新")

        # 设置各列的宽度
        self.booknamelist.SetColumnWidth(0, 100)  # 设置每一列的宽度
        self.chapterlist.SetColumnWidth(0, 230)
        self.isupdatalist.SetColumnWidth(0, 92)
        gbSizer1.AddMany([(self.booknamelist, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5),
                          (self.chapterlist, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5),
                          (self.isupdatalist, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL, 5)
                          ])
        self.SetSizer(gbSizer1)

        self.parent123 = self.GetParent()
        self.BookShelfInfo = GetBookShelfInfo(GetWebCon(web_BookShelf))
        bookin = []
        for i in range(len(self.BookShelfInfo[0])):
            bookin.append(
                [list(self.BookShelfInfo[0].keys())[i], list(self.BookShelfInfo[1].keys())[i], self.BookShelfInfo[2][i],
                 self.BookShelfInfo[3][i]])

        for i in range(len(self.BookShelfInfo[0])):
            self.booknamelist.InsertItem(self.booknamelist.GetItemCount(), list(self.BookShelfInfo[0].keys())[i])
            self.chapterlist.InsertItem(self.chapterlist.GetItemCount(), list(self.BookShelfInfo[1].keys())[i])
            self.isupdatalist.InsertItem(self.isupdatalist.GetItemCount(), str(self.BookShelfInfo[3][i]))
        self.Layout()
        # 文件操作
        fo = open("Marks.txt", "w")
        for numData in range(len(self.BookShelfInfo[0])):
            fo.write(bookin[numData][0] + "-" + bookin[numData][1] + "-" + bookin[numData][2] + "-" + str(
                bookin[numData][3]) + "\n")
        fo.close()
        # 把章节存到文件中
        for idBook in list(self.BookShelfInfo[0].values()):
            pathBook="./books/"+str(idBook)+".txt"
            try:
                with open(pathBook,"r") as fBook:
                    lineChapters = fBook.readlines()
                    try:
                        arry_chapters = lineChapters[len(lineChapters)-1].split("-")
                    except:
                        arry_chapters=['erro','404']
                    updataChapter=list(self.BookShelfInfo[1].keys())[list(self.BookShelfInfo[0].values()).index(str(idBook))]
                    if arry_chapters[0]!=updataChapter:
                        fBook = open(pathBook, "a+")
                        fBook.write(updataChapter + "-" + self.BookShelfInfo[1][updataChapter] + "\n")
            except OSError:
                with open(pathBook, "w") as fBook:
                    dictChapters = GetMulu2(str(idBook))
                    Chapters = list(dictChapters.keys())
                    idchapter = list(dictChapters.values())
                    for numChapter in range(len(Chapters)):
                        fBook.write(Chapters[len(Chapters)-numChapter-1]+"-"+idchapter[len(Chapters)-numChapter-1]+"\n")

        # Connect Events
        self.booknamelist.Bind(wx.EVT_LIST_ITEM_SELECTED, self.GoBookInfo)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OpenAtricle1, self.chapterlist)
        self.chapterlist.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OpenAtricle1)

    def __del__(self):
        pass

    def OpenAtricle1(self, event):
        selectNum = event.GetIndex()
        chapterName = self.chapterlist.GetItem(selectNum).GetText()
        BookName = self.booknamelist.GetItem(selectNum).GetText()
        self.parent123.nowBook = {BookName: str(self.BookShelfInfo[0][BookName])}
        self.parent123.nowChapter = {chapterName: str(self.BookShelfInfo[1][chapterName])}
        self.parent123.GetChapter(self.parent123, str(self.BookShelfInfo[0][BookName]))
        self.parent123.panel.Destroy()
        self.parent123.panel = ArticlePanel(self.parent123)
        self.parent123.sizer.Add(self.parent123.panel, 1, wx.EXPAND | wx.ALL, 1)
        self.parent123.SetSizerAndFit(self.parent123.sizer)
        self.parent123.panel.Hide()
        self.parent123.OpenAtricle(self.parent123)

    def GoBookInfo(self, event):
        selectNum = event.GetIndex()
        BookName = self.booknamelist.GetItem(selectNum).GetText()
        self.parent123.nowBook = {BookName: str(self.BookShelfInfo[0][BookName])}
        self.parent123.GetChapter(self.parent123, idBook=str(self.BookShelfInfo[0][BookName]))
        self.parent123.panel_three.Destroy()
        self.parent123.panel_three = BookInfo(self.parent123)
        self.parent123.sizer.Add(self.parent123.panel_three, 1, wx.EXPAND | wx.ALL, 1)
        self.parent123.SetSizerAndFit(self.parent123.sizer)
        self.parent123.GoBookInfo(self.parent123)
        self.parent123.Layout()


###########################################################################
## Class ArticlePanel
###########################################################################
class ArticlePanel(wx.Panel):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """用来展示书架和更新章节"""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(-1, -1),
                          style=wx.TAB_TRAVERSAL)
        # 建立变量
        self.parent1 = self.GetParent()
        self.bookInfo = wx.StaticText(self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bookInfo.Wrap(-1)
        self.button_BookShelf = wx.Button(self, wx.ID_ANY, u"书架", wx.DefaultPosition, wx.DefaultSize, 0)
        self.button_PreChapter = wx.Button(self, wx.ID_ANY, u"上一章", wx.DefaultPosition, wx.DefaultSize, 0)
        self.button_Chapters = wx.Button(self, wx.ID_ANY, u"目录", wx.DefaultPosition, wx.DefaultSize, 0)
        self.button_NextChapter = wx.Button(self, wx.ID_ANY, u"下一章", wx.DefaultPosition, wx.DefaultSize, 0)

        self.button_BookShelf2 = wx.Button(self, wx.ID_ANY, u"书架", wx.DefaultPosition, wx.DefaultSize, 0)
        self.button_PreChapter2 = wx.Button(self, wx.ID_ANY, u"上一章", wx.DefaultPosition, wx.DefaultSize, 0)
        self.button_Chapters2 = wx.Button(self, wx.ID_ANY, u"目录", wx.DefaultPosition, wx.DefaultSize, 0)
        self.button_NextChapter2 = wx.Button(self, wx.ID_ANY, u"下一章", wx.DefaultPosition, wx.DefaultSize, 0)

        self.ContentTxt = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(-1, 700),
                                      style=wx.TE_MULTILINE)
        # 布局
        bSizer = wx.BoxSizer(wx.VERTICAL)
        bSizer.Add(self.bookInfo, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        gSizer1 = wx.GridSizer(0, 4, 0, 0)
        gSizer1.AddMany([
            (self.button_BookShelf, 0, wx.ALL, 5), (self.button_PreChapter, 0, wx.ALL, 5),
            (self.button_Chapters, 0, wx.ALL, 5), (self.button_NextChapter, 0, wx.ALL, 5)]
        )
        bSizer.Add(gSizer1, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        bSizer.Add(self.ContentTxt, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)
        gSizer2 = wx.GridSizer(0, 4, 0, 0)
        gSizer2.AddMany([
            (self.button_BookShelf2, 0, wx.ALL, 5), (self.button_PreChapter2, 0, wx.ALL, 5),
            (self.button_Chapters2, 0, wx.ALL, 5), (self.button_NextChapter2, 0, wx.ALL, 5)]
        )
        bSizer.Add(gSizer2, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.SetSizerAndFit(bSizer)
        self.SetSizer(bSizer)

        # 赋值
        font = wx.Font(18, wx.FONTFAMILY_ROMAN, wx.NORMAL, wx.NORMAL)
        self.bookInfoTxt = list(parent.nowBook.keys())[0] + "  " + list(parent.nowChapter.keys())[0]
        ulop = "https://m.biquge5200.cc/wapbook-" + list(parent.nowBook.values())[0] + "-" + \
               list(parent.nowChapter.values())[0]
        self.nowContxt = GetConTXT(ulop)
        self.bookInfo.SetLabel(self.bookInfoTxt)
        self.bookInfo.SetFont(font)
        self.ContentTxt.SetValue(self.nowContxt)
        self.ContentTxt.SetFont(font)
        self.ContentTxt.SetEditable(False)
        self.Layout()

        # Connect Events
        self.bookInfo.Bind(wx.EVT_LEFT_DCLICK, self.GoBookInfo)
        self.button_BookShelf.Bind(wx.EVT_BUTTON, parent.GoHome)
        self.button_PreChapter.Bind(wx.EVT_BUTTON, self.GetPreChapter)
        self.button_Chapters.Bind(wx.EVT_BUTTON, self.GoBookInfo)
        self.button_NextChapter.Bind(wx.EVT_BUTTON, self.GetNextChapter)
        self.button_BookShelf2.Bind(wx.EVT_BUTTON, parent.GoHome)
        self.button_PreChapter2.Bind(wx.EVT_BUTTON, self.GetPreChapter)
        self.button_Chapters2.Bind(wx.EVT_BUTTON, self.GoBookInfo)
        self.button_NextChapter2.Bind(wx.EVT_BUTTON, self.GetNextChapter)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class

    def GetPreChapter(self, event):
        nowIndex = list(self.parent1.nowChapters.keys()).index(list(self.parent1.nowChapter.keys())[0])
        if nowIndex > 0:
            self.parent1.nowChapter.clear()
            self.parent1.nowChapter[list(self.parent1.nowChapters.keys())[nowIndex - 1]] = \
                list(self.parent1.nowChapters.values())[nowIndex - 1]
            self.bookInfoTxt = list(self.parent1.nowBook.keys())[0] + "  " + list(self.parent1.nowChapter.keys())[0]
            self.bookInfo.SetLabel(self.bookInfoTxt)
            ulop = "https://m.biquge5200.cc/wapbook-" + list(self.parent1.nowBook.values())[0] + "-" + \
                   list(self.parent1.nowChapters.values())[nowIndex - 1]
            nowContxt = GetConTXT(ulop)
            self.ContentTxt.Clear()
            self.ContentTxt.SetValue(nowContxt)
        else:
            self.bookInfoTxt = ""

    def GetNextChapter(self, event):
        nowIndex = list(self.parent1.nowChapters.keys()).index(list(self.parent1.nowChapter.keys())[0])
        tot = len(list(self.parent1.nowChapters.keys()))
        if nowIndex < tot:
            self.parent1.nowChapter.clear()
            self.parent1.nowChapter[list(self.parent1.nowChapters.keys())[nowIndex + 1]] = \
                list(self.parent1.nowChapters.values())[nowIndex + 1]
            self.bookInfoTxt = list(self.parent1.nowBook.keys())[0] + "  " + list(self.parent1.nowChapter.keys())[0]
            self.bookInfo.SetLabel(self.bookInfoTxt)
            ulop = "https://m.biquge5200.cc/wapbook-" + list(self.parent1.nowBook.values())[0] + "-" + \
                   list(self.parent1.nowChapters.values())[nowIndex + 1]
            nowContxt = GetConTXT(ulop)
            self.ContentTxt.Clear()
            self.ContentTxt.SetValue(nowContxt)

    def GoBookInfo(self, event):
        self.parent1.panel_three.Destroy()
        self.parent1.panel_three = BookInfo(self.parent1)
        self.parent1.sizer.Add(self.parent1.panel_three, 1, wx.EXPAND | wx.ALL, 1)
        self.parent1.SetSizerAndFit(self.parent1.sizer)
        self.parent1.GoBookInfo(self.parent1)
        self.parent1.Layout()


###########################################################################
## Class fame
###########################################################################
class fameOne(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, id=wx.ID_ANY, title=u"小说", pos=wx.DefaultPosition,
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        # 获取书架信息
        self.nowBook = {'修真聊天群': '4645'}
        self.nowChapter = {'三更完毕，摆好姿势求月票': '159735911'}
        self.nowChapters = {'第2302章 您所呼叫的白前辈已关机（第3更，月票）': '159769271',
                            '第2301章 白two前辈助我（第2更，月票）': '159764857',
                            '第2300章 分不清现实和幻想（第1更，月票）': '159760445',
                            '三更完毕，摆好姿势求月票': '159735911',
                            '第2299章 通往现世的大门（第3更，求月票）': '159735894',
                            '第2298章 千丝万缕的连系（第2更，求月票）': '159731089',
                            '第2297章 乖孩子（第1更，求月票）': '159725656'}
        self.panel = ArticlePanel(self)
        self.panel_two = BookShelfPanel(self)
        self.panel_three = BookInfo(self)
        self.panel.Hide()
        self.panel_three.Hide()

        # 布局
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel, 1, wx.EXPAND | wx.ALL, 1)
        self.sizer.Add(self.panel_two, 1, wx.EXPAND | wx.ALL, 1)
        self.sizer.Add(self.panel_three, 1, wx.EXPAND | wx.ALL, 1)
        self.SetSizerAndFit(self.sizer)

        self.m_menubar1 = wx.MenuBar(0)
        self.BookShelf = wx.Menu()
        self.OpenBookShelf = wx.MenuItem(self.BookShelf, wx.ID_ANY, u"打开书架", wx.EmptyString, wx.ITEM_NORMAL)
        self.BookShelf.Append(self.OpenBookShelf)

        self.ArticleSearch = wx.MenuItem(self.BookShelf, wx.ID_ANY, u"搜索", wx.EmptyString, wx.ITEM_NORMAL)
        self.BookShelf.Append(self.ArticleSearch)

        self.m_menubar1.Append(self.BookShelf, u"书架")

        self.Updata = wx.Menu()
        self.IfUpdata = wx.MenuItem(self.Updata, wx.ID_ANY, u"检查更新", wx.EmptyString, wx.ITEM_NORMAL)
        self.Updata.Append(self.IfUpdata)

        self.AddMark = wx.MenuItem(self.Updata, wx.ID_ANY, u"添加书签", wx.EmptyString, wx.ITEM_NORMAL)
        self.Updata.Append(self.AddMark)
        self.m_menubar1.Append(self.Updata, u"更新")
        self.SetMenuBar(self.m_menubar1)

        self.Layout()

        # Connect Events
        self.Bind(wx.EVT_MENU, self.GoHome, id=self.OpenBookShelf.GetId())
        self.Bind(wx.EVT_MENU, self.articlesearch, id=self.ArticleSearch.GetId())
        self.Bind(wx.EVT_MENU, self.GetUpadata, id=self.IfUpdata.GetId())
        self.Bind(wx.EVT_MENU, self.toAddMark, id=self.AddMark.GetId())

    # Virtual event handlers, overide them in your derived class

    def GetChapter(self, event, idBook):
        # 通过文件读取章节
        pathBook = "./books/" + str(idBook) + ".txt"
        fChapter = open(pathBook, "r")
        lineChapters = fChapter.readlines()
        self.nowChapters.clear()
        for dataChapter in lineChapters:
            arry_chapters = dataChapter.split("-")
            self.nowChapters[arry_chapters[0]] = str(arry_chapters[1])

    def OpenAtricle(self, event):
        if self.panel_two.IsShown():
            self.SetTitle("阅读")
            self.panel_two.Hide()
            self.panel_three.Hide()
            self.panel.Show()
        else:
            if self.panel_three.IsShown():
                self.SetTitle("阅读")
                self.panel_two.Hide()
                self.panel_three.Hide()
                self.panel.Show()
        self.Layout()

    def GoHome(self, event):
        if self.panel.IsShown():
            self.SetTitle("书架")
            self.panel.Hide()
            self.panel_three.Hide()
            self.panel_two.Show()
        else:
            if self.panel_three.IsShown():
                self.SetTitle("书架")
                self.panel.Hide()
                self.panel_three.Hide()
                self.panel_two.Show()
        self.Layout()

    def articlesearch(self, event):
        # self.panel.button1.SetLabel("articlesearch")
        print("articlesearch Showing")

    def GetUpadata(self, event):
        self.panel_two.Destroy()
        self.panel_two = BookShelfPanel(self)
        self.sizer.Add(self.panel_two, 1, wx.EXPAND | wx.ALL, 1)
        self.SetSizerAndFit(self.sizer)
        self.GoHome
        self.Layout()

    def GoBookInfo(self, event):
        if self.panel.IsShown():
            self.panel.Hide()
            self.panel_two.Hide()
            self.panel_three.Show()
        else:
            if self.panel_two.IsShown():
                self.panel_two.Hide()
                self.panel.Hide()
                self.panel_three.Show()
        self.Layout()

    def toAddMark(self, event):
        sid = list(self.nowBook.values())[0] + "," + str(int(list(self.nowChapter.values())[0]))
        pl_data_post = {"id": sid}
        r = requests.post(pl_url, data=pl_data_post, headers=Web_headers)
        ttt = r.text
        if ttt == '{"flag":"success","data":""}':
            print("已添加书签")
            # self.panel.button.SetLabel("已添加书签")
        event.Skip()


if __name__ == '__main__':
    app = wx.App(False)
    frame = fameOne()
    frame.Show()
    app.MainLoop()
