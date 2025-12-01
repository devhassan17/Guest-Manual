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
    # Seed a single property for "Vibe: A Modern Rustic Apartment"
    if Property.query.first():
        return

    # Core property info
    p = Property(
        slug="vibe-modern-rustic-apartment",
        name="Vibe: A Modern Rustic Apartment",
        address_display="330 Upper Street, N1 2XQ, London, United Kingdom",
        map_url="https://maps.google.com/?q=330+Upper+Street+N1+2XQ+London",
        checkin_time="16:00",
        checkout_time="11:00",
        wifi_ssid="VibeFI",
        wifi_password="w3L0V3V!Be!_",
        parking="Parking options can be found on justpark.com.",
        quiet_hours="22:00–08:00",
        notes=(
            "Welcome to Vibe – a cozy, modern rustic studio with a mezzanine bed, "
            "convertible sofa bed, kitchenette, fast Wi-Fi, and a comfy space to relax or work. "
            "You are perfectly located on Upper Street in Angel & Islington, surrounded by cafés, "
            "restaurants, nightlife, and quick links to central London."
        ),
        hero_url=(
            "https://a0.muscache.com/im/pictures/hosting/"
            "Hosting-U3RheVN1cHBseUxpc3Rpbmc6MTI5ODQ1NDMxNDU3NzQ2ODgwMw%3D%3D/"
            "original/b80518ff-c448-49ed-bee1-397aad3288c7.jpeg?im_w=1200"
        ),
        gallery_urls=",".join([
            "https://a0.muscache.com/im/pictures/hosting/"
            "Hosting-U3RheVN1cHBseUxpc3Rpbmc6MTI5ODQ1NDMxNDU3NzQ2ODgwMw%3D%3D/"
            "original/b80518ff-c448-49ed-bee1-397aad3288c7.jpeg?im_w=1200",
            "https://a0.muscache.com/im/pictures/hosting/"
            "Hosting-U3RheVN1cHBseUxpc3Rpbmc6MTI5ODQ1NDMxNDU3NzQ2ODgwMw%3D%3D/"
            "original/6c07b7b9-8d71-45f3-a9c8-2bc0e9a80b4a.jpeg?im_w=1200",
            "https://a0.muscache.com/im/pictures/hosting/"
            "Hosting-U3RheVN1cHBseUxpc3Rpbmc6MTI5ODQ1NDMxNDU3NzQ2ODgwMw%3D%3D/"
            "original/541f1f35-19a9-4414-b4e7-2bd6564dd94a.jpeg?im_w=1200",
        ]),
        instagram_url="https://www.instagram.com/empiresproperty_/",
        facebook_url="",
        tiktok_url="",
        whatsapp_url="+447592249258",
        phone_number="+44 7592 249258",
        email_address="enquiries@empiresproperty.com",
    )
    db.session.add(p)
    db.session.commit()

    # ------- Contacts -------
    guest_support = Contact(
        role="Guest support (WhatsApp)",
        name="Guest Support",
        phone="+447592249258",
        whatsapp="+447592249258",
        prop_id=p.id,
    )
    db.session.add(guest_support)

    # ------- Rules -------
    rules = [
        Rule(
            title="No smoking",
            description="Smoking or vaping is not allowed anywhere inside the apartment or building.",
            penalty="Additional cleaning fee and possible loss of deposit.",
            rationale="Smoke damage and odours are difficult and costly to remove for the next guests.",
            prop_id=p.id,
        ),
        Rule(
            title="No parties or events",
            description="Parties, events, or loud gatherings are not permitted.",
            penalty="Immediate cancellation of the stay and potential fines from the building.",
            rationale="This is a residential building and we must respect neighbours and building rules.",
            prop_id=p.id,
        ),
        Rule(
            title="Respect quiet hours",
            description="Please keep noise to a minimum between 22:00 and 08:00.",
            penalty="Complaints from neighbours may lead to termination of the stay.",
            rationale="Sound travels easily in the building and we want to maintain good relationships with neighbours.",
            prop_id=p.id,
        ),
        Rule(
            title="No extra overnight guests",
            description="Only the guests on the booking are allowed to stay overnight.",
            penalty="Additional charges or termination of the stay.",
            rationale="This is for safety, insurance and building regulations.",
            prop_id=p.id,
        ),
        Rule(
            title="Take care of keys and codes",
            description="Do not share access codes with anyone outside your group.",
            penalty="Replacement charges if locks or codes must be changed.",
            rationale="To keep you, future guests and the property secure.",
            prop_id=p.id,
        ),
    ]
    db.session.add_all(rules)

    # ------- How‑tos (appliances & in‑flat info) -------
    howto_wifi = HowTo(
        area="Whole flat",
        appliance="Wi-Fi",
        brand_model="",
        how=(
            "To connect, select the Wi-Fi network 'VibeFI' and enter the password 'w3L0V3V!Be!_'. "
            "You can use this on all of your devices during your stay."
        ),
        manual_url="",
        issues=(
            "If you have any issues connecting, try restarting your device and the router if accessible. "
            "Then contact guest support on WhatsApp if it still does not work."
        ),
        prop_id=p.id,
    )

    howto_tv = HowTo(
        area="Living room",
        appliance="TV & Netflix",
        brand_model="Streaming device preconfigured with Netflix",
        how=(
            "The TV is hooked up to a streaming device and is pre-configured to watch Netflix. "
            "Simply switch on the TV and streaming device, and you will have free access to Netflix."
        ),
        manual_url="",
        issues=(
            "If the TV does not turn on, check the power at the wall and that the remote has batteries. "
            "If Netflix is not loading, check the Wi-Fi connection first, then contact guest support."
        ),
        prop_id=p.id,
    )

    howto_fan = HowTo(
        area="Living room",
        appliance="Fan",
        brand_model="",
        how="We have a fan inside the cabinet underneath the TV. Please return it there after use.",
        manual_url="",
        issues="If the fan is not working, check that it is plugged in and the switch is on.",
        prop_id=p.id,
    )

    howto_heater = HowTo(
        area="Bedroom / mezzanine",
        appliance="Portable heater",
        brand_model="",
        how=(
            "There is a heater inside the left cupboard underneath the bed. "
            "Plug it into a nearby socket and use the controls on the unit to adjust the temperature."
        ),
        manual_url="",
        issues="Please turn the heater off and unplug it when leaving the flat or going to sleep.",
        prop_id=p.id,
    )

    howto_ironing = HowTo(
        area="Bedroom / wardrobe",
        appliance="Ironing board",
        brand_model="",
        how="We have an ironing board behind the wardrobe. Please return it there after you finish.",
        manual_url="",
        issues="Do not leave hot irons unattended or face-down on surfaces.",
        prop_id=p.id,
    )

    howto_spare_bedding = HowTo(
        area="Bedroom / wardrobe",
        appliance="Spare pillow & duvet",
        brand_model="",
        how=(
            "Spare duvet and pillows are inside the wardrobe, as well as a sofa bed mattress "
            "for extra comfort behind the wardrobe."
        ),
        manual_url="",
        issues="Please keep spare bedding neatly stored in the wardrobe when not in use.",
        prop_id=p.id,
    )

    howto_hairdryer = HowTo(
        area="Bedroom / wardrobe",
        appliance="Hair dryer",
        brand_model="",
        how="We have a hairdryer inside the wardrobe.",
        manual_url="",
        issues="Please do not use the hairdryer near water.",
        prop_id=p.id,
    )

    db.session.add_all([
        howto_wifi,
        howto_tv,
        howto_fan,
        howto_heater,
        howto_ironing,
        howto_spare_bedding,
        howto_hairdryer,
    ])

    # ------- Check‑in steps -------
    step1 = CheckinStep(
        step=1,
        title="Enter the building",
        body=(
            "Go to the main entrance at 330 Upper Street, N1 2XQ.\n"
            "Enter code C1570Y on the keypad.\n"
            "The door will unlock."
        ),
        tip="Have your booking details handy in case building security ask.",
        prop_id=p.id,
    )

    step2 = CheckinStep(
        step=2,
        title="Access the staircase / lift",
        body=(
            "Head upstairs to the second floor.\n"
            "On your left, you will see a door with a keypad.\n"
            "Enter code C279ZY and turn the handle clockwise to open."
        ),
        tip="Take care with your luggage on the stairs.",
        prop_id=p.id,
    )

    step3 = CheckinStep(
        step=3,
        title="Enter the flat",
        body=(
            "Continue upstairs to Flat 208.\n"
            "At the door, enter the code on the keypad handle. This will be the last 4 digits "
            "of your phone number.\n"
            "Push the handle down to unlock."
        ),
        tip="If the code fails, wait a few seconds and try again slowly.",
        prop_id=p.id,
    )

    db.session.add_all([step1, step2, step3])

    # ------- Check‑out steps -------
    cout1 = CheckoutStep(
        step=1,
        title="General tidy up",
        body=(
            "Please wash any used dishes or load them into the dishwasher if available.\n"
            "Put rubbish in the bins and wipe up any major spills."
        ),
        notes="You do not need to do a deep clean – our professional cleaners will handle that.",
        prop_id=p.id,
    )

    cout2 = CheckoutStep(
        step=2,
        title="Rubbish and recycling",
        body=(
            "Place general waste and recycling in the designated bins as described in the house manual "
            "or at the end of the corridor if applicable."
        ),
        notes="If you are unsure where the bins are, contact guest support before you leave.",
        prop_id=p.id,
    )

    cout3 = CheckoutStep(
        step=3,
        title="Lock up and depart",
        body=(
            "Make sure all windows are closed and lights are switched off.\n"
            "Close the door firmly behind you so it locks."
        ),
        notes="Double-check you have all of your belongings and travel documents before leaving.",
        prop_id=p.id,
    )

    db.session.add_all([cout1, cout2, cout3])

    # ------- Issue flows -------
    issues = [
        IssueFlow(
            category="Wi-Fi issues",
            try_first=(
                "Check that you are connected to the 'VibeFI' network and that the password "
                "w3L0V3V!Be!_ is entered correctly. Restart your device and the router if possible."
            ),
            when_to_contact="If Wi-Fi is still not working after restarting, contact guest support.",
            info_needed="Tell us which devices are affected and any error messages you see.",
            auto_reply="Thanks for letting us know – we will help you get back online as quickly as possible.",
            prop_id=p.id,
        ),
        IssueFlow(
            category="Appliance problems",
            try_first=(
                "Check that the appliance is plugged in and the power is switched on at the wall. "
                "For the heater or fan, try a different socket."
            ),
            when_to_contact="If the appliance still does not work, message guest support.",
            info_needed="Let us know which appliance is affected and what you have already tried.",
            auto_reply="Thank you – we will advise next steps or arrange assistance.",
            prop_id=p.id,
        ),
        IssueFlow(
            category="Noise or neighbours",
            try_first="Kindly try closing windows and doors and lowering your own noise first.",
            when_to_contact=(
                "If there is persistent noise from neighbours or nearby venues late at night, "
                "contact us with details and times."
            ),
            info_needed="Explain where the noise is coming from and how long it has been going on.",
            auto_reply="Thanks for reporting this – we will see what we can do to help.",
            prop_id=p.id,
        ),
        IssueFlow(
            category="Cleaning or damage",
            try_first="If you notice anything not up to standard, please send us a quick photo.",
            when_to_contact="Contact us as soon as you notice the issue, ideally at the start of your stay.",
            info_needed="Photos of the problem and a short description of how it affects your stay.",
            auto_reply="We are sorry about this – we will review and come back with a solution.",
            prop_id=p.id,
        ),
    ]
    db.session.add_all(issues)

    # ------- Emergency contacts -------
    emergencies = [
        Emergency(
            etype="Police / Fire / Ambulance",
            name="Emergency services (UK)",
            phone="999",
            when="For any life-threatening emergency, serious injury, fire or crime in progress.",
            address="330 Upper Street, N1 2XQ, London, United Kingdom",
            notes="State the full address and follow the operator's instructions.",
            prop_id=p.id,
        ),
        Emergency(
            etype="Medical (non‑urgent)",
            name="NHS 111",
            phone="111",
            when="For non‑emergency medical advice when you still need help but it is not life‑threatening.",
            address="Local services as directed by NHS 111.",
            notes="You can call 111 from any phone in the UK.",
            prop_id=p.id,
        ),
        Emergency(
            etype="Host emergency line",
            name="Guest support (WhatsApp)",
            phone="+447592249258",
            when="For urgent issues in the flat such as leaks, power loss or being locked out.",
            address="330 Upper Street, N1 2XQ, London, United Kingdom",
            notes="If it is safe to do so, send photos or a short description of the problem.",
            prop_id=p.id,
        ),
    ]
    db.session.add_all(emergencies)

    # ------- Local recommendations -------
    locals_data = [
        ("Restaurant", "Dishoom",
         "A popular Indian restaurant offering a menu inspired by the Irani cafés of Bombay. "
         "Famous for its aromatic dishes and inviting ambience."),
        ("Comedy", "Angel Comedy Club",
         "A local favorite for stand‑up comedy, featuring hilarious acts and a welcoming atmosphere. "
         "Perfect for a night of laughter."),
        ("Theatre", "The Almeida Theatre",
         "An acclaimed theatre offering a variety of performances from contemporary plays to classic "
         "adaptations. A cultural gem nearby."),
        ("Café", "The Coffee Works Project",
         "A specialty coffee shop with a focus on quality brews and friendly service. "
         "Ideal for coffee lovers looking to kick‑start their day."),
        ("Music venue", "O2 Academy Islington",
         "A vibrant music venue hosting various concerts and live events. "
         "Check the schedule for thrilling performances during your stay."),
        ("Neighbourhood", "Chalk Farm",
         "A charming area known for its iconic Roundhouse and scenic canals. "
         "A great spot for a leisurely walk and local exploration."),
        ("Shopping", "Angel Central",
         "A vibrant shopping and dining destination with a variety of shops, restaurants and a cinema, "
         "perfect for an all‑day outing."),
        ("Restaurant", "The Breakfast Club",
         "A cozy diner known for its hearty breakfast options and vibrant atmosphere, "
         "perfect for starting your day with a delicious meal."),
        ("Market", "Camden Market",
         "A bustling market offering unique shops, vintage clothes and artisanal foods. "
         "A great place to explore and pick up some souvenirs."),
        ("Park", "Regents Park",
         "A beautiful park with stunning gardens, sports facilities and serene walking paths. "
         "Ideal for a leisurely stroll or picnic."),
        ("Park", "Highbury Fields",
         "A beautiful park perfect for a leisurely stroll, picnics and jogging. "
         "Enjoy expansive green spaces and lovely views."),
        ("Pub", "The Drapers Arms",
         "A charming pub known for its locally sourced food and extensive selection of drinks. "
         "A great place to unwind and enjoy the local atmosphere."),
        ("Park", "Islington Green",
         "An iconic green space offering a peaceful retreat in the heart of the city, "
         "with plenty of benches and a nearby café."),
        ("Shopping street", "Camden Passage",
         "A hidden gem in Islington, this market street is filled with antique shops, boutiques "
         "and unique stalls, ideal for shopping enthusiasts."),
        ("Theatre / Pub", "The Old Red Lion Theatre",
         "A historic pub and theatre space offering intimate performances and a good selection of ales. "
         "Great for a relaxed evening out."),
        ("Museum", "Islington Museum",
         "Explore the local history through engaging exhibits at this small yet informative museum. "
         "A fascinating way to spend an afternoon."),
    ]

    for category, name, blurb in locals_data:
        lp = LocalPlace(
            category=category,
            name=name,
            blurb=blurb,
            address="",
            map_link="",
            hours="",
            link="",
            price="",
            prop_id=p.id,
        )
        db.session.add(lp)

    # ------- FAQs -------
    faqs = [
        FAQ(
            q="What is the Wi-Fi network and password?",
            a="The Wi-Fi network is 'VibeFI' and the password is 'w3L0V3V!Be!_'.",
            related="Wi-Fi, Internet",
            prop_id=p.id,
        ),
        FAQ(
            q="How do I check in?",
            a=(
                "Check-in is from 4 pm. Use code C1570Y at the main entrance, then C279ZY at the "
                "second-floor door, and finally the last 4 digits of your phone number on the flat door."
            ),
            related="Check-in, Access, Codes",
            prop_id=p.id,
        ),
        FAQ(
            q="Is early check-in or late check-out possible?",
            a=(
                "Standard check-in is from 4 pm and check-out is by 11 am. Early check-in or late "
                "check-out may be possible depending on cleaning schedules – message us on WhatsApp "
                "at +44 7592 249258 and we will do our best."
            ),
            related="Check-in, Check-out, Times",
            prop_id=p.id,
        ),
        FAQ(
            q="Does the apartment have Netflix?",
            a="Yes, the TV is connected to a streaming device with free access to Netflix for your stay.",
            related="TV, Netflix, Entertainment",
            prop_id=p.id,
        ),
        FAQ(
            q="Where can I find extra bedding?",
            a="Spare duvet, pillows and a sofa-bed mattress are all stored inside the wardrobe.",
            related="Bedding, Sofa bed",
            prop_id=p.id,
        ),
        FAQ(
            q="Is there heating and a fan available?",
            a=(
                "Yes. A fan is in the cabinet under the TV, and a portable heater is in the left cupboard "
                "under the bed."
            ),
            related="Heating, Fan, Comfort",
            prop_id=p.id,
        ),
        FAQ(
            q="Is smoking allowed in the apartment?",
            a="No, smoking or vaping is not allowed anywhere inside the apartment or building.",
            related="Rules, Smoking",
            prop_id=p.id,
        ),
        FAQ(
            q="How do I contact support during my stay?",
            a=(
                "For anything you need, including codes, questions or issues, message guest support "
                "on WhatsApp at +44 7592 249258."
            ),
            related="Contact, Support",
            prop_id=p.id,
        ),
    ]
    db.session.add_all(faqs)

    db.session.commit()

