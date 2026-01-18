PcForYou 🖥️🤖
The Intelligent PC Builder & Component Marketplace

PcForYou is a full-stack Django e-commerce platform that takes the guesswork out of custom PC building. At its core is the AI PC Builder Tool, which allows users to hand-pick components while the Google Gemini AI acts as a technical consultant, verifying compatibility, checking physical clearances, and ensuring optimal performance balance.

🚀 The PC Builder Tool
Unlike standard part-pickers, our tool uses Generative AI to understand the nuances of hardware:

Real-time Compatibility: Select a CPU and Motherboard; the AI instantly checks socket types, BIOS version requirements, and RAM frequency support.

Physical Clearance Guard: The AI verifies if your selected GPU will fit inside your chosen Case and if the CPU cooler height is compatible.

Intelligent Feedback: If a part is incompatible, the AI doesn't just say "No"—it explains why and suggests a better alternative.

🛒 E-Commerce Features
Advanced Cart & Wishlist: Add your AI-verified builds directly to your cart or save them to your wishlist for later.

Order Tracking: Integrated system to monitor your hardware from "Processing" to "Out for Delivery."

Admin Command Center: A powerful dashboard for managing inventory, reviewing order statuses, and overseeing user activity.

User Accounts: Secure login/signup to manage addresses, orders

🛠️ Tech Stack
Framework: Django 5.x (Backend & Frontend Templates)

AI Engine: Google Gemini API (google-generativeai)

Database: SQLite3 (Relational storage for Users, Products, and Orders)

Configuration: Managed via requirements.txt and .env

📸 Visual Tour
(Add your screenshots here as discussed earlier!)


📦 Installation & Setup
Clone the Project:

Bash
git clone https://github.com/anandhupp73/PcForYou.git
cd PcForYou
Environment Setup:

Bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
Configure API Keys: Create a .env file in the root:

Code snippet
GOOGLE_API_KEY=your_gemini_api_key

Database & Run:

Bash
python manage.py migrate
python manage.py runserver
🔮 Future Roadmap
[ ] AI-based 3D Building: A visual workbench to see your parts assembled in 3D.

[ ] FPS Estimator: AI-driven performance predictions for specific games based on the build.

[ ] Automated Stock Scraper: Syncing real-time availability with external hardware vendors.
