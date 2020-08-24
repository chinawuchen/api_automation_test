from util.operation_excel import OperationExcel
from util.operation_json import OperationJson
from util.connect_db import OperationMysql
from data import data_config


class GetData(object):

    def __init__(self):
        self.oper_excel = OperationExcel()
        self.opera_mysql = OperationMysql()

    # 去获取excel的行数，就是case(用例)的个数
    def get_case_lines(self):
        return self.oper_excel.get_lines()

    # 获取是否执行
    def get_is_run(self, row):
        flag = None
        col = int(data_config.get_run())
        run_model = self.oper_excel.get_cell_value(row, col)
        if run_model == "yes":
            flag = True
        else:
            flag = False
        return flag

    # 获取请求方式
    def get_request_method(self, row):
        col = int(data_config.get_request_way())
        request_method = self.oper_excel.get_cell_value(row, col)
        return request_method

    # 获取url
    def get_request_url(self, row):
        col = int(data_config.get_url())
        url = self.oper_excel.get_cell_value(row, col)
        return url

    # 获取请求头header关键字
    def is_header(self, row):
        col = int(data_config.get_header())
        header = self.oper_excel.get_cell_value(row, col)
        if header == "":
            return None
        else:
            return header

    # 通过请求头关键字拿到data数据
    def get_header_value(self, row):
        opera_json = OperationJson("D:\GZRJ\Python_XM\\api_automation_test\dataconfig\\request_header.json")
        request_header = opera_json.get_data(self.is_header(row))
        return request_header

    # 获取请求数据
    def get_request_data(self, row):
        col = int(data_config.get_data())
        data = self.oper_excel.get_cell_value(row, col)
        if data == "":
            return None
        else:
            return data

    # 获取json数据,根据get_request_data的返回值获取
    def get_data_for_json(self, row):
        opera_json = OperationJson()
        request_data = opera_json.get_data(self.get_request_data(row))
        return request_data

    # 获取预期结果
    def get_expcet_data(self, row):
        col = int(data_config.get_expect())
        expect = self.oper_excel.get_cell_value(row, col)
        if expect == "":
            return None
        else:
            return expect

    # 通过sql获取预期结果
    def get_expcet_data_for_mysql(self, row):
        sql = self.get_expcet_data(row)
        res  = self.opera_mysql.search_one(sql)
        return res
        #return res.encode('unicode-escape')

    # 往excel中写入测试结果(直接调用operation_excel中的写入方法，把row, col, value传入就可以了)
    def write_result(self, row, value):
        col = int(data_config.get_result())
        self.oper_excel.write_value(row, col, value)

    # 判断是否有case依赖
    def is_depend(self, row):
        col = int(data_config.get_case_depend())
        depend_case_id = self.oper_excel.get_cell_value(row, col)
        if depend_case_id == "":
            return None
        else:
            return depend_case_id

    # 获取依赖数据的key
    def get_depend_key(self, row):
        col = int(data_config.get_data_depend())
        depend_key = self.oper_excel.get_cell_value(row, col)
        if depend_key == "":
            return None
        else:
            return depend_key

    # 获取依赖数据的所属字段
    def get_depend_field(self, row):
        col = int(data_config.get_field_depend())
        data = self.oper_excel.get_cell_value(row, col)
        if data == "":
            return None
        else:
            return data

if __name__ == "__main__":
    run = GetData()
    print(run.get_is_run(2))
    print(run.get_request_method(2))
    print(run.get_request_url(2))
    print(run.get_request_data(2))
    print(run.get_data_for_json(2))
    print(run.get_expcet_data(2))
    #print(run.get_depend_key(2))
    #print(run.is_depend(2))
    #print(run.get_depend_field(2))
    print("=============")
    print(run.is_header(2))
    print(run.get_header_value(2))









