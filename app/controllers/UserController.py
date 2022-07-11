from sys import stderr
from flask import redirect, render_template, request, session, url_for
from app import app
from app.decorators.authRequired import authRequired
from app.forms.UserLoginForm import UserLoginForm
from app.services.UserService import UserService
from app.forms.UserRegisterForm import UserRegisterForm
from app.forms.UserUpdateForm import UserUpdateForm

userService = UserService()

class UserController:
    @app.route('/users', methods=["GET"])
    def getUserList():
        users = userService.findAll()

        return render_template('users/list.html', users=users)

    @app.route('/users/<int:userid>', methods=["GET"])
    def getOneUser(userid: int):
        user = userService.findOne(userid)

        return render_template('users/profile.html', user=user)

    @app.route('/users/test', methods=["GET"])
    def getTestUser():
        user = userService.findOneBy(username='admin')

        return render_template('users/profile.html', user=user)
#
#     @app.route('/users/register', methods=["GET", "POST"])
#     def register():
#         form = UserRegisterForm(request.form)
#
#         if request.method == 'POST':
#             if form.validate():
#                 user = userService.insert(form.getAsUser())
#
#                 return redirect(url_for('getOneUser', userid = user.userid))
#
#         return render_template('users/register.html', form=form)
#
#     @app.route('/users/update/<int:userid>', methods=["GET", "POST"])
#     @authRequired(level='ADMIN', orIsCurrentUser=True)
#     def userUpdate(userid: int):
#         form = UserUpdateForm(request.form)
#
#         # sessionUserId = session.get('userid')
#         # if sessionUserId == None or sessionUserId != userid:
#         #     return redirect(url_for('index'))
#
#         if request.method == 'POST':
#             if form.validate():
#                 user = userService.update(userid, form)
#
#                 return redirect(url_for('getOneUser', userid = userid))
#
#         user = userService.findOne(userid)
#         return render_template('users/update.html', form=form, user=user)
#
#     @app.route('/login', methods=["GET", "POST"])
#     def login():
#         form = UserLoginForm(request.form)
#
#         if request.method == 'POST':
#             if form.validate():
#                 user = userService.login(form.getAsUser())
#
#                 if user != None:
#                     session['username'] = user.username
#                     session['userid'] = user.userid
#                     return redirect(url_for('getOneUser', userid = user.userid))
#
#                 errors = {}
#                 errors['authentication'] = 'Wrong user or password!'
#
#                 return render_template('users/login.html', form=form, errors=errors)
#
#         return render_template('users/login.html', form=form, errors=form.errors)
#
#     @app.route('/logout', methods=["GET"])
#     def logout():
#         session.pop('userid', None)
#         session.pop('username', None)
#         return redirect(url_for('index'))
#
#     @app.route('/profile', methods=["GET"])
#     def profile():
#         userid = session.get('userid')
#         if userid != None:
#             return redirect(url_for('getOneUser', userid = userid))
#         else:
#             return redirect(url_for('index'))