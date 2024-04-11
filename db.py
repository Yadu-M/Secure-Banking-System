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
            db.insert({
                "username": username,
                "pass": password,
                "balance": 0})
            return "success"
    except Exception as e:
        raise Exception(e)

def auth(username, password):
    try:
        User = Query()
        account = db.search(User.username == username)       
        if (len(account) == 0):
            raise Exception("No account found lil bro")

        # print(account[0]['pass'])
        if str(account[0]["pass"]) == str(password):
            return account[0]["balance"]
            # return "success"
        else:
            raise Exception("Wrong password detected")

    except Exception as e:
        raise Exception(e)

# def userinfo(username):
#     try:
#         User = Query()
#         account = db.search(User.username == username)
#         if (len(account) == 0):
#             raise Exception("No account found lil bro")

#         print(str(account))

#     except Exception as e:
#         raise Exception(e)


def deposit(username: str, amount: int):
    try:
        User = Query()
        account = db.search(User.username == username)[0]
        if len(account) == 0:
            raise Exception("No account found lil bro")

        print("Old account:", account)
        newBalance = account["balance"] + amount
        db.update({"balance": newBalance}, User.username == username)

        # Optionally fetch the updated account to confirm
        updated_account = db.search(User.username == username)[0]
        print("Updated account:", updated_account)
        return newBalance

    except Exception as e:
        raise Exception(e)


def withdraw(username: str, amount: int):
    try:
        User = Query()
        account = db.search(User.username == username)[0]
        if len(account) == 0:
            raise Exception("No account found lil bro")

        print("Old account:", account)
        newBalance = account["balance"] - amount
        db.update({"balance": newBalance}, User.username == username)

        # Optionally fetch the updated account to confirm
        updated_account = db.search(User.username == username)[0]
        print("Updated account:", updated_account)
        return newBalance

    except Exception as e:
        raise Exception(e)

def getBalance(username: str):
    try:
        User = Query()
        account = db.search(User.username == username)[0]
        if len(account) == 0:
            raise Exception("No account found lil bro")

        # Optionally fetch the updated account to confirm
        return account["balance"]

    except Exception as e:
        raise Exception(e)
