from sys import stderr

class User:
    def __init__(self, id, nm, pwd, email, descr) -> None:
        self.userid          = id
        self.username        = nm
        self.userpassword    = pwd
        self.useremail       = email
        self.userdescription = descr
        self.roles           = []       # array of roles for user, as text
