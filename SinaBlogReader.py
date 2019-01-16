#coding=UTF-8
# XingHe Studio Sina Blog Reader
# Create by Stream.Wang 2019-01-15
# Modify by Stream.Wang 2019-01-16
import sys
from __builtin__ import str
from _ast import Str
reload(sys);
sys.setdefaultencoding('utf8');

import os,io;
import urllib2,json;
from pyquery import PyQuery
#基础函数
def sys_windowstf():
    # SYS 返回系统是否是windows
    import platform
    if str(platform.system()).lower()=='Windows'.lower():
        return True
    else:
        return False
def sys_pathstr():
    if sys_windowstf()==True :
        return "\\"
    else:
        return r"/"
def fil_changefileext(filename,extname=''):
    # FIL ChangeFileExt 改变文件扩展名
    # filename    输入的文件路径名
    # extname=''  要更改分扩展名，如 .txt
    try:
        if extname[0]!='.':
            extname='.'+extname
    except:
        extname=''
    if os.path.splitext(filename)[1]=='':
        uouttxt=filename+'.'+extname
    elif os.path.splitext(filename)[1]=='.':
        uouttxt=filename+extname
    else:
        uouttxt=filename[:0-len(os.path.splitext(filename)[1])]+extname
    return uouttxt    
#===============================================================
#程序开始    
XHAppName='XingHe Studio Sina Blog Reader';
XHAppVer='Ver 0.99B';
XHAppPath=os.path.dirname(sys.argv[0])+sys_pathstr(); #系统所在路径;
XHAppPathName=sys.argv[0]; #系统所在路径名;
XHAppCnf=fil_changefileext(sys.argv[0],'.cnf'); #配置文件
print(XHAppName+' '+XHAppVer);
print(' App Path: '+XHAppPath);
print(' App Name: '+XHAppPathName);
print(' App Config: '+XHAppCnf);
#配置文件相关
XHAppCnfData={'DataPath':XHAppPath+'Data'+sys_pathstr(),'SinaBlogID':'1018603404'}; #初始化配置文件信息
#写入配置文件
if not os.path.exists(XHAppCnf):
    with io.open(XHAppCnf,'wb') as json_file:
        json.dump(XHAppCnfData,json_file,ensure_ascii=False);
#读取配置文件
XHAppCnfData={}; #配置文件信息
with io.open(XHAppCnf,'rb') as json_file:
    XHAppCnfData=json.load(json_file);
#数据存储路径
XHAppDataPath=XHAppCnfData['DataPath'];
print(' App DataPath: '+XHAppDataPath);
if not os.path.exists(XHAppPath+'Data') : os.mkdir(XHAppPath+'Data');
OutHtmlList='';
#新浪ID
SinaBlogID=XHAppCnfData['SinaBlogID'];
if SinaBlogID.strip()=='': SinaBlogID='1018603404';
if not os.path.exists(XHAppPath+'Data'+sys_pathstr()+SinaBlogID) : os.mkdir(XHAppPath+'Data'+sys_pathstr()+SinaBlogID);
XHAppDataPath=XHAppPath+'Data'+sys_pathstr()+SinaBlogID+sys_pathstr();
print('  >> Sina Blog ID: '+SinaBlogID);
SinaBlogUrl='http://blog.sina.com.cn/s/articlelist_'+SinaBlogID+'_0_1.html';
print('  >> Read Url: '+SinaBlogUrl);
BlogML=urllib2.urlopen(SinaBlogUrl).read();#读取博客目录
BlogMLHtml=PyQuery(BlogML)('div.menuList').html();
BlogMLHtml=PyQuery(BlogMLHtml)('a');
BlogMLList={};
for li in BlogMLHtml.items(): 
    #忽略博文收藏目录
    if li.text()!=u'\u535a\u6587\u6536\u85cf' : BlogMLList[li.text()]=li.attr('href');
BlogMLList=sorted(BlogMLList.items(), key=lambda d: d[0]);
BlogLB=BlogML;
#分析页数
BlogLsHtml=PyQuery(BlogLB)('ul.SG_pages').html();
if BlogLsHtml.strip()!='':
    BlogPgHtml=int(PyQuery(BlogLsHtml)('span').text().replace(u'共','').replace(u'页',''));
else:
    BlogPgHtml=1;
BlogPgHtmlZ=BlogPgHtml;
#分析记录数
BlogLsHtml=PyQuery(BlogLB)('div.SG_colW73').html();
BlogLsHtml=PyQuery(BlogLsHtml)('div.SG_connHead').html();
BlogLsHtml=PyQuery(BlogLsHtml)('span.title').html();
BlogCtHtml=int(PyQuery(BlogLsHtml)('em').text().replace(u'(','').replace(u')',''));
BlogCtHtmlZ=BlogCtHtml;
BlogMLList2={};
BlogCounts=0;
print('  >>  类别数: '+str(len(BlogMLList))+'， 总页数：'+str(BlogPgHtmlZ)+'， 总博客数：'+str(BlogCtHtmlZ) );
print('  >>' );
print('  >> 开始缓存所有分类页面...' );
for key in range(len(BlogMLList)):
    BlogLBName=BlogMLList[key][0];#分类名称
    BlogLBUrl=BlogMLList[key][1];#分类网页地址
    print('  >> Read Url: '+BlogLBUrl);
    BlogLB=urllib2.urlopen(BlogLBUrl).read();#读取博客目录
    #本地保存
    BlogLBUrlFileName=os.path.basename(BlogLBUrl.strip());
    BlogLBUrlJsonName=fil_changefileext(BlogLBUrlFileName,'.json')
    fil_changefileext
    fileHandle = open ( XHAppDataPath+BlogLBUrlFileName, 'w' );
    fileHandle.write(BlogLB);
    fileHandle.close();
    OutHtmlList=OutHtmlList+XHAppDataPath+BlogLBUrlFileName+'\n';
    #print(BlogLB); #调试输出
    #分析页数
    BlogLsHtml=PyQuery(BlogLB)('ul.SG_pages').html();
    if BlogLsHtml.strip()!='':
        BlogPgHtml=int(PyQuery(BlogLsHtml)('span').text().replace(u'共','').replace(u'页',''));
    else:
        BlogPgHtml=1;
    #分析记录数
    BlogLsHtml=PyQuery(BlogLB)('div.SG_colW73').html();
    BlogLsHtml=PyQuery(BlogLsHtml)('div.SG_connHead').html();
    BlogLsHtml=PyQuery(BlogLsHtml)('span.title').html();
    BlogCtHtml=int(PyQuery(BlogLsHtml)('em').text().replace(u'(','').replace(u')',''));
    strkey=str(key+1).zfill(5); 
    print('  >>  '+strkey+' '+BlogLBName+' 共'+str(BlogPgHtml)+'页 / 共记录数'+str(BlogCtHtml)+'条');
    BlogMLList2['ArticleList_'+strkey+'_01_Name']=BlogLBName;
    BlogMLList2['ArticleList_'+strkey+'_02_Url']=BlogLBUrl;
    BlogMLList2['ArticleList_'+strkey+'_03_Pages']=BlogPgHtml;
    BlogMLList2['ArticleList_'+strkey+'_04_Counts']=BlogCtHtml;
    BlogMLList2['ArticleList_'+strkey+'_05_Memo']=strkey+' '+BlogLBName+' 共'+str(BlogPgHtml)+'页 / 共记录数'+str(BlogCtHtml)+'条';
    BlogCounts=BlogCounts+BlogCtHtml;
    #页数 BlogPgHtml
    #记录数 BlogCtHtml
    #开始读取该大类明细博客信息
BlogMLList2=sorted(BlogMLList2.items(), key=lambda d: d[0]);
BlogMLList2_Json=json.dumps(BlogMLList2,encoding="UTF-8", ensure_ascii=False);
with io.open(XHAppDataPath+SinaBlogID+'_ArticleList.json','wb') as json_file:
    json.dump(BlogMLList2_Json,json_file,ensure_ascii=False);
print('  >> 其它博客数：'+str(BlogCtHtmlZ-BlogCounts)+'条');
OutHtmlList=OutHtmlList+'\n';
print('  >>');
print('  >> 开始下载博客...');

#读取博客列表
BlogCtHtmlZ2=0
BlogMLHtml=PyQuery(BlogML)('div.articleList').html();
BlogMLHtml=PyQuery(BlogMLHtml)('a');
BlogMLList={};
for li in BlogMLHtml.items(): 
    if li.attr('href').strip()!='' and 'news.sina.com.cn' not in li.attr('href').strip() : BlogMLList[len(BlogMLList)+1]=li.attr('href');
print('  >> Read Url: '+SinaBlogUrl);
print('  >> 第1页/共'+str(BlogPgHtmlZ)+'页 记录数：'+str(len(BlogMLList)));
BlogCtHtmlZ2=BlogCtHtmlZ2+len(BlogMLHtml);
#本地保存
BlogLBUrlFileName=os.path.basename(SinaBlogUrl.strip())
fileHandle = open (XHAppDataPath+BlogLBUrlFileName, 'w' );
fileHandle.write(BlogML);
fileHandle.close();
OutHtmlList=OutHtmlList+XHAppDataPath+BlogLBUrlFileName+'\n';
for key in range(BlogPgHtmlZ-1):
    SinaBlogUrl='http://blog.sina.com.cn/s/articlelist_'+SinaBlogID+'_0_'+str(key+2)+'.html'
    print('  >> Read Url: '+SinaBlogUrl);
    BlogML=urllib2.urlopen(SinaBlogUrl).read();#读取博客目录
    BlogMLHtml=PyQuery(BlogML)('div.articleList').html();
    BlogMLHtml=PyQuery(BlogMLHtml)('a');
    for li in BlogMLHtml.items(): 
        if li.attr('href').strip()!='' and 'news.sina.com.cn' not in li.attr('href').strip() : BlogMLList[len(BlogMLList)+1]=li.attr('href');
    print('  >> 第'+str(key+2)+'页/共'+str(BlogPgHtmlZ)+'页 记录数：'+str(len(BlogMLHtml)));
    BlogCtHtmlZ2=BlogCtHtmlZ2+len(BlogMLHtml);
    #本地保存
    BlogLBUrlFileName=os.path.basename(SinaBlogUrl.strip());
    fileHandle = open (XHAppDataPath+BlogLBUrlFileName, 'w' );
    fileHandle.write(BlogML);
    fileHandle.close();
    OutHtmlList=OutHtmlList+XHAppDataPath+BlogLBUrlFileName+'\n';
BlogMLList=sorted(BlogMLList.items(), key=lambda d: d[0]);
BlogMLList_Json=json.dumps(BlogMLList,encoding="UTF-8", ensure_ascii=False);
with io.open(XHAppDataPath+SinaBlogID+'_BlogList.json','wb') as json_file:
    json.dump(BlogMLList_Json,json_file,ensure_ascii=False);
OutHtmlList=OutHtmlList+'\n';    
print('  >> 实际博客记录数：'+str(len(BlogMLList)));
print('  >>');
print('  >> 开始读取所有微博页面...');
#开始读取所有博客信息信息
for key in range(len(BlogMLList)):
    BlogBKName=BlogMLList[key][0];#博客索引
    BlogBKUrl=BlogMLList[key][1];#博客网页地址
    BlogFileName=os.path.basename(BlogBKUrl.strip());
    print('  >> Read Blog Url '+str(key+1)+'/'+str(len(BlogMLList))+': '+BlogBKUrl);
    BlogHTML=urllib2.urlopen(BlogBKUrl).read();#读取博客目录
    BlogMLHtml=PyQuery(BlogHTML).html();
    #本地保存
    fileHandle = open (XHAppDataPath+BlogFileName, 'w' );
    fileHandle.write(BlogMLHtml);
    fileHandle.close();
    OutHtmlList=OutHtmlList+XHAppDataPath+BlogFileName+'\n';
OutHtmlList=OutHtmlList+'\n';
fileHandle = open (XHAppDataPath+SinaBlogID+'_HtmlList.txt', 'w' );
fileHandle.write(OutHtmlList);
fileHandle.close();
print('  >>');
print('  >> 全部页面读取完成，开始修饰Html文件...');
