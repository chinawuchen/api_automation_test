import xlrd
from xlutils.copy import copy


class OperationExcel(object):

    # 初始化的时候默认一个file_name和sheet_id
    def __init__(self, file_name=None, sheet_id=None):
        if file_name:
            self.file_name = file_name
            self.sheet_id = sheet_id
        else:
            self.file_name = "D:\GZRJ\Python_XM\\api_automation_test\dataconfig\songli.xlsx"
            self.sheet_id = 0
        self.data = self.get_data()

    # 获取sheets内容
    def get_data(self):
        data = xlrd.open_workbook(self.file_name)
        tables = data.sheets()[self.sheet_id]
        return tables

    # 获取单元格的行数
    def get_lines(self):
        return self.data.nrows

    # 获取单元格的内容
    def get_cell_value(self, row, col):
        return self.data.cell_value(row, col)

    # 把测试结果写入excel
    def write_value(self, row, col, value):
        '''
        往excel中写入数据  row行, col列, value值
        '''
        read_data = xlrd.open_workbook(self.file_name) # 1.先打开excel
        write_data = copy(read_data) # 2.然后复制一份
        sheet_data = write_data.get_sheet(0) # 3.通过sheet去获取复制的文件的内容
        sheet_data.write(row, col, value) # 4.往exc中写入测试结果
        write_data.save(self.file_name) # 5.将写入的数据保存

    '''获取依赖数据,先通过依赖case_id去找到行号，然后通过行号去获取该行的数据'''
    # 根据case_id 找到对应行的内容
    def get_rows_data(self, case_id):
        row_num = self.get_row_num(case_id) # 调用get_row_num找到行号
        row_data = self.get_row_values(row_num) # 把找到的行号给get_row_values，并找到该行的内容
        return row_data

    # 根据对应的case_id找到对应的行号
    def get_row_num(self, case_id):
        num = 0
        clols_data = self.get_cols_data()
        case_id = str(case_id)
        for col_data in clols_data:
            if case_id in col_data:
                return num
            num += 1
        #return num

    # 根据行号，找到该行的内容
    def get_row_values(self, row):
        tables = self.data
        row_data = tables.row_values(row)
        return row_data

    # 获取某一列的内容，给get_row_num去调用然后循环
    def get_cols_data(self, col_id=None):
        if col_id != None:
            clos = self.data.col_values(col_id)
        else:
            clos = self.data.col_values(0)
        return clos

if __name__ == "__main__":
    run = OperationExcel()
    print(run.get_lines())
    print(run.get_cell_value(2,3))

