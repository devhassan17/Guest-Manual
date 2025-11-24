# Guest Manual — Flask PRO (Social + Mobile + QR)
Features:
- Social tab (Instagram, Facebook, TikTok, WhatsApp, Phone, Email)
- Mobile-optimized tabs; tighter hero/cards
- QR code endpoint per property (`/p/<slug>/qr.png`)
- Online image URLs (hero + gallery)
- Works with Flask 3.x / Flask-Babel 4.x

Quickstart:
```
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Existing DB? Delete `guest_manual.db` to recreate with new columns, or run a migration.
