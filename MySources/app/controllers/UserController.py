from sys                            import stderr

from flask                          import redirect, render_template, request, session, url_for

from app                            import app

from app.decorators.authRequired    import authRequired

from app.services.UserService       import UserService

from app.forms.UserLoginForm        import UserLoginForm
from app.forms.UserRegisterForm     import UserRegisterForm
from app.forms.UserUpdateForm       import UserUpdateForm

userService = UserService()

class UserController:
    @app.route('/users', methods=["GET"])
    def getUserList():
        users = userService.findAll()

        return render_template('users/list.html', users=users)

    @app.route('/users/<int:userid>', methods=["GET"])
    def getOneUser(id: int):
        usr = userService.findOne(id)

        return render_template('users/profile.html', user=usr)

    @app.route('/users/register', methods=["GET", "POST"])
    def register():
        frm = UserRegisterForm(request.form)

        if request.method == 'POST':
            if frm.validate():
                usr = userService.insert(frm.getAsUser())

                return redirect(url_for('getOneUser', userid = usr.userid))

        return render_template('users/register.html', form=frm)

    @app.route('/users/update/<int:userid>', methods=["GET", "POST"])
    @authRequired(level='ADMIN', sameUserSessionArgs=True)
    def userUpdate(id: int):
        frm = UserUpdateForm(request.form)
        
        # sessionUserId = session.get('userid')
        # if sessionUserId == None or sessionUserId != id:
        #     return redirect(url_for('index'))

        if request.method == 'POST':
            if frm.validate():
                usr = userService.update(id, frm)

                return redirect(url_for('getOneUser', userid = id))

        usr = userService.findOne(id)
        return render_template('users/update.html', form=frm, user=usr)

    @app.route('/login', methods=["GET", "POST"])
    def login():
        frm = UserLoginForm(request.form)

        if request.method == 'POST':
            if frm.validate():
                usr = userService.login(frm.getAsUser())

                if usr != None:
                    session['username'] = usr.username
                    session['userid'  ] = usr.userid
                    return redirect(url_for('getOneUser', userid = usr.userid))

                err = {}
                err['authentication'] = 'Wrong user or password!'

                return render_template('users/login.html', frm=form, errors=err)

        return render_template('users/login.html', form=frm, errors=frm.err)

    @app.route('/logout', methods=["GET"])
    def logout():
        session.pop('userid'  , None)
        session.pop('username', None)
        return redirect(url_for('index'))

    @app.route('/profile', methods=["GET"])
    def profile():
        id = session.get('userid')
        if id != None:
            return redirect(url_for('getOneUser', userid = id))
        else:
            return redirect(url_for('index'))
