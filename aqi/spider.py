import execjs
import json
import requests

# Init environment
# node = execjs.get()  # window not defined
node = execjs.get('PhantomJS')

# Params
method = 'GETCITYWEATHER'
city = '北京'
type_backup = type
type = 'HOUR'
start_time = '2018-01-25 00:00:00'
end_time = '2018-01-25 23:00:00'

# Compile javascript
file = 'encryption.js'
ctx = node.compile(open(file).read())
# Get params
js = 'getEncryptedData("{0}", "{1}", "{2}", "{3}", "{4}")'.format(method, city, type, start_time, end_time)
print(js)
params = ctx.eval(js)

print(params)

url = 'https://www.aqistudy.cn/apinew/aqistudyapi.php'
response = requests.post(url, data={'d': params})

js1 = 'decodeData("{0}")'.format(response.text)

decrypted_data = ctx.eval(js1)

print(type_backup(decrypted_data))

s = json.loads(decrypted_data)
print(s)