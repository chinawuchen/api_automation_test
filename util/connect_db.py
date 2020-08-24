import json
import pymysql.cursors


class OperationMysql(object):

    def __init__(self):
        self.conn = pymysql.connect(
            host = "47.240.70.216",
            user = "root",
            passwd = "3b60e8832efcfa85",
            db = "hub_zzbtest_com",
            port = 3306,
            charset = "utf8",
            cursorclass = pymysql.cursors.DictCursor  # 以字典的形式返回操作结果，key:value
        )
        self.cur = self.conn.cursor() # 创建一个游标，根据游标去查询数据

    def search_one(self, sql):
        self.cur.execute(sql) # 1.查询
        result = self.cur.fetchone() # 2.保存查询的结果
        return json.dumps(result, default=str, ensure_ascii=False)

if __name__ == "__main__":
    sql = OperationMysql()
    aa = sql.search_one("SELECT * FROM hb_member where user_email='1102055693@qq.com'")
    print(aa)
    print(type(aa))