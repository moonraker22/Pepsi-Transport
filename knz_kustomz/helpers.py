from werkzeug.security import generate_password_hash

from knz_kustomz.models import Locations, User, db


def add_location(
    name, address="", place_id="", latitude="", longitude="", waypoints=""
):
    """Adds a location to the database"""
    location = Locations(
        name=name,
        address=address,
        place_id=place_id,
        latitude=latitude,
        longitude=longitude,
        waypoints=waypoints,
    )
    db.session.add(location)
    db.session.commit()


def get_location(name: str):
    """Returns location object"""
    return Locations.query.filter_by(name=name).first()


def create_user(email, password) -> None:
    """Creates a new user in the database"""
    hashed_password = generate_password_hash(password)
    user = User(email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


# def get_user(email: str) -> User:
#     """Returns the User object"""
#     return User.query.filter_by(email=email).first()
