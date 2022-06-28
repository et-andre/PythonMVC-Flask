from flask  import redirect, render_template, request, url_for

from app    import app

class UserController:
    @app.route('/', methods=["GET"])
    def index():
        return render_template('home/home.html')
