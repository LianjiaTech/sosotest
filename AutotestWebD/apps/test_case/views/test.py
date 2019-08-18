import urllib.request

url = "http://www.baidu.com"
get = urllib.request.urlopen(url).read()
print(get)