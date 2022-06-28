from flask_wtf          import FlaskForm

from wtforms            import StringField
from wtforms.validators import DataRequired

from app.models.User    import User

class UserLoginForm(FlaskForm):
    username     = StringField("username"    , validators=[DataRequired()])
    userpassword = StringField("userpassword", validators=[DataRequired()])

    # create objet User, with 2 fields filled from form
    def getAsUser(self) -> User:
        return User(0, self.username.data, self.userpassword.data, "", "")
