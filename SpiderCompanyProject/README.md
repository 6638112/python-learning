项目功能：
python爬虫项目，主要为从天眼查爬取公司数据，目前已有8000+内蒙古公司数据；

cookie信息：
读取cookie文件->识别为机器人后selectnium自动打开chrome浏览器更新cookie信息->写出至文件；

实现手段：
发送get、post请求+beautifulsoup解析页面->将公司基本信息、详情写出至文件->供es、hbase入库使用；
