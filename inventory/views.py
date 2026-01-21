from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from .models import *
from .forms import *

# ==================== Authentication Views ====================
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'ยินดีต้อนรับ {username}')
                return redirect('dashboard')
        else:
            messages.error(request, 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'ออกจากระบบเรียบร้อยแล้ว')
    return redirect('login')

# ==================== Dashboard ====================
@login_required
def dashboard(request):
    today = timezone.now().date()
    
    # สรุปข้อมูลวันนี้
    today_sales = Sale.objects.filter(sale_date__date=today)
    today_revenue = today_sales.aggregate(total=Sum('net_amount'))['total'] or 0
    today_sales_count = today_sales.count()
    
    # สรุปข้อมูลเดือนนี้
    month_start = today.replace(day=1)
    month_sales = Sale.objects.filter(sale_date__date__gte=month_start)
    month_revenue = month_sales.aggregate(total=Sum('net_amount'))['total'] or 0
    
    month_purchases = Purchase.objects.filter(purchase_date__date__gte=month_start, status='received')
    month_cost = month_purchases.aggregate(total=Sum('total_amount'))['total'] or 0
    
    month_expenses = Expense.objects.filter(expense_date__date__gte=month_start)
    month_expense_total = month_expenses.aggregate(total=Sum('amount'))['total'] or 0
    
    month_profit = month_revenue - month_cost - month_expense_total
    
    # สินค้าใกล้หมด
    low_stock_products = Product.objects.filter(stock_quantity__lte=F('min_stock'))[:5]
    
    # ยอดขายสูงสุด
    top_products = Product.objects.annotate(
        total_sold=Sum('saleitem__quantity')
    ).order_by('-total_sold')[:5]
    
    # รายการขายล่าสุด
    recent_sales = Sale.objects.all()[:10]
    
    context = {
        'today_revenue': today_revenue,
        'today_sales_count': today_sales_count,
        'month_revenue': month_revenue,
        'month_cost': month_cost,
        'month_expense_total': month_expense_total,
        'month_profit': month_profit,
        'low_stock_products': low_stock_products,
        'top_products': top_products,
        'recent_sales': recent_sales,
    }
    return render(request, 'dashboard.html', context)

# ==================== Product Views ====================
@login_required
def product_list(request):
    products = Product.objects.all()
    search = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    
    if search:
        products = products.filter(
            Q(code__icontains=search) | 
            Q(name__icontains=search)
        )
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'search': search,
        'selected_category': category_id,
    }
    return render(request, 'product_list.html', context)

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'เพิ่มสินค้าเรียบร้อยแล้ว')
            return redirect('product_list')
    else:
        form = ProductForm()
    
    return render(request, 'product_form.html', {'form': form, 'title': 'เพิ่มสินค้า'})

@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'แก้ไขสินค้าเรียบร้อยแล้ว')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'product_form.html', {'form': form, 'title': 'แก้ไขสินค้า'})

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'ลบสินค้าเรียบร้อยแล้ว')
        return redirect('product_list')
    return render(request, 'product_confirm_delete.html', {'product': product})

# ==================== Category Views ====================
@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'เพิ่มหมวดหมู่เรียบร้อยแล้ว')
            return redirect('category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'category_form.html', {'form': form, 'title': 'เพิ่มหมวดหมู่'})

# ==================== Supplier Views ====================
@login_required
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'supplier_list.html', {'suppliers': suppliers})

@login_required
def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'เพิ่มผู้จัดจำหน่ายเรียบร้อยแล้ว')
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    
    return render(request, 'supplier_form.html', {'form': form, 'title': 'เพิ่มผู้จัดจำหน่าย'})


# ต่อจาก views.py ส่วนที่ 1

# ==================== Purchase Views ====================
@login_required
def purchase_list(request):
    purchases = Purchase.objects.all()
    status = request.GET.get('status', '')
    
    if status:
        purchases = purchases.filter(status=status)
    
    return render(request, 'purchase_list.html', {'purchases': purchases, 'selected_status': status})

@login_required
def purchase_create(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.created_by = request.user
            purchase.save()
            messages.success(request, f'สร้างใบสั่งซื้อ {purchase.purchase_number} เรียบร้อยแล้ว')
            return redirect('purchase_detail', pk=purchase.pk)
    else:
        form = PurchaseForm()
    
    return render(request, 'purchase_form.html', {'form': form, 'title': 'สร้างใบสั่งซื้อ'})

@login_required
def purchase_detail(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    items = purchase.items.all()
    
    if request.method == 'POST':
        form = PurchaseItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.purchase = purchase
            item.save()
            
            # อัพเดทยอดรวม
            total = purchase.items.aggregate(total=Sum('total_price'))['total'] or 0
            purchase.total_amount = total
            purchase.save()
            
            messages.success(request, 'เพิ่มรายการสินค้าเรียบร้อยแล้ว')
            return redirect('purchase_detail', pk=pk)
    else:
        form = PurchaseItemForm()
    
    context = {
        'purchase': purchase,
        'items': items,
        'form': form,
    }
    return render(request, 'purchase_detail.html', context)

@login_required
def purchase_item_delete(request, pk):
    item = get_object_or_404(PurchaseItem, pk=pk)
    purchase = item.purchase
    item.delete()
    
    # อัพเดทยอดรวม
    total = purchase.items.aggregate(total=Sum('total_price'))['total'] or 0
    purchase.total_amount = total
    purchase.save()
    
    messages.success(request, 'ลบรายการเรียบร้อยแล้ว')
    return redirect('purchase_detail', pk=purchase.pk)

@login_required
def purchase_receive(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    if purchase.status == 'pending':
        purchase.status = 'received'
        purchase.received_date = timezone.now()
        purchase.save()
        
        # อัพเดท stock
        for item in purchase.items.all():
            item.product.stock_quantity += item.quantity
            item.product.save()
        
        messages.success(request, 'รับสินค้าเรียบร้อยแล้ว')
    
    return redirect('purchase_detail', pk=pk)

# ==================== Sale Views ====================
@login_required
def sale_list(request):
    sales = Sale.objects.all()
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    if date_from:
        sales = sales.filter(sale_date__date__gte=date_from)
    if date_to:
        sales = sales.filter(sale_date__date__lte=date_to)
    
    return render(request, 'sale_list.html', {
        'sales': sales,
        'date_from': date_from,
        'date_to': date_to,
    })

@login_required
def sale_create(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.created_by = request.user
            sale.save()
            messages.success(request, f'สร้างใบเสร็จ {sale.sale_number} เรียบร้อยแล้ว')
            return redirect('sale_detail', pk=sale.pk)
    else:
        form = SaleForm()
    
    return render(request, 'sale_form.html', {'form': form, 'title': 'สร้างใบเสร็จ'})

@login_required
def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    items = sale.items.all()
    
    if request.method == 'POST':
        form = SaleItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.sale = sale
            
            # ตรวจสอบ stock
            if item.product.stock_quantity < item.quantity:
                messages.error(request, f'สินค้า {item.product.name} เหลือไม่เพียงพอ (เหลือ {item.product.stock_quantity} {item.product.unit})')
                return redirect('sale_detail', pk=pk)
            
            item.save()
            
            # อัพเดทยอดรวม
            total = sale.items.aggregate(total=Sum('total_price'))['total'] or 0
            sale.total_amount = total
            sale.net_amount = total - sale.discount
            sale.save()
            
            messages.success(request, 'เพิ่มรายการสินค้าเรียบร้อยแล้ว')
            return redirect('sale_detail', pk=pk)
    else:
        form = SaleItemForm()
    
    context = {
        'sale': sale,
        'items': items,
        'form': form,
    }
    return render(request, 'sale_detail.html', context)

@login_required
def sale_item_delete(request, pk):
    item = get_object_or_404(SaleItem, pk=pk)
    sale = item.sale
    
    # คืน stock
    item.product.stock_quantity += item.quantity
    item.product.save()
    
    item.delete()
    
    # อัพเดทยอดรวม
    total = sale.items.aggregate(total=Sum('total_price'))['total'] or 0
    sale.total_amount = total
    sale.net_amount = total - sale.discount
    sale.save()
    
    messages.success(request, 'ลบรายการเรียบร้อยแล้ว')
    return redirect('sale_detail', pk=sale.pk)

# ==================== Expense Views ====================
@login_required
def expense_list(request):
    expenses = Expense.objects.all()
    category = request.GET.get('category', '')
    
    if category:
        expenses = expenses.filter(category=category)
    
    return render(request, 'expense_list.html', {
        'expenses': expenses,
        'selected_category': category,
    })

@login_required
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.created_by = request.user
            expense.save()
            messages.success(request, 'บันทึกรายจ่ายเรียบร้อยแล้ว')
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    
    return render(request, 'expense_form.html', {'form': form, 'title': 'บันทึกรายจ่าย'})

# ==================== Report Views ====================
@login_required
def report_monthly(request):
    year = int(request.GET.get('year', timezone.now().year))
    month = int(request.GET.get('month', timezone.now().month))
    
    month_start = datetime(year, month, 1).date()
    if month == 12:
        month_end = datetime(year + 1, 1, 1).date()
    else:
        month_end = datetime(year, month + 1, 1).date()
    
    # รายได้
    sales = Sale.objects.filter(sale_date__date__gte=month_start, sale_date__date__lt=month_end)
    total_revenue = sales.aggregate(total=Sum('net_amount'))['total'] or 0
    
    # ต้นทุน
    purchases = Purchase.objects.filter(
        received_date__date__gte=month_start,
        received_date__date__lt=month_end,
        status='received'
    )
    total_cost = purchases.aggregate(total=Sum('total_amount'))['total'] or 0
    
    # รายจ่าย
    expenses = Expense.objects.filter(expense_date__date__gte=month_start, expense_date__date__lt=month_end)
    total_expense = expenses.aggregate(total=Sum('amount'))['total'] or 0
    expense_by_category = expenses.values('category').annotate(total=Sum('amount'))
    
    # กำไร
    profit = total_revenue - total_cost - total_expense
    
    # รายงานตามวัน
    daily_sales = sales.extra(select={'day': 'date(sale_date)'}).values('day').annotate(
        total=Sum('net_amount'),
        count=Count('id')
    ).order_by('day')
    
    context = {
        'year': year,
        'month': month,
        'total_revenue': total_revenue,
        'total_cost': total_cost,
        'total_expense': total_expense,
        'profit': profit,
        'expense_by_category': expense_by_category,
        'daily_sales': daily_sales,
    }
    return render(request, 'report_monthly.html', context)

@login_required
def report_yearly(request):
    year = int(request.GET.get('year', timezone.now().year))
    
    year_start = datetime(year, 1, 1).date()
    year_end = datetime(year + 1, 1, 1).date()
    
    # รายได้
    sales = Sale.objects.filter(sale_date__date__gte=year_start, sale_date__date__lt=year_end)
    total_revenue = sales.aggregate(total=Sum('net_amount'))['total'] or 0
    
    # ต้นทุน
    purchases = Purchase.objects.filter(
        received_date__date__gte=year_start,
        received_date__date__lt=year_end,
        status='received'
    )
    total_cost = purchases.aggregate(total=Sum('total_amount'))['total'] or 0
    
    # รายจ่าย
    expenses = Expense.objects.filter(expense_date__date__gte=year_start, expense_date__date__lt=year_end)
    total_expense = expenses.aggregate(total=Sum('amount'))['total'] or 0
    
    # กำไร
    profit = total_revenue - total_cost - total_expense
    
    # รายงานรายเดือน
    monthly_data = []
    for m in range(1, 13):
        month_start = datetime(year, m, 1).date()
        if m == 12:
            month_end = datetime(year + 1, 1, 1).date()
        else:
            month_end = datetime(year, m + 1, 1).date()
        
        month_sales = sales.filter(sale_date__date__gte=month_start, sale_date__date__lt=month_end)
        month_revenue = month_sales.aggregate(total=Sum('net_amount'))['total'] or 0
        
        month_purchases = purchases.filter(received_date__date__gte=month_start, received_date__date__lt=month_end)
        month_cost = month_purchases.aggregate(total=Sum('total_amount'))['total'] or 0
        
        month_expenses = expenses.filter(expense_date__date__gte=month_start, expense_date__date__lt=month_end)
        month_expense = month_expenses.aggregate(total=Sum('amount'))['total'] or 0
        
        monthly_data.append({
            'month': m,
            'revenue': month_revenue,
            'cost': month_cost,
            'expense': month_expense,
            'profit': month_revenue - month_cost - month_expense,
        })
    
    context = {
        'year': year,
        'total_revenue': total_revenue,
        'total_cost': total_cost,
        'total_expense': total_expense,
        'profit': profit,
        'monthly_data': monthly_data,
    }
    return render(request, 'report_yearly.html', context)