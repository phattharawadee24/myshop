from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    """หมวดหมู่สินค้า"""
    name = models.CharField(max_length=100, verbose_name="ชื่อหมวดหมู่")
    description = models.TextField(blank=True, verbose_name="รายละเอียด")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "หมวดหมู่สินค้า"
        verbose_name_plural = "หมวดหมู่สินค้า"
    
    def __str__(self):
        return self.name

class Product(models.Model):
    """สินค้า"""
    code = models.CharField(max_length=50, unique=True, verbose_name="รหัสสินค้า")
    name = models.CharField(max_length=200, verbose_name="ชื่อสินค้า")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="หมวดหมู่")
    description = models.TextField(blank=True, verbose_name="รายละเอียด")
    unit = models.CharField(max_length=50, default="ชิ้น", verbose_name="หน่วย")
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="ราคาทุน")
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="ราคาขาย")
    stock_quantity = models.IntegerField(default=0, verbose_name="จำนวนคงเหลือ")
    min_stock = models.IntegerField(default=10, verbose_name="จำนวนขั้นต่ำ")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="รูปภาพ")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "สินค้า"
        verbose_name_plural = "สินค้า"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    @property
    def is_low_stock(self):
        return self.stock_quantity <= self.min_stock

class Supplier(models.Model):
    """ผู้จัดจำหน่าย/ซัพพลายเออร์"""
    name = models.CharField(max_length=200, verbose_name="ชื่อผู้จัดจำหน่าย")
    contact_person = models.CharField(max_length=100, blank=True, verbose_name="ผู้ติดต่อ")
    phone = models.CharField(max_length=20, blank=True, verbose_name="เบอร์โทร")
    email = models.EmailField(blank=True, verbose_name="อีเมล")
    address = models.TextField(blank=True, verbose_name="ที่อยู่")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "ผู้จัดจำหน่าย"
        verbose_name_plural = "ผู้จัดจำหน่าย"
    
    def __str__(self):
        return self.name

class Purchase(models.Model):
    """การนำเข้าสินค้า"""
    purchase_number = models.CharField(max_length=50, unique=True, verbose_name="เลขที่ใบสั่งซื้อ")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name="ผู้จัดจำหน่าย")
    purchase_date = models.DateTimeField(default=timezone.now, verbose_name="วันที่สั่งซื้อ")
    received_date = models.DateTimeField(null=True, blank=True, verbose_name="วันที่รับสินค้า")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="ยอดรวม")
    status = models.CharField(max_length=20, choices=[
        ('pending', 'รอรับสินค้า'),
        ('received', 'รับสินค้าแล้ว'),
        ('cancelled', 'ยกเลิก')
    ], default='pending', verbose_name="สถานะ")
    note = models.TextField(blank=True, verbose_name="หมายเหตุ")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="ผู้บันทึก")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "การนำเข้าสินค้า"
        verbose_name_plural = "การนำเข้าสินค้า"
        ordering = ['-purchase_date']
    
    def __str__(self):
        return f"{self.purchase_number} - {self.supplier.name}"
    
    def save(self, *args, **kwargs):
        if not self.purchase_number:
            last = Purchase.objects.order_by('-id').first()
            if last:
                num = int(last.purchase_number.split('-')[1]) + 1
            else:
                num = 1
            self.purchase_number = f"PO-{num:05d}"
        super().save(*args, **kwargs)

class PurchaseItem(models.Model):
    """รายการสินค้าที่สั่งซื้อ"""
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items', verbose_name="ใบสั่งซื้อ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="สินค้า")
    quantity = models.IntegerField(verbose_name="จำนวน")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="ราคาต่อหน่วย")
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="ราคารวม")
    
    class Meta:
        verbose_name = "รายการสินค้านำเข้า"
        verbose_name_plural = "รายการสินค้านำเข้า"
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        
        # อัพเดท stock เมื่อรับสินค้าแล้ว
        if self.purchase.status == 'received':
            self.product.stock_quantity += self.quantity
            self.product.save()

class Sale(models.Model):
    """การขายสินค้า"""
    sale_number = models.CharField(max_length=50, unique=True, verbose_name="เลขที่ใบเสร็จ")
    sale_date = models.DateTimeField(default=timezone.now, verbose_name="วันที่ขาย")
    customer_name = models.CharField(max_length=200, blank=True, verbose_name="ชื่อลูกค้า")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="ยอดรวม")
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="ส่วนลด")
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="ยอดสุทธิ")
    payment_method = models.CharField(max_length=20, choices=[
        ('cash', 'เงินสด'),
        ('transfer', 'โอนเงิน'),
        ('card', 'บัตรเครดิต')
    ], default='cash', verbose_name="วิธีชำระเงิน")
    note = models.TextField(blank=True, verbose_name="หมายเหตุ")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="ผู้บันทึก")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "การขายสินค้า"
        verbose_name_plural = "การขายสินค้า"
        ordering = ['-sale_date']
    
    def __str__(self):
        return f"{self.sale_number}"
    
    def save(self, *args, **kwargs):
        if not self.sale_number:
            last = Sale.objects.order_by('-id').first()
            if last:
                num = int(last.sale_number.split('-')[1]) + 1
            else:
                num = 1
            self.sale_number = f"INV-{num:05d}"
        
        self.net_amount = self.total_amount - self.discount
        super().save(*args, **kwargs)

class SaleItem(models.Model):
    """รายการสินค้าที่ขาย"""
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items', verbose_name="ใบเสร็จ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="สินค้า")
    quantity = models.IntegerField(verbose_name="จำนวน")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="ราคาต่อหน่วย")
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="ราคารวม")
    
    class Meta:
        verbose_name = "รายการสินค้าขาย"
        verbose_name_plural = "รายการสินค้าขาย"
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        
        # ลด stock
        self.product.stock_quantity -= self.quantity
        self.product.save()

class Expense(models.Model):
    """รายจ่ายอื่นๆ"""
    expense_date = models.DateTimeField(default=timezone.now, verbose_name="วันที่จ่าย")
    category = models.CharField(max_length=100, choices=[
        ('utilities', 'ค่าน้ำ-ค่าไฟ'),
        ('rent', 'ค่าเช่า'),
        ('salary', 'เงินเดือน'),
        ('maintenance', 'ค่าซ่อมบำรุง'),
        ('other', 'อื่นๆ')
    ], verbose_name="ประเภท")
    description = models.CharField(max_length=200, verbose_name="รายละเอียด")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="จำนวนเงิน")
    note = models.TextField(blank=True, verbose_name="หมายเหตุ")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="ผู้บันทึก")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "รายจ่าย"
        verbose_name_plural = "รายจ่าย"
        ordering = ['-expense_date']
    
    def __str__(self):
        return f"{self.description} - {self.amount}"