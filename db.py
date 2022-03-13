import sqlite3

import db


class DataBase():
    def __init__(self,db_file):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_users(self,user_id,nickname):
        """Создаём нового пользователя"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`,`nickname`) VALUES (?,?)",(user_id,nickname))

    def user_exists(self,user_id):
        """Проверяем наличие пользователя в БД"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `users` WHERE `user_id` = ?',(user_id,)).fetchall()
            return bool(len(result))

    def add_subscribe(self,user_id):
        with self.connection:
            return self.cursor.execute("INSERT INFO `users` (`user_id`,`time_sub`) VALUES(?,?)",(user_id,30))

    def exists_subscribe(self,user_id,status):
            result = self.cursor.execute('SELECT * FROM `users` WHERE `user_id` = ? AND `time_sub` > 0 ',(user_id,)).fetchall()
            return bool(len(result))

    def update_subscribe(self,user_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `subscribe_status` = ?  WHERE `user_id` = ?",(True,user_id,))