# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web

from dbconn import db_cursor

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/main.html")


class CourseListHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/cou_list.html", courses = dal_list_courses())

class CourseEditHandler(tornado.web.RequestHandler):
    def get(self, stu_no):

        cou = None
        if stu_no != 'new' :
            cou = dal_get_course(stu_no)
        
        if cou is None:
            cou = dict(stu_no='new', name='', birthday='', sex='',stclass='')

        self.render("pages/cou_edit.html", stulist = cou)

    def post(self, stu_no):
        name = self.get_argument('name')
        birthday = self.get_argument('birthday')
        sex = self.get_argument('sex')
        stclass  = self.get_argument('stclass') 

        if stu_no == 'new' :
            dal_create_course(name, birthday,sex,stclass)
        else:
            dal_update_course(stu_no,name,birthday,sex,stclass)

        self.redirect('/coulist')

class CourseDelHandler(tornado.web.RequestHandler):
    def get(self, stu_no):
        dal_del_course(stu_no)
        self.redirect('/coulist')

# -------------------------------------------------------------------------

def dal_list_courses():
    data = []
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        SELECT * FROM stulist ORDER BY stu_no DESC
        """
        cur.execute(s)      
        for r in cur.fetchall():
            cou = dict(stu_no=r[0],name=r[1], birthday=r[2],sex=r[3],stclass=r[4])
            data.append(cou)
    return data


def dal_get_course(stu_no):
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        SELECT * FROM stulist WHERE stu_no=%s
        """
        cur.execute(s, (stu_no, ))
        r = cur.fetchone()
        if r :
            return dict(stu_no=r[0],name=r[1], birthday=r[2],sex=r[3],stclass=r[4])

def dal_create_course(name, birthday,sex,stclass):
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        cur.execute("SELECT nextval('seq_stu_sn')")
        stu_no = cur.fetchone()
        assert stu_no is not None

        print('新学生学号%d: ' % stu_no)

        s = """
        INSERT INTO stulist (stu_no,name, birthday,sex,stclass)
        VALUES (%(stu_no)s, %(name)s, %(birthday)s, %(sex)s,%(stclass)s)
        """
        cur.execute(s, dict(stu_no=stu_no,name=name, birthday=birthday,sex=sex,stclass=stclass))


def dal_update_course(stu_no,name, birthday,sex,stclass):
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        UPDATE stulist SET
          stu_no=%(stu_no)s, 
          name=%(name)s, 
          birthday=%(birthday)s,
          sex=%(sex)s, 
          stclass=%(stclass)s
        WHERE stu_no=%(stu_no)s
        """
        cur.execute(s, dict(stu_no=stu_no,name=name, birthday=birthday,sex=sex,stclass=stclass))

def dal_del_course(stu_no):
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        DELETE FROM stulist WHERE stu_no=%(stu_no)s
        """
        cur.execute(s, dict(stu_no=stu_no))
        print('删除%d条记录' % cur.rowcount)
