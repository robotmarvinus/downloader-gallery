import os

class Data():
    def __init__(self):
        self.pathhome = os.environ['HOME']
        self.pathconf = self.pathhome + "/.local/share/aurelia/downloaders/gallery.txt"
        self.pathview = self.pathhome + "/.local/share/aurelia/downloaders/thumbs"
        self.pathdata = None
        self.pathimgs = None

        self.load = True
        self.send = True

        self.yandex_token      = "AgAAAAA5lcFYAAYBS37o67UnWkqnh-jXkmMDeiI"
        self.yandex_collection = "5df9d8a840a3238279b61bf1"

        self.records_all    = None
        self.records_main   = None
        self.records_search = None
        self.records_load   = None
        self.records_send   = None
        self.records_ok     = None
        self.records_no     = 0

        self.sites = [
            ["theomegaproject.org", None]
        ]

        self.load_config()

    def load_config(self):
        if os.path.exists(self.pathconf):
            fopen = open(self.pathconf, "r")
            array = fopen.read().split("\n")
            fopen.close()
            if len(array) == 2 and os.path.isdir(array[0]) and os.path.isdir(array[1]):
                self.pathdata = array[0]
                self.pathimgs = array[1]
        else:
            dirconf = os.path.dirname(self.pathconf)
            if os.path.exists(dirconf) == False:
                os.mkdir(dirconf)

            fopen = open(self.pathconf, "w+")
            fopen.close()

    def load_db_config(self, database):
        result = database.select("config")
        if result:
            if result[0] == "y":
                self.load = True
            elif result[0] == "n":
                self.load = False

            if result[1] == "y":
                self.send = True
            elif result[1] == "n":
                self.send = False

            self.yandex_token = result[2]
            self.yandex_collection = result[3]

    def load_db_sites(self, database):
        find  = False
        sites = database.select("sites")
        for item in self.sites:
            find  = False
            for it in sites:
                if item[0] == it[0]:
                    if it[1] == "n":
                        item[1] = False
                    elif it[1] == "y":
                        item[1] = True
                    find = True

            if find == False:
                database.insert_site(item[0])
                item[1] = False

    def load_db_records(self, database):
        data = database.count()
        if data:
            self.records_all    = data[0]
            self.records_main   = data[1]
            self.records_search = data[2]
            self.records_load   = data[3]
            self.records_send   = data[4]
            self.records_ok     = data[5]

    def get_site_status(self, value):
        for item in self.sites:
            if item[0] == value:
                return item[1]

    def data_save(self, load, send, yandex_token, yandex_collection, path_one, path_two):
        try:
            self.load     = load
            self.send     = send
            self.pathdata = path_one
            self.pathimgs = path_two
            self.yandex_token = yandex_token
            self.yandex_collection = yandex_collection
            
            fileopen = open(self.pathconf, 'w')
            fileopen.write(path_one + "\n" + path_two)
            fileopen.close()

            return True
        except Exception:
            return "Error"

    def file_exist(self, path):
        return os.path.exists(path)

    def is_dir(self, path):
        return os.path.isdir(path)

    def is_file(self, path):
        return os.path.isfile(path)

    def make_dir(self, path):
        os.makedirs(path)