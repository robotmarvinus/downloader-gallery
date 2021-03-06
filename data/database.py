import sqlite3
import os

#status:
# - no
# - unknown
# - search
# - action
# - load
# - send
# - ok

class Database():
    def __init__(self, application):
        self.path        = None
        self.application = application
        
        if application.data.pathdata:
            self.set_path(application.data.pathdata)

    def set_path(self, path):
        if path:
            self.path  = path + "/gallery.db"
            if os.path.exists(self.path) == False:
                self.create()

    def create(self):
        try:
            connection = sqlite3.connect(self.path)
            cursor     = connection.cursor()

            query      = "CREATE TABLE 'galleries' ('gallery' TEXT, 'title' TEXT, 'site' TEXT, 'name' TEXT, 'preview' TEXT, 'images' TEXT, 'tags' TEXT, 'status' TEXT)"
            cursor.execute(query)
            connection.commit()

            query      = "CREATE TABLE `config` (`load`	TEXT, `send` TEXT, `token` TEXT, `collection` TEXT)"
            cursor.execute(query)
            connection.commit()

            query      = "CREATE TABLE `sites` (`site` TEXT, `status` TEXT)"
            cursor.execute(query)
            connection.commit()

            query      = "INSERT INTO 'config' ('load', 'send', 'token', 'collection') VALUES (?,?,?,?)"
            cursor.execute(query, ("y", "y", self.application.data.yandex_token, self.application.data.yandex_collection,))
            connection.commit()

            connection.close()

        except Exception as e:            
            self.application.event_print("Ошибка базы данных: create() " + str(e))
            return "Error"
            
    def insert(self, gallery, title, site, name, preview, status='unknown'):
        try:
            connection = sqlite3.connect(self.path)
            cursor     = connection.cursor()
            query      = "INSERT INTO 'galleries' ('gallery', 'title', 'site', 'name', 'preview', 'status') VALUES (?,?,?,?,?,?)"

            cursor.execute(query, (gallery, title, site, name, preview, status,))
            connection.commit()

            connection.close()

            return None
            
        except Exception as e:
            self.application.event_print("Ошибка базы данных: insert() " + str(e))
            return "Error"

    def insert_site(self, value):
        try:
            connection = sqlite3.connect(self.path)
            cursor     = connection.cursor()
            query      = "INSERT INTO 'sites' ('site', 'status') VALUES (?,?)"

            cursor.execute(query, (value, "n",))
            connection.commit()

            connection.close()

        except Exception as e:
            self.application.event_print("Ошибка базы данных: insert() " + str(e))
            return "Error"

    def count(self):
        try:
            connection     = sqlite3.connect(self.path)
            cursor         = connection.cursor()

            cursor.execute("SELECT COUNT(*) FROM 'galleries'")
            records_all    = cursor.fetchall()[0][0]

            cursor.execute("SELECT COUNT(*) FROM 'galleries' WHERE status='unknown'")
            records_main   = cursor.fetchall()[0][0]

            cursor.execute("SELECT COUNT(*) FROM 'galleries' WHERE status='search'")
            records_search = cursor.fetchall()[0][0]

            cursor.execute("SELECT COUNT(*) FROM 'galleries' WHERE status='action' OR status='load'")
            records_load   = cursor.fetchall()[0][0]

            cursor.execute("SELECT COUNT(*) FROM 'galleries' WHERE status='action' OR status='send'")
            records_send   = cursor.fetchall()[0][0]

            cursor.execute("SELECT COUNT(*) FROM 'galleries' WHERE status='ok'")
            records_ok     = cursor.fetchall()[0][0]

            connection.close()

            return [records_all, records_main, records_search, records_load, records_send, records_ok]

        except Exception as e: 
            self.application.event_print("Ошибка базы данных: count() " + str(e))
            return None

    def select(self, value, values=None):
        try:
            connection = sqlite3.connect(self.path)
            cursor     = connection.cursor()

            if value == "find" and values:
                query  = "SELECT * FROM 'galleries' WHERE gallery=? AND site=? AND name=?"
                cursor.execute(query, (values[0], values[1], values[2],))
                result = cursor.fetchone()
            elif value == "unknown":
                query  = "SELECT * FROM 'galleries' WHERE status='unknown' ORDER BY RANDOM()"
                cursor.execute(query)
                result = cursor.fetchone()
            elif value == "unknowns":
                query  = "SELECT * FROM 'galleries' WHERE status='unknown' ORDER BY RANDOM() LIMIT 10"
                cursor.execute(query)
                result = cursor.fetchall()
            elif value == "search":
                query  = "SELECT * FROM 'galleries' WHERE status='search'"
                cursor.execute(query)
                result = cursor.fetchone()
            elif value == "load":
                query  = "SELECT * FROM 'galleries' WHERE status='action' OR status='load' ORDER BY RANDOM()"
                cursor.execute(query)
                result = cursor.fetchone()
            elif value == "send":
                query  = "SELECT * FROM 'galleries' WHERE status='action' OR status='send' ORDER BY RANDOM()"
                cursor.execute(query)
                result = cursor.fetchone()                
            elif value == "name":
                query  = "SELECT * FROM 'galleries' WHERE status='unknown' AND name=? AND site=?"
                cursor.execute(query, (values[0], values[1]))
                result = cursor.fetchall()
            elif value == "config":
                query  = "SELECT * FROM 'config'"
                cursor.execute(query)
                result = cursor.fetchone()
            elif value == "sites":
                query  = "SELECT * FROM 'sites'"
                cursor.execute(query)
                result = cursor.fetchall()

            connection.close()
            return result

        except Exception as e: 
            self.application.event_print("Ошибка базы данных: select() " + str(e))
            return None

    def update(self, gallery, site, name, status, images=None, tags=None):
        try:
            connection = sqlite3.connect(self.path)
            cursor     = connection.cursor()

            if status == "action":
                if tags != None:
                    query  = "UPDATE 'galleries' SET status=?, images=?, tags=? WHERE gallery=? AND site=? AND name=?"
                    cursor.execute(query, (status, images, tags, gallery, site, name,))
                else:
                    query  = "UPDATE 'galleries' SET status=?, images=? WHERE gallery=? AND site=? AND name=?"
                    cursor.execute(query, (status, images, gallery, site, name,))
            else:
                query  = "UPDATE 'galleries' SET status=? WHERE gallery=? AND site=? AND name=?"
                cursor.execute(query, [status, gallery, site, name])

            connection.commit()
            connection.close()
            
        except Exception as e: 
            self.application.event_print("Ошибка базы данных: update() " + str(e))
            return "Error"

        return None

    def update_config(self):
        if self.application.data.load == True:
            load       = "y"
        elif self.application.data.load == False:
            load       = "n"

        if self.application.data.send == True:
            send       = "y"
        elif self.application.data.send == False:
            send       = "n"

        token      = self.application.data.yandex_token
        collection = self.application.data.yandex_collection

        try:
            connection = sqlite3.connect(self.path)
            cursor     = connection.cursor()
            
            query      = "UPDATE 'config' SET load=?, send=?, token=?, collection=? WHERE rowid == 1"
            cursor.execute(query, [load, send, token, collection])

            connection.commit()
            connection.close()
            
        except Exception as e: 
            self.application.event_print("Ошибка базы данных: update() " + str(e))
            return None

    def update_site(self, value):
        try:
            connection = sqlite3.connect(self.path)
            cursor     = connection.cursor()

            query      = "UPDATE 'sites' SET status=? WHERE site=?"
            cursor.execute(query, ("y", value,))

            connection.commit()
            connection.close()

        except Exception as e:
            self.application.event_print("Ошибка базы данных: update_site() " + str(e))
            return "Error"