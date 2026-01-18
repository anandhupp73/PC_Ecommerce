🖥️ PcForYou – Intelligent PC Builder & Component Marketplace 🤖

PcForYou is a full-stack Django-based e-commerce platform designed to remove the guesswork from building a custom PC. At its core lies an AI-powered PC Builder Tool that acts as a smart technical consultant, validating component compatibility, physical clearances, and performance balance in real time.

Unlike traditional part-pickers, PcForYou leverages Generative AI (Google Gemini) to understand real-world hardware nuances and guide users toward optimal builds.

🚀 Key Features
🧠 AI PC Builder Tool

An intelligent assistant that validates your custom build step by step.

Real-time Compatibility Checks

CPU ↔ Motherboard socket matching

BIOS version requirements

RAM type and frequency support

Physical Clearance Validation

GPU length vs case size

CPU cooler height vs case clearance

Intelligent Feedback & Suggestions

Explains why a part is incompatible

Recommends compatible alternatives instead of generic errors

🛒 E-Commerce Capabilities

Advanced Cart & Wishlist

Save AI-verified PC builds

Add full builds or individual components to cart

Order Tracking System

Track orders from Processing → Out for Delivery

User Accounts

Secure authentication

Manage addresses, orders, and saved builds

Admin Command Center

Inventory management

Order status updates

User activity monitoring

🛠️ Tech Stack
Layer	Technology
Backend & Templates	Django 5.x
AI Engine	Google Gemini API (google-generativeai)
Database	SQLite3
Environment Config	.env
Dependencies	requirements.txt
📸 Screenshots & Demo

(Add application screenshots here to showcase the UI and AI builder experience)

📦 Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/anandhupp73/PcForYou.git
cd PcForYou

2️⃣ Create & Activate Virtual Environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure Environment Variables

Create a .env file in the project root:

GOOGLE_API_KEY=your_gemini_api_key

5️⃣ Database Migration & Run Server
python manage.py migrate
python manage.py runserver

🔮 Future Roadmap

 AI-based 3D PC Builder

Visual workstation to see components assembled in real time

 FPS Estimator

AI-driven performance predictions for specific games

 Automated Stock Scraper

Sync real-time pricing and availability from external vendors
