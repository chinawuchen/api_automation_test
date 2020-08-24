import json


class OperationJson(object):

    # 初始化读取json文件
    def __init__(self, file_path=None):
        if file_path == None:
            self.file_path = "D:\GZRJ\Python_XM\\api_automation_test\dataconfig\songli.json"
        else:
            self.file_path = file_path
        self.data = self.read_data()

    # 读取json文件
    def read_data(self):
        with open(self.file_path, encoding='UTF-8') as fp:
            data = json.load(fp)
            return data

    # 根据关键字获取数据
    def get_data(self, id):
        return self.data.get(id)

    # 将cookies写入json文件
    def write_data(self, data):
        with open("D:\GZRJ\Python_XM\\api_automation_test\dataconfig\cookie.json", "w") as fp:
            fp.write(json.dumps(data))

if __name__ == "__main__":
    run = OperationJson()
    print(run.get_data("songli_1"))
