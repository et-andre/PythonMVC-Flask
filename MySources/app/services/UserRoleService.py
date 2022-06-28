import sys

from app                            import conn

from app.models.Role                import Role
from app.models.User                import User

from app.decorators.authRequired    import authRequired

class UserRoleService:
    def listUserRoles(self, user: User):
        # user: full user record
        with conn.cursor() as cur:
            sql = """
                    select
                            r.roleid,
                            r.rolename
                        from
                            role     r,
                            roleuser ru
                        where
                            (r.roleid  = ru.roleid) and
                            (ru.userid = %s)
                """
            cur.execute(sql, (user.userid,))

            roles = []
            for row in cur.fetchall():
                roles.append(str(row[1]))   # index 1 = field 2 = rolename
            user.roles = roles

            return roles

        # end with conn.cursor() as cur
    # end listUserRoles

    def userHasRole(self, id, user: User):
        # id  : role id
        # user: full user record
        with conn.cursor() as cur:
            sql = """
                    select
                            count(*)
                        from
                            roleuser
                        where
                            (roleid = %s) and
                            (userid = %s)
                """
            cur.execute(sql, (id, user.userid))

            return (cur.rowcount == 1)

        # end with conn.cursor() as cur
    # end userHasRole

    @authRequired(role="ADMIN") # method can olny be called by a user with role ADMIN
    def addRoleToUser(self, id, user: User):
        # id  : role id
        # user: full user record
        if self.userHasRole(id, user):
            return True

        with conn.cursor() as cur:
            sql = """
                    insert
                        into
                            roleuser
                        (
                            roleid,
                            userid
                        )
                        values
                        (
                            %s,
                            %s
                        )
                """
            try:
                cur.execute(sql, (id, user.userid))
                conn.commit()
                return True
            except Exception as e:
                print(e, file=sys.stderr)
                conn.rollback()
                return False

        # end with
    # end addRoleToUser

    @authRequired(role="ADMIN") # method can olny be called by a user with role ADMIN
    def remRoleOfUser(self, id, user: User):
        # id  : role id
        # user: full user record
        if not self.userHasRole(id, user):  # not this role for this user: nothing to do, it's done !
            return True

        if id == 1:                         # cannot remove role 1 (user): forbidden
            return False

        with conn.cursor() as cur:
            sql = """
                    delete
                        from
                            roleuser
                        where
                            (roleid = %s) and
                            (userid = %s)
                """
            try:
                cur.execute(sql, (id, user.userid))
                conn.commit()
                return True
            except Exception as e:
                print(e, file=sys.stderr)
                conn.rollback()
                return False

        # end with
    # end remRoleOfUser
