# 🏪 MyShop - ระบบบริหารจัดการคลังสินค้า

ระบบบริหารจัดการสินค้าและขายปลีกแบบครบวงจร สำหรับเจ้าของร้านค้า เพื่อช่วยจัดการสินค้า การซื้อ การขาย และรายงานผลการขายได้อย่างมีประสิทธิภาพ

---

## ✨ คุณสมบัติหลัก

### 📦 จัดการสินค้า
- ✅ เพิ่ม/แก้ไข/ลบสินค้า
- ✅ จัดหมวดหมู่สินค้า
- ✅ ติดตามคงเหลือสินค้า
- ✅ เตือนเมื่อสินค้าต่ำกว่าจำนวนขั้นต่ำ
- ✅ อัปโหลดรูปภาพสินค้า

### 🛒 การขาย
- ✅ บันทึกใบขาย
- ✅ ตรวจสอบการมีอยู่ของสินค้า
- ✅ คำนวณส่วนลดอัตโนมัติ
- ✅ ดูประวัติการขาย
- ✅ ลบรายการขายได้

### 🏭 การจัดซื้อ
- ✅ บันทึกใบสั่งซื้อจากผู้จัดจำหน่าย
- ✅ ติดตามสถานะการได้รับสินค้า
- ✅ จัดการผู้จัดจำหน่าย/ซัพพลายเออร์
- ✅ คำนวณต้นทุน

### 💰 บัญชีรายรับรายจ่าย
- ✅ บันทึกค่าใช้จ่าย
- ✅ วิเคราะห์รายจ่าย
- ✅ ดูรายงานค่าใช้จ่ายรายเดือน/รายปี

### 📊 รายงานและวิเคราะห์
- ✅ รายงานยอดขายรายวัน/เดือน/ปี
- ✅ รายงานกำไร-ขาดทุน
- ✅ สรุปขอมูลบนแดชบอร์ด
- ✅ ตรวจสอบแนวโน้มการขาย

### 🔐 ความปลอดภัย
- ✅ ระบบล็อกอิน/ออกจากระบบ
- ✅ ตรวจสอบสิทธิ์การเข้าถึง
- ✅ บันทึกข้อมูลผู้บันทึก

---

## 🛠️ เทคโนโลยีที่ใช้

- **Backend:** Django 5.2.4
- **Database:** PostgreSQL / SQLite
- **Frontend:** HTML5, CSS3, JavaScript
- **Security:** Django Built-in
- **Deployment:** Gunicorn + WhiteNoise
- **PDF Generation:** ReportLab

---

## 📋 ข้อกำหนดระบบ

- Python 3.8+
- Django 5.2+
- PostgreSQL (สำหรับ Production) หรือ SQLite (สำหรับ Development)
- pip (Python Package Manager)

---

## ⚡ การติดตั้ง

### 1. โคลนหรือดาวน์โหลดโปรเจกต์

```bash
cd c:\programming\myshop
```

### 2. สร้างสภาพแวดล้อมเสมือน (Virtual Environment)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

### 4. ตั้งค่าฐานข้อมูล

```bash
# สร้างไมเกรชัน
python manage.py makemigrations

# เรียกใช้ไมเกรชัน
python manage.py migrate
```

### 5. สร้างบัญชี Admin

```bash
python manage.py createsuperuser
```

ตามด้วยการใส่ชื่อผู้ใช้ รหัสผ่าน และอีเมล

### 6. รันเซิร์ฟเวอร์

```bash
python manage.py runserver
```

ตอนนี้คุณสามารถเข้าใช้ได้ที่ `http://127.0.0.1:8000`

---

## 🚀 การใช้งาน

### เข้าสู่ระบบ
1. ไปที่หน้า `http://127.0.0.1:8000/login/`
2. ใส่ชื่อผู้ใช้และรหัสผ่านที่สร้างไว้

### 📱 เมนูหลัก
- **Dashboard** - แสดงสรุปข้อมูลประจำวัน
- **Products** - จัดการสินค้า
- **Categories** - จัดหมวดหมู่สินค้า
- **Suppliers** - จัดการผู้จัดจำหน่าย
- **Purchases** - บันทึกการซื้อ
- **Sales** - บันทึกการขาย
- **Expenses** - บันทึกค่าใช้จ่าย
- **Reports** - ดูรายงาน

---

## 📁 โครงสร้างโปรเจกต์

```
myshop/
├── manage.py                 # Django management script
├── requirements.txt          # List of dependencies
├── db.sqlite3               # Database (SQLite)
├── shop/                    # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── inventory/               # Django application
│   ├── models.py           # Data models
│   ├── views.py            # Views/Controllers
│   ├── forms.py            # Forms
│   ├── urls.py             # URL routing
│   └── migrations/         # Database migrations
├── templates/              # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── product_*.html
│   ├── sale_*.html
│   ├── purchase_*.html
│   ├── expense_*.html
│   └── report_*.html
└── media/                  # User uploaded files
    └── products/           # Product images
```

---

## 🗄️ โมเดลข้อมูล (Data Models)

### Category - หมวดหมู่สินค้า
```
- name: ชื่อหมวดหมู่
- description: รายละเอียด
```

### Product - สินค้า
```
- code: รหัสสินค้า
- name: ชื่อสินค้า
- category: หมวดหมู่
- cost_price: ราคาทุน
- selling_price: ราคาขาย
- stock_quantity: จำนวนคงเหลือ
- min_stock: จำนวนขั้นต่ำ
```

### Supplier - ผู้จัดจำหน่าย
```
- name: ชื่อบริษัท
- contact_person: ผู้ติดต่อ
- phone: เบอร์โทร
- email: อีเมล
- address: ที่อยู่
```

### Purchase - ใบสั่งซื้อ
```
- purchase_number: เลขที่ใบสั่ง
- supplier: ผู้จัดจำหน่าย
- purchase_date: วันที่สั่ง
- received_date: วันที่รับ
- status: สถานะ (รอรับ/รับแล้ว/ยกเลิก)
```

### Sale - ใบขาย
```
- sale_number: เลขที่ใบขาย
- customer_name: ชื่อลูกค้า
- sale_date: วันที่ขาย
- total_amount: ยอดรวม
- discount: ส่วนลด
- net_amount: ยอดรับสุทธิ
```

### Expense - ค่าใช้จ่าย
```
- expense_number: เลขที่บิล
- category: หมวดหมู่ค่าใช้จ่าย
- description: รายละเอียด
- amount: จำนวนเงิน
- expense_date: วันที่เกิดค่าใช้จ่าย
```

---

## 🔧 การปรับแต่งและการพัฒนา

### เพิ่มฟีเจอร์ใหม่
1. เพิ่มโมเดลใน `inventory/models.py`
2. สร้างฟอร์มใน `inventory/forms.py`
3. สร้าง View ใน `inventory/views.py`
4. เพิ่ม URL ใน `inventory/urls.py`
5. สร้าง Template ใน `templates/`
6. รัน `python manage.py makemigrations` และ `python manage.py migrate`

### ปรับแต่ง Styling
- แก้ไขไฟล์ CSS ใน `templates/`
- ใช้ Django Widget Tweaks สำหรับการปรับแต่งฟอร์ม

---

## 📊 Admin Dashboard

เข้าใช้ Django Admin Panel ได้ที่:
```
http://127.0.0.1:8000/admin/
```

ที่นี่คุณสามารถ:
- จัดการข้อมูลทั้งหมด
- ดูประวัติการเปลี่ยนแปลง
- จัดการสิทธิ์ผู้ใช้

---

## 🐛 แก้ไขปัญหาทั่วไป

### ปัญหา: "ModuleNotFoundError: No module named 'django'"
**วิธีแก้:** ตรวจสอบว่า virtual environment ถูกเปิดใช้งาน
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### ปัญหา: "No such table: inventory_..."
**วิธีแก้:** รัน migrations
```bash
python manage.py migrate
```

### ปัญหา: Static files ไม่แสดง
**วิธีแก้:** รวบรวม static files
```bash
python manage.py collectstatic
```

---

## 📝 ไฟล์สำคัญ

- `requirements.txt` - รายการแพคเกจที่ต้องติดตั้ง
- `shop/settings.py` - การตั้งค่าโปรเจกต์
- `inventory/models.py` - โมเดลข้อมูล
- `inventory/views.py` - ลอจิกธุรกิจ
- `inventory/urls.py` - เส้นทาง URL

---

## 🔐 ความปลอดภัย

⚠️ **สำหรับ Production:**
- เปลี่ยน `DEBUG = False` ใน `settings.py`
- สร้าง Secret Key ใหม่
- ตั้งค่า `ALLOWED_HOSTS`
- ใช้ HTTPS
- ตั้งค่า Database ให้ปลอดภัย
- ใช้ Environment Variables สำหรับข้อมูลที่ละเอียด

---

## 🤝 การสนับสนุนและการพัฒนาต่อ

ถ้าคุณพบปัญหาหรือมีคำแนะนำ กรุณา:
1. ตรวจสอบ Logs
2. เรียกใช้ `python manage.py runserver` เพื่อดูข้อความแสดงข้อผิดพลาด
3. ตรวจสอบ Database Migration

---

## 📄 ลิขสิทธิ์

โปรเจกต์นี้ได้รับอนุญาตภายใต้ MIT License

---

## 📞 ติดต่อสอบถาม

สำหรับคำถามหรือข้อเสนอแนะ กรุณาติดต่อ:
- Email: support@myshop.local
- Issues: เปิด Issue ในระบบ

---

**ขอบคุณที่ใช้ MyShop! 🙏**

สุดท้ายแล้ว หวังว่าระบบนี้จะช่วยให้การบริหารร้านค้าของคุณเป็นไปได้อย่างราบรื่นและมีประสิทธิภาพ ✨
