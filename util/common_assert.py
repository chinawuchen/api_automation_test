import json
import operator


class CommonUtil(object):

    def is_contain(self, str_one, str_two):
        '''判断实际结果str_one是否在返回结果str_two里面'''
        flag = None
        if str_one in str_two:
            flag = True
        else:
            flag = False
        return flag

    def is_equal_dict(self, dict_one, dict_two):
        '''判断两个字典是否相等'''
        if isinstance(dict_one,str):
            dict_one = json.loads(dict_one)
        if isinstance(dict_two,str):
            dict_two = json.loads(dict_two)
        return operator.eq(dict_one,dict_two)

if __name__ == "__main__":
    run = CommonUtil()
    data1 = {"uid": 1, "phone": "18126834311", "erban_no": "4130633", "password": "0ab44bd43d6b18fcd5cd928d6faab1b8"}
    data2 = {"uid": 1, "phone": "18126834311", "erban_no": "4130633", "password": "0ab44bd43d6b18fcd5cd928d6faab1b8"}
    print(type(data1))
    print(type(data2))
    print(run.is_equal_dict(data1,data2))
