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
                cursor.execute(""" INSERT INTO link(name, link, short_link, access, user_id) VALUES (?, ?, ?, ?, ?);""", (name, link, short_link, access, user_id))
                con.commit()
                print("Ссылка сокращена")
                return "Ссылка сокращена"       
        except:
                print ('ошибка сокращения')
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



# def checkLink(user_id, link_id):
#         try:
#                 con = sqlite3.connect("users.db")
#                 cursor = con.cursor()

#                 subscrs = cursor.execute(""" SELECT * FROM subscribes 
#                                         where user_id = ? and
#                                          category_id=?""", (user_id, link_id)).fetchone()

#                 if subscrs == None:
#                         return 0
#                 else:
#                         return 1

                      

#         except sqlite3.Error as err:
#                 print(err)
#                 return "false"
#         finally:
#                 con.close()



# def delLinks(user_id, link_id):
#         try:
#                 con = sqlite3.connect("users.db")
#                 cursor = con.cursor()

#                 catName = cursor.execute("""SELECT name FROM category where ID = ? """, (link_id,)).fetchall()

#                 subscrs = cursor.execute(""" SELECT link_id FROM links 
#                                         where user_id = ? and
#                                         link_id=?""", (user_id,link_id,)).fetchone()

#                 if not subscrs:
#                         print(f"Данной ссылки не существует {catName[0][0]}")
#                         return catName[0][0]
#                 else:
#                         delSub = cursor.execute(""" DELETE FROM links 
#                                         where link_id = ?""", (link_id,))
#                         con.commit()
                        
#                         print(f"Вы удалили ссылку {catName[0][0]}")
#                         return catName[0][0]
                
#         except sqlite3.Error as err:
#                 print(err)
#                 return "false"
#         finally:
#                 con.close()

try:
        con = sqlite3.connect("users.db")
        cursor = con.cursor()

except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)

finally:
        con.close()