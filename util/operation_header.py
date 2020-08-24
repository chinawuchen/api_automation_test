import json
import requests

from util.operation_json import OperationJson


class OperationHeader(object):

    def __init__(self, response=None):
        self.response = response

    def get_cookie(self):
        '''获取cookie的jar文件'''
        cookie = self.response.cookies
        return cookie

    # 调用操作json文件的写入方法(把cookie传给它写入)
    def write_cookie(self):
        cookie = requests.utils.dict_from_cookiejar(self.get_cookie())
        print(cookie)
        op_json = OperationJson()
        op_json.write_data(cookie)

if __name__ == "__main__":
    url = "http://enchat.lswsc.com/index.php/api/Login/index"
    data = {"user": "13045899811", "psw": "123456", "login_type": "0"}
    aa = requests.post(url, data)
    print(aa)
    bb = OperationHeader(aa)
    print(bb.get_cookie())
    print(bb.write_cookie())

