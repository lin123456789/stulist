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


def dal_list_courses():
    data = []
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        SELECT *  FROM stulist  ORDER BY stu_no DESC
        """
        cur.execute(s)      
        for r in cur.fetchall():
            cou = dict(stu_no=r[0],name=r[1], birthday=r[2],sex=r[3],stclass=r[4])
            data.append(cou)
    print(data)
    return data

 