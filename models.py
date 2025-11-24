from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    address_display = db.Column(db.String(300))
    map_url = db.Column(db.String(500))
    checkin_time = db.Column(db.String(20))
    checkout_time = db.Column(db.String(20))
    wifi_ssid = db.Column(db.String(120))
    wifi_password = db.Column(db.String(120))
    parking = db.Column(db.Text)
    quiet_hours = db.Column(db.String(50))
    notes = db.Column(db.Text)
    hero_url = db.Column(db.String(800))
    gallery_urls = db.Column(db.Text)
    instagram_url = db.Column(db.String(300))
    facebook_url  = db.Column(db.String(300))
    tiktok_url    = db.Column(db.String(300))
    whatsapp_url  = db.Column(db.String(300))
    phone_number  = db.Column(db.String(60))
    email_address = db.Column(db.String(120))

    contacts = db.relationship("Contact", backref="property", cascade="all, delete-orphan")
    rules = db.relationship("Rule", backref="property", cascade="all, delete-orphan")
    howtos = db.relationship("HowTo", backref="property", cascade="all, delete-orphan")
    issues = db.relationship("IssueFlow", backref="property", cascade="all, delete-orphan")
    emergencies = db.relationship("Emergency", backref="property", cascade="all, delete-orphan")
    locals = db.relationship("LocalPlace", backref="property", cascade="all, delete-orphan")
    checkin_steps = db.relationship("CheckinStep", backref="property", cascade="all, delete-orphan")
    checkout_steps = db.relationship("CheckoutStep", backref="property", cascade="all, delete-orphan")
    faqs = db.relationship("FAQ", backref="property", cascade="all, delete-orphan")
    messages = db.relationship("Message", backref="property", cascade="all, delete-orphan")
    views = db.relationship("PageView", backref="property", cascade="all, delete-orphan")

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50))
    name = db.Column(db.String(120))
    phone = db.Column(db.String(60))
    whatsapp = db.Column(db.String(60))
    prop_id = db.Column(db.Integer, db.ForeignKey("property.id"))

class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    penalty = db.Column(db.String(120))
    rationale = db.Column(db.Text)
    prop_id = db.Column(db.Integer, db.ForeignKey("property.id"))

class HowTo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.String(120))
    appliance = db.Column(db.String(120))
    brand_model = db.Column(db.String(120))
    how = db.Column(db.Text)
    manual_url = db.Column(db.String(500))
    issues = db.Column(db.Text)
    prop_id = db.Column(db.Integer, db.ForeignKey("property.id"))

class IssueFlow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(120))
    try_first = db.Column(db.Text)
    when_to_contact = db.Column(db.Text)
    info_needed = db.Column(db.Text)
    auto_reply = db.Column(db.Text)
    prop_id = db.Column(db.Integer, db.ForeignKey("property.id"))

class Emergency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    etype = db.Column(db.String(50))
    name = db.Column(db.String(120))
    phone = db.Column(db.String(60))
    when = db.Column(db.Text)
    address = db.Column(db.String(300))
    notes = db.Column(db.Text)
    prop_id = db.Column(db.Integer, db.ForeignKey("property.id"))

class LocalPlace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))
    name = db.Column(db.String(200))
    blurb = db.Column(db.Text)
    address = db.Column(db.String(300))
    map_link = db.Column(db.String(500))
    hours = db.Column(db.String(120))
    link = db.Column(db.String(500))
    price = db.Column(db.String(10))
    prop_id = db.Column(db.Integer, db.ForeignKey("property.id"))

class CheckinStep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    step = db.Column(db.Integer)
    title = db.Column(db.String(200))
    body = db.Column(db.Text)
    image = db.Column(db.String(200))
    video = db.Column(db.String(200))
    tip = db.Column(db.Text)
    prop_id = db.Column(db.Integer, db.ForeignKey("property.id"))

class CheckoutStep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    step = db.Column(db.Integer)
    title = db.Column(db.String(200))
    body = db.Column(db.Text)
    notes = db.Column(db.Text)
    prop_id = db.Column(db.Integer, db.ForeignKey("property.id"))

class FAQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    q = db.Column(db.String(300))
    a = db.Column(db.Text)
    related = db.Column(db.String(200))
    prop_id = db.Column(db.Integer, db.ForeignKey("property.id"))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey("property.id"))
    name = db.Column(db.String(120))
    contact = db.Column(db.String(120))
    category = db.Column(db.String(80))
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PageView(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey("property.id"))
    section = db.Column(db.String(40))
    user_agent = db.Column(db.String(300))
    ip = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def seed(db):
    if Property.query.first():
        return
    p = Property(
        slug="kensington-suite-a",
        name="Kensington Suite A",
        address_display="Flat 3, 12 Example St, London W8 5AA",
        map_url="https://maps.google.com/?q=Flat+3+12+Example+St+London",
        checkin_time="15:00",
        checkout_time="11:00",
        wifi_ssid="Empires_Guest",
        wifi_password="London2025!",
        parking="Residents bay 14; permit in hallway drawer",
        quiet_hours="22:00–08:00",
        notes="Elevator key in lockbox B",
        hero_url="https://images.unsplash.com/photo-1505692794403-34d4982b1e54?q=80&w=2000&auto=format&fit=crop",
        gallery_urls=",".join([
            "https://images.unsplash.com/photo-1493809842364-78817add7ffb?q=80&w=1400&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1505691938895-1758d7feb511?q=80&w=1400&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1519710164239-da123dc03ef4?q=80&w=1400&auto=format&fit=crop"
        ]),
        instagram_url="https://instagram.com/yourbrand",
        facebook_url="https://facebook.com/yourbrand",
        tiktok_url="https://www.tiktok.com/@yourbrand",
        whatsapp_url="https://wa.me/447911123456",
        phone_number="+44 7xxx xxx xxx",
        email_address="hello@example.com",
    )
    db.session.add(p); db.session.commit()
