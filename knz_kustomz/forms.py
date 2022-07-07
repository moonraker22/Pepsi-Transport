from flask_wtf import FlaskForm

from wtforms import (
    SelectField,
    DateTimeField,
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    DecimalField,
    IntegerField,
)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from knz_kustomz.models import User


class RegistrationForm(FlaskForm):
    """Registration form"""

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Email is required"),
            Email(message="Please enter an email address"),
        ],
        render_kw={
            "placeholder": "Email",
            "id": "email",
            "style": "margin-bottom:3vh;",
        },
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=2, max=20)],
        render_kw={"placeholder": "Password", "style": "margin-bottom:3vh;"},
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password"), Length(min=2, max=20)],
        render_kw={"placeholder": "Confirm Password", "style": "margin-bottom:1vh;"},
    )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "There's already a user with that email. Please sign in or reset your password"
            )


class LoginForm(FlaskForm):
    """Login form"""

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Email is required"),
            Email(message="Please enter an email address"),
        ],
        render_kw={
            "placeholder": "Email",
            "id": "email",
            "style": "margin-bottom:3vh;",
        },
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(message="Password is required")],
        render_kw={"placeholder": "Password", "style": "margin-bottom:3vh;"},
    )
    remember = BooleanField("Remember Me")


class PaysheetsForm(FlaskForm):
    """Form for paysheets"""

    date = DateTimeField(
        "Date",
        format="%b %d, %Y",
        validators=[DataRequired(message="Date is required")],
        render_kw={"placeholder": "Choose Date"},
    )
    truck = StringField("Truck Number", render_kw={"placeholder": "Truck Number"})
    starting_milage = IntegerField(
        "Starting Milage", render_kw={"placeholder": "Starting Milage"}
    )
    ending_milage = IntegerField(
        "Ending Milage", render_kw={"placeholder": "Ending Milage"}
    )
    miles = IntegerField("Miles", render_kw={"placeholder": "Total Miles"})
    backhaul = DecimalField("Backhaul", render_kw={"placeholder": "Backhaul"})
    delay = DecimalField("Delay", render_kw={"placeholder": "Delay(Hrs)"})
    save = SubmitField(label="Save", render_kw={"type": "submit"})


class LocationsForm(FlaskForm):
    """Locations form"""

    locations = SelectField(u"Location")
    submit = SubmitField(label="Submit", render_kw={"type": "submit"})


class UpdateAccountForm(FlaskForm):
    """Update email form"""

    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Update")


def validate_email(self, email):
    if email.data != current_user.email:
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "There's already a user with that email. Please sign in or reset your password"
            )


class RequestResetForm(FlaskForm):
    """Reset password form"""

    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                "There is no account with that email. You must register first."
            )


class ResetPasswordForm(FlaskForm):
    """Reset password form"""

    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Reset Password")
