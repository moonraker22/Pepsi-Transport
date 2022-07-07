from knz_kustomz import app, db, LoginManager, login_manager, SQLAlchemy
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    """User database model."""

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)
    paysheets = db.relationship("Paysheets", backref="paysheets", lazy=True)

    @staticmethod
    def get_user(email: str):
        """Returns the User object"""
        user = User.query.filter_by(email=email).first()
        return user

    def __repr__(self) -> str:
        return f"User({self.email}, {self.id})"


class Locations(db.Model):
    """Locations database model"""

    __tablename__ = "locations"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255))
    latitude = db.Column(db.String(100))
    longitude = db.Column(db.String(100))
    waypoints = db.Column(db.String(255))
    place_id = db.Column(db.String(255))
    description = db.Column(db.Text())

    # def __init__(self, address, place_id, latitude='', longitude='', waypoints=None, **kwargs):
    #     super(Locations, self).__init__(**kwargs)
    #     self.address = address
    #     self.latitude = latitude
    #     self.longitude = longitude
    #     self.waypoints = waypoints
    #     self.place_id = place_id

    def __repr__(self) -> str:
        return f"Locations({self.name}, {self.address}, {self.latitude}, {self.longitude}, {self.waypoints}, {self.place_id})"


class Paysheets(db.Model):
    __tablename__ = "paysheets"
    # __table_args__ = {'schema':'db'}
    id = db.Column(db.Integer(), primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(
        db.Integer(),
        db.ForeignKey("user.id"),
        nullable=False,
    )
    date = db.Column(db.DateTime, unique=True, nullable=False)
    starting_milage = db.Column(db.Integer())
    ending_milage = db.Column(db.Integer())
    total_miles = db.Column(db.Integer())
    backhaul = db.Column(db.Float())
    truck = db.Column(db.String(20))
    delay = db.Column(db.Float())

    def __repr__(self) -> str:
        return f"Paysheets({self.user_id}, {self.date}, {self.starting_milage}, {self.ending_milage}, {self.total_miles}, {self.backhaul}, {self.truck}"


def init_db():
    """Initialize the database"""
    db.drop_all()
    db.create_all()

    # Create test user
    user = User(email="test@gmail.com", password="test")
    db.session.add(user)
    db.session.commit()

    # Create Locations in the database
    tulsa = Locations(
        name="Tulsa",
        address="510 W Skelly Dr, Tulsa, OK 74107, USA",
        place_id="ChIJpVol8ZaUtocROzFr1q9XYzU",
        description="Tulsa Pepsi",
    )
    mesquite = Locations(
        name="Mesquite",
        address="4532 I-30, Mesquite, TX 75150, USA",
        place_id="ChIJEWjrVvijToYRmsfTETRwuR0",
        description="Enter left side of the gate and check in",
    )
    oklahoma_city = Locations(
        name="Oklahoma City",
        address="14501 N Kelley Ave, Oklahoma City, OK 73114",
        place_id="ChIJqb2od-sesocRwHV01tgB8Yw",
        description="Enter through the gate, has employee badge scan in. Trailer drop spots at the end on the left and bills go in mailbox by the door near the docks",
    )
    enid = Locations(
        name="Enid",
        address="5801 E Owen K Garriott Rd, Enid, OK 73701",
        place_id="ChIJB32ZJXjVr4cRJmo0H-DxV6w",
        description="Turn at Mack dealership and go right to Pepsi. Gate code is 0914#. Drop loaded trailers inside fence",
    )
    ft_smith = Locations(
        name="Ft Smith",
        address="3701 Zero St, Fort Smith, AR 72908",
        place_id="ChIJcUeJG7Syy4cREey8j1zcFRI",
        description="Employee badge scan in at gate. Drop trailers on the left and bills go in mailbox by the door on the left of the 3 dock doors to the left",
    )
    lawton = Locations(
        name="Lawton",
        address="209 SE Simpson St, Lawton, OK 73501",
        place_id="ChIJxddOOcUYrYcRgUWMnZHBmX4",
        description="Circle around to front by docks. Drop on concrete pad towards the end of building",
    )
    coffeyville = Locations(
        name="Coffeyville",
        address="2406 US-169, Coffeyville, KS 67337",
        place_id="ChIJ24bZQuiEt4cRtoAkHMqBTtQ",
        description="Unlock gate with key and drop in the dock",
    )
    wichita = Locations(
        name="Wichita",
        address="5005-5099 S Water St, Wichita, KS 67216",
        place_id="ChIJn6C5MMLluocRrL_-5gFvkPs",
        description="Pull in right side of gate and check in",
    )
    harrison = Locations(
        name="Harrison",
        address="229 Industrial Park Rd, Harrison, AR 72601",
        place_id="ChIJzQeCAhz1zocRt8bXx05lV-A",
        description="Gate code is 65591#. Drop trailer on right with legs on the pavement. Put bills in back or light box of trailer",
    )
    sprinfield = Locations(
        name="Sprinfield",
        address="2200 E Turner St, Springfield, MO 65803",
        place_id="ChIJV098YiZiz4cRh4m6vuYxEAQ",
        description="Gate code is 2890#. Put bills in mailbox by the dock doors on left. Drop trailer in back of warehouse.",
    )
    joplin = Locations(
        name="Joplin",
        address="7911 E 24th St, Joplin, MO 64804",
        place_id="ChIJKdMHFJp8yIcRubrTjJBzKQg",
        description="Gate has employee badge scan in. Check in with warehouse personell",
    )
    springfield_buske = Locations(
        name="Springfield Buske",
        address="1904 Le Compte Rd, Springfield, MO 65802",
        place_id="ChIJs__jUaJ9z4cRgT4jLpmGod8",
        description="Check in for live load is off Le Compte rd on east side. Drop lot is off Le Compte rd on west side.",
    )
    plastipak = Locations(
        name="Plastipak",
        address="3200 W Kingsley Rd #100, Garland, TX 75041",
        place_id="ChIJS_0-XcegToYRThGVkItJZLE",
        description="Check in at office on the south side of the building in the middle",
    )
    plastipak_dunnage = Locations(
        name="Plastipak Dunnage",
        address="3201 Miller Park N, Garland, TX 75042",
        place_id="ChIJVwpKExseTIYRvupc_hzaS8s",
        description="Unload in docks 26-29. Check in in office by dock 1. Facility is not the one on north side of miller. It's on the south side past International Rd.",
    )
    wichita_falls = Locations(
        name="Wichita Falls",
        address="1100 7th St, Wichita Falls, TX 76301",
        place_id="ChIJXYbjQ48gU4YR8vYUWQv9Zfw",
        description="Gate code is 2623#. Drop on west side and put metal pads under legs of trailer. Bills go in mailbox by door next to docks",
    )
    hugo = Locations(
        name="Hugo",
        address="200 Pepsi Cola Ave, Hugo, OK 74743",
        place_id="ChIJW6Juh8jpSoYR3j0i5mvoMw4",
        description="",
    )
    ada = Locations(
        name="Ada",
        address="3801 N Broadway Ave, Ada, OK 74820",
        place_id="ChIJdXUXRzNss4cR_kR-KT9jNII",
        description="Gate needs clicker to open. Drop in back and put bills in mailbox by dock doors",
    )
    olathe = Locations(
        name="Olathe",
        address="1775 E Kansas City Rd, Olathe, KS 66061",
        place_id="ChIJ-zI9xIyVwIcR6eWvuJdgUqQ",
        description="Gate code is 0914#. Drop on backside of the building and put bills in the mailbox by the dock doors",
    )
    kansas_city = Locations(
        name="Kansas City",
        address="6050 Manchester Trafficway, Kansas City, MO 64130",
        place_id="ChIJlSwJTK7lwIcR6mGcORnPpM4",
        description="Need badge to get to drop yard behind warehouse",
    )
    edgerton = Locations(
        name="Edgerton",
        address="30901 W 185th St Entrance is off of, Waverly Rd, Gardner, KS 66030",
        place_id="ChIJ02OvZ-GlwIcRKBfVpVm8SD8",
        description="Drop where guard tells you and office is in the middle of building on entrance side",
    )
    lancaster = Locations(
        name="Lancaster",
        address="1201 Danieldale Rd, Lancaster, TX 75134",
        place_id="ChIJ56nWEFeXToYRiK8F2gMXw0k",
        description="Drive through gate and check in at shipping office in middle of the building. Must check out at the gate",
    )

    # sprinfield = Locations(
    #     name = "Sprinfield",
    #     address = "",
    #     place_id = "",
    #     description = ""
    # )
    db.session.add(lancaster)
    db.session.add(kansas_city)
    db.session.add(edgerton)
    db.session.add(ada)
    db.session.add(olathe)
    db.session.add(wichita_falls)
    db.session.add(hugo)
    db.session.add(plastipak_dunnage)
    db.session.add(plastipak)
    db.session.add(springfield_buske)
    db.session.add(joplin)
    db.session.add(sprinfield)
    db.session.add(harrison)
    db.session.add(wichita)
    db.session.add(coffeyville)
    db.session.add(lawton)
    db.session.add(enid)
    db.session.add(ft_smith)
    db.session.add(mesquite)
    db.session.add(tulsa)
    db.session.add(oklahoma_city)
    db.session.commit()

    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User, Paysheets=Paysheets, Locations=Locations)

    if __name__ == "__main__":
        init_db()
