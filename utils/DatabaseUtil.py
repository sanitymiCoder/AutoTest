
import pymysql
import pymysql.cursors
from utils.ConfigParseUtil import ConfigParseUtil


conf = ConfigParseUtil()

class ConnectMysql:
    
    def __init__(self) -> None:
        self.conf = {
            'host':conf.get_db_value('host'),
            'port':conf.get_db_value('port'),
            'user':conf.get_db_value('user'),
            'password':conf.get_db_value('password'),
            'database':conf.get_db_value('database'),
        }
        try:
            self.conn = pymysql.connect(**self.conf)
            #获取操作游标
            #cursor=pymysql.cursors.DictCursor:将查询结果以键值对返回（默认是元组）
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            print(f'成功连接数据库，数据库ip：{self.conf.get('host')}')
        except Exception as e:
            print(f'连接数据库失败，-原因{e}')
            
    def close(self):
        if self.conn and self.cursor:
            self.cursor.close()
            self.conn.close()
        return True
            
            
    def query(self,sql,fetchall=False):
        """查询数据库数据
        Args:
            sql (_type_): sql语句
            fetchall (bool, optional):查询单条数据或者多条数据
        Returns:
            _type_: _description_
        """
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            if fetchall:
                res = self.cursor.fetchall()
            else:
                res = self.cursor.fetchone()
            return res
        except Exception as e:
            print(f'查询数据库出现异常，-原因{e}')
        finally:
            self.close()
            
            
    def delete(self,sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            print('数据库删除数据成功')
        except Exception as e:
            print(f'删除数据库出现异常-{e}')
        finally:
            self.close()
        
        
    