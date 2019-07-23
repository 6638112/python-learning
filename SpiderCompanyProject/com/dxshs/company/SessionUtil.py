# import requests
# import http.cookiejar as cj
#
# r = requests.session()
# r.cookies = cj.LWPCookieJar()  # 接入容器
# r.get(url,headers=,cookie=) # 不过需要注意，就算使用了会话，方法级别的参数也不会被跨请求保持,此cookie只发送给该请求
# print(r.text)
# r.post(url,headers=,data=,)
# #请求x N
# r.cookies.save(filename='cookies.txt', ignore_discard=True, ignore_expires=True)  # 保存cookie到本地，忽略关闭浏览器丢失，忽略失效
# r.close() # 对话支持with打开以实现自动close
#
#
# '''#载入本地cookie
# s = requests.session()
# s.cookies = cj.LWPCookieJar(filename='cookies.txt')
# s.cookies.load(filename='cookies.txt', ignore_discard=True)
# '''