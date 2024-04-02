from tinydb import TinyDB, Query

DB_PATH = 'database.json'
db = TinyDB(DB_PATH)

def add_user(username, password):
    try:
        query = Query()
        check = db.contains(query.username == username)
        if check:
            raise Exception("User already exists")
        else:
            db.insert({"username": username,"pass": password})
            return "success"
    except Exception as e:
        raise Exception(e)

def auth(username, password):
    try:
        User = Query()
        account = db.search(User.username == username)        
        if (len(account) == 0):
            raise Exception("No account found lil bro")

        print(account[0]['pass'])
        if account[0]['pass'] == password:
            return "success"
        else:
            raise Exception("Wrong password detected")

    except Exception as e:
        raise Exception(e)

