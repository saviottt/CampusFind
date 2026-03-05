# 🔍 CampusFind — Campus Lost & Found System

A full-stack web application for college students to report, search, and recover lost items on campus.

## Tech Stack
- **Backend**: Python 3 + Flask
- **Database**: SQLite (auto-created on first run)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Auth**: Session-based with Werkzeug password hashing

## Features
1. ✅ User Registration & Login (with student ID & department)
2. ✅ Report Lost Items (with image upload)
3. ✅ Report Found Items (with image upload)
4. ✅ Search & Filter (by keyword, category, location, date)
5. ✅ Auto Matching Suggestions (keyword + location scoring)
6. ✅ In-App Messaging between users
7. ✅ Item Status Tracking (Active / Returned / Closed)
8. ✅ Image Upload Support
9. ✅ Campus Location Dropdown (27 predefined locations)
10. ✅ In-App Notification System with badge counter

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
python app.py

# 3. Open in browser
http://localhost:5000
```

The SQLite database (`campus_lostfound.db`) and uploads folder are created automatically.

## Project Structure
```
campus_lostfound/
├── app.py                  # Main Flask application
├── requirements.txt
├── campus_lostfound.db     # Auto-created SQLite database
├── static/
│   ├── css/style.css       # All styles
│   ├── js/main.js          # Frontend JavaScript
│   └── uploads/            # User-uploaded images
└── templates/
    ├── base.html           # Base layout with navbar
    ├── index.html          # Homepage
    ├── login.html          # Login page
    ├── register.html       # Registration page
    ├── report.html         # Report lost/found item
    ├── item_detail.html    # Item detail with messaging
    ├── search.html         # Search & filter
    ├── all_items.html      # Browse all items
    ├── profile.html        # User profile & notifications
    └── partials/
        └── item_card.html  # Reusable item card component
```

## Database Schema
- **users**: id, name, email, password (hashed), student_id, department
- **items**: id, user_id, type (lost/found), status, title, category, description, location, date_occurred, contact_info, image_path
- **messages**: id, sender_id, receiver_id, item_id, message, is_read
- **notifications**: id, user_id, title, body, link, is_read

## Campus Locations (27 predefined)
Central Library, Main Cafeteria, Computer Science Lab, Physics Lab, Chemistry Lab, Biology Lab, Engineering Block, Arts Block, Commerce Block, Science Block, Administration Block, Auditorium, Sports Ground, Basketball Court, Swimming Pool, Gymnasium, Boys Hostel, Girls Hostel, Parking Area, Bus Stop, Main Gate, Medical Center, Seminar Hall, Workshop/Makerspace, Garden/Open Area, Restroom, Other

## Item Categories (13 predefined)
Electronics, Books & Stationery, Clothing & Accessories, ID Cards & Documents, Keys, Bags & Wallets, Jewelry & Watches, Sports Equipment, Water Bottles & Tumblers, Eyeglasses & Sunglasses, Headphones & Earbuds, Umbrellas, Other
