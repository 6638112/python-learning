import os
import cx_Oracle
import logging
logging.basicConfig(level=logging.DEBUG)

class OracleHelper:
    """
    oracle查询工具类
    """

    def __init__(self, user, pwd, locator):
        """
        初始化
        :param user:用户名
        :param pwd: 密码
        :param locator:监听（host/orcl）
        """
        self.conn = cx_Oracle.connect(user, pwd, locator)
        self.cursor = self.conn.cursor()

    def select(self, sql):
        result = self.cursor.execute(sql).fetchall()#得到所有数据集
        for row in result:
            logging.debug(row)

        # while True:
        #     rs = self.cursor.fetchone()
        #     if rs == None:
        #         break
        #     logging.debug(rs)
        self.cursor.close()
        self.conn.close()
        return result

    def sqlDML(self, sql):
        self.cursor.execute(sql)
        self.cursor.close()
        self.conn.commit()