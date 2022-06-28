import bcrypt

from sys                            import stderr
from flask                          import session

from app                            import conn

from app.models.User                import User
from app.models.Role                import Role

from app.services.IService          import IService
from app.services.UserRoleService   import UserRoleService

from app.forms.UserUpdateForm       import UserUpdateForm

class UserService(IService):
    def __init__(self) -> None:
        self.userRoleService = UserRoleService()

    def login(self, user: User):
        usr = self.findOneBy(username=user.username)
        if usr == None:     # user not found
            return None
        if not bcrypt.checkpw(user.userpassword.encode("utf-8"), usr.userpassword.encode("utf-8")):
            return None     # bad password

        # valid user & password
        return usr

    # end login
        
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #                   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #   read methods    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #                   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def findAll(self):
        with conn.cursor() as cur:
            sql = """
                    select
                            userid,
                            username,
                            useremail,
                            userdescription
                        from
                            users
                """
            cur.execute(sql)
            users = []
            for usr in cur.fetchall():
                users.append(User(usr[0], usr[1], "", usr[2], usr[3]))
            return users

        # end with conn.cursor()
    # end findAll

    def findOne(self, id: int):
        # id: userid
        with conn.cursor() as cur:
            sql = """
                    select
                            userid,
                            username,
                            useremail,
                            userdescription
                        from
                            users
                        where
                            userid = %s
                """
            cur.execute(sql, (id,))
            usr = cur.fetchone()
            if cur.rowcount != 1:   # not found
                return None

            # found
            user = User(usr[0], usr[1], "", usr[2], usr[3])
            #user.roles = 
            return user

        # end with conn.cursor()
    # end findOne

    def findOneBy(self, **kwargs):
        # kwargs: list of fieldname / fieldvalue
        with conn.cursor() as cur:
            sql  = """
                    select
                            userid,
                            username,
                            userpassword,
                            useremail,
                            userdescription
                        from
                            users
                """
            whr  = ""
            args = []
            for key, val in kwargs.items():
                whr  = " where " if whr == "" else " and "
                whr += f"({key} = %s)"
                args.append(val)
            
            sql += whr
            cur.execute(sql, args)
            usr = cur.fetchone()
            if cur.rowcount != 1:   # not found
                return None

            # found
            return User(usr[0], usr[1], usr[2], usr[3], usr[4])

        # end with conn.cursor()
    # end findOneBy

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #                   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #   write methods   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #                   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def insert(self, usr: User):
        # usr: full user object
        with conn.cursor() as cur:
            # prepare password
            pwd    = usr.userpassword.encode("utf-8")
            mySalt = bcrypt.gensalt()
            hash   = bcrypt.hashpw(pwd, mySalt).encode("utf-8")

            sql = """
                    insert
                        into
                            users
                        (
                            username,
                            userpassword,
                            useremail,
                            userdescription
                        ) values (
                            %s,
                            %s,
                            %s,
                            %s
                        )
                        returning
                            userid
                """

            try:
                cur.execute(usr.username, hash, usr.useremail, usr.userdescription)
                usr.userid = cur.fetchone()[0]  # get userid generated by insert
                conn.commit()

            except Exception as e:
                print(e, file=sys.stderr)
                conn.rollback()
                return None

            return usr

        # end with conn.cursor() as cur:
    # end insert

    def update(self, id, uuf: UserUpdateForm):
        # id : userid
        # uuf: data from update form
        usr = self.findOne(id)
        if usr == None:     # not found
            return None

        # usr populated with field already filled in DB, at least userid
        usr = uuf.getAsUser(usr) # get other fields from form
        with conn.cursor() as cur:
            sql = """
                    update
                            users
                        set (
                            useremail,
                            userdescription
                        ) values (
                            %s,
                            %s
                        )
                        where
                            userid = %s
                """
            try:
                cur.execute(usr.useremail, usr.userdescription, usr.userid)
            except Exception() as e:
                print(e, file=stderr)
                conn.rollback
                return None

            # update to role ?
            if uuf.isAdmin.data:
                self.userRoleService.addRoleToUser(2, usr)
            elif "ADMIN" in usr.roles:
                self.userRoleService.remRoleOfUser(2, usr)
            else:
                conn.commit()

            if (id == session.get("userid")):
                usr.roles = self.userRoleService.listUserRoles(usr)
                session["userroles"] = usr.roles

            return usr

        # end with conn.cursor() as cur:
    # end update

    def delete(self, id):
        # id: userid
        with conn.cursor() as cur:
            sql = """
                    delete
                        from
                            %s
                        where
                            userid = %s
                """
            try:
                cur.execute(sql, ("roleuser", id))
                cur.execute(sql, ("users"   , id))
                conn.commit()
            except Exception() as e:
                conn.rollback()
                print(e, file=stderr)
                return None

        # end with conn.cursor() as cur:
    # end delete
