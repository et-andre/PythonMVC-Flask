from app import db

class User(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    useremail = db.Column(db.String(100), unique=True, nullable=False)
    userpassword = db.Column(db.String(255), nullable=False)
    userdescription = db.Column(db.String(255), nullable=True)
    # def __init__(self, userid, username, userpassword, useremail, userdescription) -> None:
    #     self.userid = userid
    #     self.username = username
    #     self.userpassword = userpassword
    #     self.useremail = useremail
    #     self.userdescription = userdescription
    #     self.roles = []
    #
    # def isAdmin(self):
    #    print(self.roles, file=stderr)
    #    print("ADMIN" in self.roles, file=stderr)
    #    isAdmin = "ADMIN" in self.roles
    #    return isAdmin