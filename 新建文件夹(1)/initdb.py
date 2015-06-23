#! /usr/bin/env python3
# -*- coding:UTF-8 -*-

from dbconn import db_cursor

def create_db():
    sqlstr = """
    DROP TABLE IF EXISTS stulist;

    CREATE TABLE IF NOT EXISTS stulist  (
        stu_no   VARCHAR(10),        --学号
        name       TEXT,        --姓名
        birthday    DATE,     --出生日期
        sex      CHAR(5),        --性别
        stclass    TEXT,        --班级
        PRIMARY KEY(stu_no)
    );
    -- CREATE UNIQUE INDEX idx_stulist_no ON stulist(stu_no);

    CREATE SEQUENCE seq_stu_sn 
        START 10000 INCREMENT 1 OWNED BY stulist.stu_no;

    """
    with db_cursor() as cur :
        cur.execute(sqlstr) # 执行SQL语句
    
def init_data():
    sqlstr = """
    DELETE FROM stulist;

    INSERT INTO stulist ( stu_no, name,birthday,sex,stclass)  VALUES 
        ('1210650301',  '张三','1993.2.3','男','1303'),
        ('1310650102',  '王五','1994.5.5','男','1301'),
        ('1310650202',  '立夏','1994.10.25','女','1302'),
        ('1310650312',  '黄国','1994.7.7','男','1303'),
        ('1310650422',  '王艳','1994.2.5','女','1304');
        

    """
    with db_cursor() as cur :
        cur.execute(sqlstr)    

if __name__ == '__main__':
    create_db()
    init_data()
    print('数据库已初始化完毕！')

