import requests
import json


class RunMethod(object):

    def post_main(self, url, data=None, header=None, cookies=None):
        res = None
        if header != None:
            res = requests.post(url=url, data=data, headers=header, cookies=cookies)
            # 如果是https请求无法发送加上verify=False，忽略https
        else:
            res = requests.post(url=url, data=data, cookies=cookies)
        return res

    def get_main(self, url, params=None, header=None, cookies=None):
        res = None
        if header != None:
            res = requests.get(url=url, params=params, headers=header, cookies=cookies)
        else:
            res = requests.get(url=url, params=params, cookies=cookies)
        return res

    def run_main(self, method, url, data=None, header=None, params=None, cookies=None):
        res = None
        if method == "post":
            res = self.post_main(url, data, header, cookies)
        else:
            res = self.post_main(url, params, header, cookies)
        return res
        #return json.dumps(res, ensure_ascii=False)

if __name__ == "__main__":
    run = RunMethod()
    url = "http://hubskins.zzbtest.com/front/member/login"
    data = {"user_email": "1102055693@qq.com","user_pass": "wu123456"}
    res = run.run_main("post", url, data)
    print(res)
    print(type(res))




