from sys import stderr

from flask import session
from app.forms.UserUpdateForm import UserUpdateForm
from app.models.User import User
from app.services.IService import IService
from app import db
import bcrypt

class UserService():
    # def login(self, user: User):
    #     toLogin = self.findOneBy(username=user.username)
    #
    #     if toLogin != None and bcrypt.checkpw(user.userpassword.encode('utf-8'), toLogin.userpassword.encode('utf-8')):
    #         return toLogin
    #
    #     return None

    def findAll(self):
        return User.query.all()

    def findOne(self, dataId: int):
        return User.query.get(dataId)

    def findOneBy(self, **kwargs):
        return User.query.filter_by(**kwargs).first()

    def insert(self, data: User):
        db.session.add(data)
        db.session.commit()
#
#     def update(self, dataId: int, data: UserUpdateForm):
#         user = self.findOne(dataId)
#
#         if user == None:
#             return None
#
#         user = data.getAsUser(user)
#
#         with conn.cursor() as cur:
#             try:
#                 cur.execute("UPDATE users SET useremail = %s, userdescription = %s WHERE userid = %s",
#                     (user.useremail, user.userdescription, dataId))
#
#                 if data.isAdmin.data:
#                     self.userRoleService.linkRoleToUser(2, user)
#                 elif "ADMIN" in user.roles:
#                     self.userRoleService.unlinkRoleToUser(2, user)
#
#                 print(dataId, file=stderr)
#                 print(session.get('userid'), file=stderr)
#                 if dataId == session.get('userid'):
#                     roles = self.userRoleService.findUserRoles(user)
#                     print(roles, file=stderr)
#                     session['userroles'] = roles
#                     user.roles = roles
#
#                 conn.commit()
#
#                 return user
#             except Exception as e:
#                 print(e, file=stderr)
#                 conn.rollback()
#
#             return None
#
#     def delete(self, dataId: int):
#         with conn.cursor() as cur:
#             try:
#                 cur.execute("DELETE FROM userroles WHERE userid = %s", (dataId,))
#                 cur.execute("DELETE FROM users WHERE userid = %s",
#                     (dataId,))
#                 conn.commit()
#
#                 return dataId
#             except Exception as e:
#                 print(e, file=stderr)
#                 conn.rollback()
#
#             return None