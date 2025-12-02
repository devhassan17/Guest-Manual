import os, io, datetime
from flask import Flask, render_template, redirect, url_for, request, session, flash, abort, send_file
from flask_migrate import Migrate
from flask_babel import Babel, _
from models import (
    db, Property, Contact, Rule, HowTo, IssueFlow, Emergency,
    LocalPlace, CheckinStep, CheckoutStep, FAQ, Message, PageView, seed
)
import qrcode

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")

    # ---- Config ----
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "devkey")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///guest_manual.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["APP_NAME"] = os.getenv("APP_NAME", "Guest Manual")
    app.config["BRAND_PRIMARY"] = os.getenv("BRAND_PRIMARY", "#0E7C86")
    app.config["BRAND_ACCENT"] = os.getenv("BRAND_ACCENT", "#E7F5F6")
    app.config["ADMIN_PASSWORD"] = os.getenv("ADMIN_PASSWORD", "admin")
    app.config["THEME"] = os.getenv("THEME", "classic")
    app.config["LANGUAGES"] = ["en", "fr", "es"]

    # ---- Extensions ----
    db.init_app(app)
    Migrate(app, db)

    def get_locale():
        return request.accept_languages.best_match(app.config["LANGUAGES"]) or "en"
    Babel(app, locale_selector=get_locale)

    # ---- DB init / seed ----
    with app.app_context():
        db.create_all()
        seed(db)

    # ---- Template context ----
    @app.context_processor
    def inject_config():
        return dict(config=app.config, now=datetime.datetime.utcnow())

    # ---- Helpers ----
    def log_view(prop, section):
        pv = PageView(
            property_id=prop.id,
            section=section,
            user_agent=request.headers.get("User-Agent",""),
            ip=request.remote_addr
        )
        db.session.add(pv); db.session.commit()

    def is_authed():
        return session.get("authed") is True

    # =======================
    # Public routes
    # =======================
    @app.route("/")
    def index():
        props = Property.query.order_by(Property.name).all()
        return render_template("index.html", props=props)

    @app.route("/p/<slug>")
    def property_home(slug):
        prop = Property.query.filter_by(slug=slug).first_or_404()
        log_view(prop, "welcome")
        return render_template("property/welcome.html", p=prop, section="welcome")

    @app.route("/p/<slug>/<section>")
    def property_section(slug, section):
        prop = Property.query.filter_by(slug=slug).first_or_404()
        sections = ["welcome","check-in","rules","how-to","issues","emergency","local","checkout","faqs","social","print","reviews"]
        if section not in sections:
            abort(404)
        tpl = f"property/{section}.html"
        log_view(prop, section)
        return render_template(tpl, p=prop, section=section)

    # How-to detail page (Manual button)
    @app.route("/p/<slug>/howto/<int:id>")
    def property_howto_detail(slug, id):
        prop = Property.query.filter_by(slug=slug).first_or_404()
        h = HowTo.query.get_or_404(id)
        if hasattr(h, "prop_id") and h.prop_id != prop.id:
            abort(404)
        return render_template("property/howto_detail.html", p=prop, h=h)

    # Shareable QR (PNG)
    @app.get("/p/<slug>/qr.png")
    def property_qr(slug):
        prop = Property.query.filter_by(slug=slug).first_or_404()
        url = url_for("property_home", slug=slug, _external=True)
        img = qrcode.make(url)
        buf = io.BytesIO()
        img.save(buf, format="PNG"); buf.seek(0)
        return send_file(buf, mimetype="image/png")

    # Contact / Issue form
    @app.post("/p/<slug>/message")
    def create_message(slug):
        prop = Property.query.filter_by(slug=slug).first_or_404()
        m = Message(
            property_id=prop.id,
            name=request.form.get("name","").strip(),
            contact=request.form.get("contact","").strip(),
            category=request.form.get("category","General"),
            body=request.form.get("body","").strip()
        )
        db.session.add(m); db.session.commit()
        flash(_("Thanks — we received your message."), "ok")
        return redirect(request.referrer or url_for("property_home", slug=slug))

    # =======================
    # Admin: auth & dashboard
    # =======================
    @app.route("/admin/login", methods=["GET","POST"])
    def admin_login():
        if request.method == "POST":
            pwd = request.form.get("password","")
            if pwd == app.config.get("ADMIN_PASSWORD","admin"):
                session["authed"] = True
                return redirect(url_for("admin_dashboard"))
            flash(_("Wrong password"), "error")
        return render_template("admin/login.html")

    @app.route("/admin/logout")
    def admin_logout():
        session.clear()
        return redirect(url_for("index"))

    @app.route("/admin")
    def admin_dashboard():
        if not is_authed():
            return redirect(url_for("admin_login"))
        props = Property.query.order_by(Property.name).all()
        from datetime import datetime, timedelta
        since = datetime.utcnow() - timedelta(days=30)
        views = PageView.query.filter(PageView.created_at >= since).all()
        by_prop = {}
        for v in views:
            by_prop.setdefault(v.property_id, 0)
            by_prop[v.property_id] += 1
        return render_template("admin/dashboard.html", props=props, views=by_prop)

    # =======================
    # Admin: property CRUD (basic)
    # =======================
    @app.route("/admin/property/new", methods=["GET","POST"])
    @app.route("/admin/property/<int:pid>", methods=["GET","POST"])
    def admin_property_form(pid=None):
        if not is_authed():
            return redirect(url_for("admin_login"))
        p = Property.query.get(pid) if pid else None
        if request.method == "POST":
            data = request.form
            if not p: p = Property()
            for field in [
                "slug","name","address_display","map_url","checkin_time","checkout_time",
                "wifi_ssid","wifi_password","parking","quiet_hours","notes",
                "hero_url","gallery_urls",
                "instagram_url","facebook_url","tiktok_url","whatsapp_url","phone_number","email_address"
            ]:
                setattr(p, field, data.get(field,"").strip())
            db.session.add(p); db.session.commit()
            flash(_("Saved property"), "ok")
            return redirect(url_for("admin_dashboard"))
        return render_template("admin/property_form.html", p=p)

    @app.post("/admin/property/<int:pid>/delete")
    def admin_property_delete(pid):
        if not is_authed():
            return redirect(url_for("admin_login"))
        p = Property.query.get_or_404(pid)
        db.session.delete(p); db.session.commit()
        flash(_("Deleted"), "ok")
        return redirect(url_for("admin_dashboard"))

    # Quick add: single rule (compat)
    @app.post("/admin/<int:pid>/rule")
    def add_rule(pid):
        if not is_authed(): return redirect(url_for("admin_login"))
        p = Property.query.get_or_404(pid)
        r = Rule(
            title=request.form.get("title",""),
            description=request.form.get("description",""),
            penalty=request.form.get("penalty",""),
            rationale=request.form.get("rationale",""),
            prop_id=p.id
        )
        db.session.add(r); db.session.commit()
        return redirect(url_for("admin_dashboard"))

    # =======================
    # Admin: Manage per-property content (the page you link with “Manage”)
    # (Routes for this page are the same you already added earlier)
    # =======================
    @app.get("/admin/property/<int:pid>/manage")
    def admin_property_manage(pid):
        if not is_authed(): return redirect(url_for("admin_login"))
        p = Property.query.get_or_404(pid)
        return render_template("admin/property_manage.html", p=p)

    @app.post("/admin/<int:pid>/faq")
    def admin_add_faq(pid):
        if not is_authed(): return redirect(url_for("admin_login"))
        p = Property.query.get_or_404(pid)
        f = FAQ(q=request.form.get("q",""), a=request.form.get("a",""), related=request.form.get("related",""), prop_id=p.id)
        db.session.add(f); db.session.commit()
        flash("FAQ added", "ok")
        return redirect(url_for("admin_property_manage", pid=pid))

    @app.post("/admin/<int:pid>/emergency")
    def admin_add_emergency(pid):
        if not is_authed(): return redirect(url_for("admin_login"))
        p = Property.query.get_or_404(pid)
        e = Emergency(
            etype=request.form.get("etype",""),
            name=request.form.get("name",""),
            phone=request.form.get("phone",""),
            when=request.form.get("when",""),
            address=request.form.get("address",""),
            notes=request.form.get("notes",""),
            prop_id=p.id
        )
        db.session.add(e); db.session.commit()
        flash("Emergency contact added", "ok")
        return redirect(url_for("admin_property_manage", pid=pid))

    @app.post("/admin/<int:pid>/local")
    def admin_add_local(pid):
        if not is_authed(): return redirect(url_for("admin_login"))
        p = Property.query.get_or_404(pid)
        l = LocalPlace(
            category=request.form.get("category",""),
            name=request.form.get("name",""),
            blurb=request.form.get("blurb",""),
            address=request.form.get("address",""),
            map_link=request.form.get("map_link",""),
            hours=request.form.get("hours",""),
            link=request.form.get("link",""),
            price=request.form.get("price",""),
            prop_id=p.id
        )
        db.session.add(l); db.session.commit()
        flash("Local place added", "ok")
        return redirect(url_for("admin_property_manage", pid=pid))

    @app.post("/admin/<int:pid>/howto")
    def admin_add_howto(pid):
        if not is_authed(): return redirect(url_for("admin_login"))
        p = Property.query.get_or_404(pid)
        h = HowTo(
            area=request.form.get("area",""),
            appliance=request.form.get("appliance",""),
            brand_model=request.form.get("brand_model",""),
            how=request.form.get("how",""),
            manual_url=request.form.get("manual_url",""),
            issues=request.form.get("issues",""),
            prop_id=p.id
        )
        db.session.add(h); db.session.commit()
        flash("How-to added", "ok")
        return redirect(url_for("admin_property_manage", pid=pid))

    @app.post("/admin/<int:pid>/checkin")
    def admin_add_checkin(pid):
        if not is_authed(): return redirect(url_for("admin_login"))
        p = Property.query.get_or_404(pid)
        s = CheckinStep(
            step=int(request.form.get("step","0") or 0),
            title=request.form.get("title",""),
            body=request.form.get("body",""),
            image=request.form.get("image",""),
            video=request.form.get("video",""),
            tip=request.form.get("tip",""),
            prop_id=p.id
        )
        db.session.add(s); db.session.commit()
        flash("Check-in step added", "ok")
        return redirect(url_for("admin_property_manage", pid=pid))

    @app.post("/admin/<int:pid>/checkout")
    def admin_add_checkout(pid):
        if not is_authed(): return redirect(url_for("admin_login"))
        p = Property.query.get_or_404(pid)
        s = CheckoutStep(
            step=int(request.form.get("step","0") or 0),
            title=request.form.get("title",""),
            body=request.form.get("body",""),
            notes=request.form.get("notes",""),
            prop_id=p.id
        )
        db.session.add(s); db.session.commit()
        flash("Check-out step added", "ok")
        return redirect(url_for("admin_property_manage", pid=pid))

    @app.post("/admin/<int:pid>/contact")
    def admin_add_contact(pid):
        if not is_authed(): return redirect(url_for("admin_login"))
        p = Property.query.get_or_404(pid)
        c = Contact(
            role=request.form.get("role",""),
            name=request.form.get("name",""),
            phone=request.form.get("phone",""),
            whatsapp=request.form.get("whatsapp",""),
            prop_id=p.id
        )
        db.session.add(c); db.session.commit()
        flash("Contact added", "ok")
        return redirect(url_for("admin_property_manage", pid=pid))

    @app.post("/admin/faq/<int:id>/delete")
    def admin_delete_faq(id):
        if not is_authed(): return redirect(url_for("admin_login"))
        m = FAQ.query.get_or_404(id); pid = m.prop_id
        db.session.delete(m); db.session.commit()
        flash("Deleted", "ok")
        return redirect(url_for("admin_property_manage", pid=pid))

    @app.post("/admin/emergency/<int:id>/delete")
    def admin_delete_emergency(id):
        if not is_authed(): return redirect(url_for("admin_login"))
        m = Emergency.query.get_or_404(id); pid = m.prop_id
        db.session.delete(m); db.session.commit()
        flash("Deleted", "ok")
        return redirect(url_for("admin_property_manage", pid=pid))

    @app.post("/admin/local/<int:id>/delete")
    def admin_delete_local(id):
        if not is_authed(): return redirect(url_for("admin_login"))
        m = LocalPlace.query.get_or_404(id); pid = m.prop_id
        db.session.delete(m); db.session.commit()
        flash("Deleted", "ok")
        return redirect(url_for("admin_property_manage", pid=pid))

    @app.post("/admin/howto/<int:id>/delete")
    def admin_delete_howto(id):
        if not is_authed(): return redirect(url_for("admin_login"))
        m = HowTo.query.get_or_404(id); pid = m.prop_id
        db.session.delete(m); db.session.commit()
        flash("Deleted", "ok")
        return redirect(url_for("admin_property_manage", pid=pid))

    @app.post("/admin/checkin/<int:id>/delete")
    def admin_delete_checkin(id):
        if not is_authed(): return redirect(url_for("admin_login"))
        m = CheckinStep.query.get_or_404(id); pid = m.prop_id
        db.session.delete(m); db.session.commit()
        flash("Deleted", "ok")
        return redirect(url_for("admin_property_manage", pid=pid))

    @app.post("/admin/checkout/<int:id>/delete")
    def admin_delete_checkout(id):
        if not is_authed(): return redirect(url_for("admin_login"))
        m = CheckoutStep.query.get_or_404(id); pid = m.prop_id
        db.session.delete(m); db.session.commit()
        flash("Deleted", "ok")
        return redirect(url_for("admin_property_manage", pid=pid))

    @app.post("/admin/contact/<int:id>/delete")
    def admin_delete_contact(id):
        if not is_authed(): return redirect(url_for("admin_login"))
        m = Contact.query.get_or_404(id); pid = m.prop_id
        db.session.delete(m); db.session.commit()
        flash("Deleted", "ok")
        return redirect(url_for("admin_property_manage", pid=pid))

    # ---- return (keep at the very end) ----
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
