# python-funny
有趣有料，边学边玩

### mzitu  

- 基于py2 
- 爬取美女图片


- www.haoip.cc   proxy ip 
- mzitu pictures of beautiful girls

引入模块:

- requests urllib的升级版本
- re 正则表达式模块
- random 随机
- beautifulsoup4 你懂的
- lxml 一个HTML解析包 

```pyt
# download dir 
Mzitu = mzitu('H:/mzitu')
# home url
Mzitu.do_spider('http://www.mzitu.com/all')
```



### douban

- 基于py2


- 豆瓣书，爬取分类，评分，评分人数
- Book.py  主执行
- DupBook.py 分类下书籍有重复，手动去重

写的比较乱，比较简单。支持断点续爬，数据入mysql。

生成日志文件 myapp.log

