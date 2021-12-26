import sqlite3
def connect():
    try:
        con = sqlite3.connect("users.db")
        cursor = con.cursor()
    
        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                login TEXT NOT NULL,
                password TEXT NOT NULL);""")
        con.commit()

        cursor.execute("""CREATE TABLE IF NOT EXISTS link(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL, 
                link TEXT NOT NULL,
                short_link TEXT NOT NULL,
                access TEXT NOT NULL,
                user_id INT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (ID));""")
        con.commit()

        print("Вы успешно подключились")

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)

    finally:
        con.close()
  
    
def reg(login, password):
        print("Авторизация")
        try:
                con = sqlite3.connect("users.db")
                cursor = con.cursor()
                cursor.execute(""" INSERT INTO users(login, password) VALUES (?, ?);""", (login, password))
                con.commit()
                print("Вы зарегистрированы")
                return "Вы зарегистрированы"       
        except:
                print ('ошибка при регистрации')
        finally:
                con.close()


def getUser(user_id):
        con = sqlite3.connect("users.db")
        cursor = con.cursor()
        check = cursor.execute("""SELECT * FROM users WHERE ID = ?""", (user_id,)).fetchone()
        
        if not check:
                print("Пользователя с таким id нет!")
                return False
        return check
        

        
def auth(login, password):
        print("Вход в систему")
        con = sqlite3.connect("users.db")
        cursor = con.cursor()
        info = cursor.execute("""SELECT * FROM users WHERE login = ? AND password = ?""", (login, password,)).fetchщту()
        print("Вы вошли в систему")


def checkUser(login):
        try:
                con = sqlite3.connect("users.db")
                cursor = con.cursor()
                user = cursor.execute("""SELECT * FROM users where login = ?""", (login,)).fetchone()
                print(user)
                if not user:
                        return 0
                else:
                        return user
                
        except:
                print ('не достал пароль')
                return 'что-то пошло не так'
        finally:
                con.close()


def addLink(name, link, short_link, access, user_id):
        print("Авторизация")
        try:
                con = sqlite3.connect("users.db")
                cursor = con.cursor()
                cursor.execute(""" INSERT INTO link(name, link, short_link, access, user_id) VALUES (?, ?, ?, ?, ?)""", (name, link, short_link, access, user_id))
                con.commit()
                print("Ссылка сокращена")
                return "Ссылка сокращена"       
        except:
                print ('ошибка сокращения')
        finally:
                con.close()


def getLink(user_id, link_id):
        try:
                con = sqlite3.connect("users.db")
                cursor = con.cursor()
                info = cursor.execute(""" SELECT * FROM link where user_id = ? and ID = ?""", (user_id, link_id,)).fetchone()

                return info

        except sqlite3.Error as err:
                print(err)
                return "false"
        finally:
                con.close()


def getLinks(user_id):
        try:
                con = sqlite3.connect("users.db")
                cursor = con.cursor()
                info = cursor.execute(""" SELECT * FROM link where user_id = ?""", (user_id,)).fetchall()

                return info
                        
        except sqlite3.Error as err:
                print(err)
                return "false"
        finally:
                con.close()


def delLinks(user_id, link_id):
        try:
                con = sqlite3.connect("users.db")
                cursor = con.cursor()

                cursor.execute(""" DELETE FROM link
                                where ID = ? and user_id = ?""", (link_id, user_id))
                con.commit()

                return "Ссылка удалена"

        except sqlite3.Error as err:
                print(err)
                return "false"
        finally:
                con.close()


def updateLinks(name, access, user_id, link_id):
        try:
                con = sqlite3.connect("users.db")
                cursor = con.cursor()

                cursor.execute(""" UPDATE link SET name = ? 
                                where ID = ? and user_id = ?""", (name, link_id, user_id))
                con.commit()

                cursor.execute(""" UPDATE link SET access = ? 
                                                where ID = ? and user_id = ?""", (access, link_id, user_id))
                con.commit()

                return "Ссылка обновлена"

        except sqlite3.Error as err:
                print(err)
                return "false"
        finally:
                con.close()



try:
        con = sqlite3.connect("users.db")
        cursor = con.cursor()

except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)

finally:
        con.close()