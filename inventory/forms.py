from django import forms
from .models import Product, Category, Supplier, Purchase, PurchaseItem, Sale, SaleItem, Expense

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['code', 'name', 'category', 'description', 'unit', 'cost_price', 'selling_price', 'stock_quantity', 'min_stock', 'image']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'รหัสสินค้า'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ชื่อสินค้า'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'เช่น ชิ้น, กล่อง'}),
            'cost_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'min_stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ชื่อหมวดหมู่'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'phone', 'email', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ชื่อผู้จัดจำหน่าย'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ชื่อผู้ติดต่อ'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'เบอร์โทรศัพท์'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'อีเมล'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['supplier', 'purchase_date', 'received_date', 'status', 'note']
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'purchase_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'received_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ['product', 'quantity', 'unit_price']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['sale_date', 'customer_name', 'discount', 'payment_method', 'note']
        widgets = {
            'sale_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ชื่อลูกค้า (ไม่บังคับ)'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['product', 'quantity', 'unit_price']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['expense_date', 'category', 'description', 'amount', 'note']
        widgets = {
            'expense_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'รายละเอียด'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }