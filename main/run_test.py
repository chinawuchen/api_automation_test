import json
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from base.runmain import RunMethod
from data.get_data import GetData
from data.dependent_data import DependdetData
from util.common_assert import CommonUtil
from util.operation_header import OperationHeader
from util.operation_json import OperationJson
from util.send_email import SendEmail
from util.run_log import initLogging


class RunTest(object):

    def __init__(self):
        self.run_method = RunMethod()
        self.data = GetData()
        self.com_util = CommonUtil()
        self.send_mail = SendEmail()

    # 程序开始执行
    def go_on_run(self):
        res = None
        # 定义三个列表,存储成功,失败,未执行的用例(case_id)
        pass_count = []
        fail_count = []
        no_run_count = []

        # 每次执行用例之前将log日志文件清空数据
        log_file = "D:\GZRJ\Python_XM\\api_automation_test\log\log.txt"
        with open(log_file,'w') as f:
            f.seek(0,0) # 加上f.seek(0)，把文件定位到position 0;没有这句的话，文件是定位到数据最后，truncate也是从最后这里删除
            f.truncate()

        # 先获取excel表格的行数
        row_count = self.data.get_case_lines()
        print("start_用例开始执行,请稍候.....")

        for i in range(1, row_count): # 每循环一次，拿一次接口的所有数据
            try:
                # 先拿到is_run判断是否执行,如果是yes(会返回Ture),就去拿其它数据
                is_run = self.data.get_is_run(i)
                if is_run == True:
                    method = self.data.get_request_method(i)
                    url = self.data.get_request_url(i)
                    data = self.data.get_data_for_json(i)
                    header_key = self.data.is_header(i) # 获取excel文件中header关键字
                    header = self.data.get_header_value(i) # 获取json文件中header_key对应的头文件数据
                    expect = self.data.get_expcet_data(i) # 这里拿到的预期结果是字符串
                    # expect = self.data.get_expcet_data_for_mysql(i) # 断言方法如果是is_equal_dict就要取数据库这个值
                    depend_case = self.data.is_depend(i) # 获取依赖case_id

                    # 判断是否有依赖id，然后把返回数据替换到请求数据
                    if depend_case != None:
                        self.depend_data = DependdetData(depend_case)
                        # 1.获取依赖的响应字段数据
                        depend_response_data = self.depend_data.get_data_for_key(i)
                        # 2.获取需要替换的字段
                        depend_key = self.data.get_depend_field(i)
                        # 3.把1步拿到的values去替换第2步拿到的字段
                        data[depend_key] = depend_response_data

                    # 判断是否要写入,获取cookie
                    if header_key == "write_Cookies":
                        res = self.run_method.run_main(method, url, data, header, params=data)
                        op_header = OperationHeader(res)
                        op_header.write_cookie()
                        res = res.json()  # 先获取cookies再转成json字典类型,不然后面无法和预期结果对比
                    elif header_key == "get_Cookies":
                        op_json = OperationJson("D:\GZRJ\Python_XM\\api_automation_test\dataconfig\cookie.json")
                        cookie = op_json.get_data("PHPSESSID")
                        cookies = {"PHPSESSID": cookie}
                        #print(cookies)
                        res = self.run_method.run_main(method, url, data, header, params=data, cookies=cookies).json()
                    else:
                        res = self.run_method.run_main(method, url, data, header, params=data).json()
                    #print(res)
                    #print(res["data"]["accessToken"])

                    # 判断预期结果是否在返回结果里面，需要把返回结果res转成json字符串中文和预期结果比较
                    if self.com_util.is_contain(expect, json.dumps(res, ensure_ascii=False)):
                        self.data.write_result(i, "pass")
                        pass_count.append(i)
                    else:
                        self.data.write_result(i, json.dumps(res, ensure_ascii=False))
                        with open(log_file, 'a', encoding='utf-8') as f:
                            f.write("\n第%s条用例实际结果与预期结果不一致:\n" % i)
                            f.write("Expected:%s\n  Actual:%s\n" % (expect, res))
                        fail_count.append(i)

                # 如果is_run是no,会返回False,然后把当前的case_id(行号)写入no_run_count
                else:
                    no_run_count.append(i)

            except Exception as e:
                # 将异常写入excel的测试结果中
                self.data.write_result(i, str(e))
                # 将报错写入指定路径的日志文件里
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.write("\n第%s条用例报错:\n" % i)
                initLogging(log_file, e)
                fail_count.append(i)

                """                  
                    if self.com_util.is_equal_dict(expect, res):
                        self.data.write_result(i, "PASS")
                        pass_count.append(i)
                    else:
                        self.data.write_result(i, res)
                        fail_count.append(i)
                                              """
        #我这里打印了一下用例的执行情况，嘿嘿
        print("end_用例执行完毕！")
        print("成功的用例：%s" % pass_count)
        print("失败的用例：%s" % fail_count)
        #print("未执行的用例：%s" % no_run_count)
        # 调用发送邮件
        #self.send_mail.send_main(pass_count, fail_count)

if __name__ == "__main__":
    run = RunTest()
    run.go_on_run()
