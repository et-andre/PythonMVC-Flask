from sys        import stderr
from functools  import wraps
from flask      import redirect, session, url_for

def authRequired(role="USER", sameUserSessionArgs=False):
    def authRequiredDecorator(func):
        @wraps(func)
        def functionWrapper(*args, **kwargs):
            # 1. ok si le user a des données dans la session, et s'il a le rôle passé en paramètre
            if session.get("userroles") and (role in session.get("userroles")):
                return func(*args, **kwargs)

            # 2. le user n'a pas le bon rôle, mais peut travailler sur lui-même: il doit être passé en paramètre et correspondre au user de la session
            if sameUserSessionArgs and session.get("userid") and (session["userid"] == kwargs["userid"]):
                return func(*args, **kwargs)

            # 3. ni l'un, ni l'autre: pas autorisé
            return redirect(url_for("index"))

        # end functionWrapper

        return functionWrapper

    # end authRequiredDecorator

    return authRequiredDecorator
