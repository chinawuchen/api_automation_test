import json
from jsonpath_rw import jsonpath,parse

from util.operation_excel import OperationExcel
from data.get_data import GetData
from base.runmain import RunMethod


'''执行依赖case,并拿到依赖的key的values'''
class DependdetData(object):

    def __init__(self, case_id):
        self.case_id = case_id
        self.opera_excel = OperationExcel()
        self.data = GetData()
        self.run_method = RunMethod()

    # 通过case_id去获取该case_id的整行数据
    def get_case_line_data(self):
        row_data = self.opera_excel.get_rows_data(self.case_id)
        return row_data

    # 执行依赖case
    def run_dependent(self):
        row_num = self.opera_excel.get_row_num(self.case_id) # 先要通过case_id去获取依赖case的行号啊
        method = self.data.get_request_method(row_num)
        url = self.data.get_request_url(row_num)
        data = self.data.get_data_for_json(row_num)
        header = self.data.is_header(row_num)
        res = self.run_method.run_main(method, url, data, header, params=data).json()
        # 执行依赖的时候获取响应的json数据,不然我拿不到依赖case的响应,因为我在runmain里面res没有转成json啊，嘿嘿
        return res  # json字典类型

    # 根据依赖的key去获取依赖case的响应，并返回values
    def get_data_for_key(self, row):
        depend_data = self.data.get_depend_key(row)
        response_data = self.run_dependent()
        #print(depend_data)
        #print(response_data)
        #print(type(response_data))
        return [match.value for match in parse(depend_data).find(response_data)][0]
        #json_exe = parse(depend_data)
        #madle = json_exe.find(response_data)
        #return [math.value for math in madle][0]

if __name__ == "__main__":
    run = DependdetData("songli_1")
    print(run.get_data_for_key(2))
