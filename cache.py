import sqlite3


class PlotCache(object):
    CREATE = 'create table if not exists plots (id int primary key, vault int, batch int, protocol int, plot text)'
    SELECT = 'select plot from plots where vault = ? and batch = ? and protocol = ?'
    INSERT = 'insert into plots (vault, batch, protocol, plot) values (?, ?, ?, ?)'

    def __init__(self, db):
        self.db = db

    def get(self, top_folder, middle_folder, bottom_folder):
        with sqlite3.connect(self.db) as db:
            cur = db.cursor()
            cur.execute(self.SELECT, (
                top_folder,
                middle_folder,
                bottom_folder,
            ))
            res = cur.fetchone()
            return res[0]

    def put(self, first, second, file_name, blob):
       cur.execute(self.INSERT, (first, second, file_name, blob))
       db.commit()
