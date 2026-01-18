# 🖥️ PcForYou – Intelligent PC Builder & Component Marketplace 🤖
> *Build smarter PCs with AI-powered compatibility checks*

---

## 📌 Overview

**PcForYou** is a full-stack **Django-based e-commerce platform** that removes the guesswork from building a custom PC.

At its core is an **AI-powered PC Builder Tool** powered by **Google Gemini**, which acts as a virtual hardware consultant—validating component compatibility, checking physical clearances, and ensuring balanced performance **in real time**.

Unlike traditional part-pickers, PcForYou understands *real-world hardware nuances* and guides users toward **practical, optimized builds**.

---

## 🚀 Key Features

### 🧠 AI PC Builder Tool
An intelligent assistant that validates your custom build **step by step**.

- 🔄 **Real-time Compatibility Checks**
  - CPU ↔ Motherboard socket & chipset compatibility  
  - BIOS version requirements for newer processors  
  - RAM type (DDR4 / DDR5), frequency & capacity support  
  - GPU ↔ Motherboard interface compatibility (PCIe)  
  - Power supply wattage & connector requirements  

- 📏 **Physical Clearance Validation**
  - GPU length, width & slot clearance vs case size  
  - CPU cooler height & radiator support vs case clearance  
  - Motherboard form factor (ATX / mATX / ITX) vs case support  
  - PSU form factor compatibility  

- 💡 **Smart Feedback & Suggestions**
  - Explains *why* a component is incompatible  
  - Suggests compatible and better-balanced alternatives  
  - Prevents common PC building mistakes  


---

### 🛒 E-Commerce Functionality

- 🛍️ **Advanced Cart & Wishlist**
  - Save AI-verified PC builds
  - Add full builds or individual components

- 📦 **Order Tracking System**
  - Track orders from **Processing → Out for Delivery**

- 👤 **User Accounts**
  - Secure authentication
  - Manage addresses, orders

- 🛠️ **Admin Command Center**
  - Inventory management
  - Order & user monitoring
  - Status updates from a centralized dashboard

---

## 🧰 Tech Stack

### Backend
- Python
- Django 5.x

### AI Integration
- Google Gemini API (`google-generativeai`)

### Database
- SQLite3

### Configuration
- Environment variables via `.env`
- Dependencies via `requirements.txt`

---

## 📸 Screenshots

> *(Add screenshots of the AI builder, cart, and admin panel here)*

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/anandhupp73/PC_Ecommerce.git
cd PC_Ecommerce/PcForYou

python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate
pip install -r requirements.txt

Configure Environment Variables

Create a .env file in the project root:

GOOGLE_API_KEY=your_gemini_api_key

Run Migrations & Start Server

python manage.py migrate
python manage.py runserver

🔮 Future Enhancements

 🧩 AI-powered 3D PC Builder

Visual workstation to assemble components in 3D

 🎮 FPS Estimator

AI-based performance prediction for popular games

 🌐 Automated Stock Scraper

Real-time pricing & availability from external vendors
