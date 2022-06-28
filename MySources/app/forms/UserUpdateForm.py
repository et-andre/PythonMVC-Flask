from flask_wtf          import FlaskForm

from wtforms            import StringField, EmailField, BooleanField
from wtforms.validators import DataRequired, EqualTo

from app.models.User    import User

class UserUpdateForm(FlaskForm):
    useremail       = StringField ("useremail"      , validators=[DataRequired()])
    userdescription = StringField ("userdescription", validators=[DataRequired()])
    isAdmin         = BooleanField("isAdmin"        , validators=[]              )

    # update objet User, with fields filled from form
    def getAsUser(self, usr: User) -> User:
        # usr: fulluser object
        usr.useremail       = self.usseremail.data
        usr.userdescription = self.userdescription.data
    
        return usr
