from django.db import models
from django.contrib.auth.models import User 
import random
from django.utils import timezone

class Tax(models.Model):
    tax_name = models.CharField(max_length=20)
    tax_percentage = models.FloatField()

    def __str__(self):
        return '{}  {} %'.format(str(self.tax_name),(self.tax_percentage))
    
class Units(models.Model):
    unit = models.CharField(max_length=20)
    description = models.CharField(max_length=255)

    def __str__(self):
        return str(self.unit)
    

class ProductCategory(models.Model):
    name = models.CharField(max_length=20)
    # image = models.FileField(upload_to='category_images')
    date_added = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)


from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator


class Vendor(models.Model):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(
        max_length=15,
        # validators=[RegexValidator(r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]
    )
    gst_number = models.CharField(max_length=15, validators=[MinLengthValidator(15), MaxLengthValidator(15)], null=True, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(null=True,max_length=255)
    country = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)
    contact_info = models.TextField(blank=True, null=True)
    supply_product = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name +" "+ self.supply_product)

class InventoryStock(models.Model):
    date_added = models.DateField(auto_now_add=True)
    product_code = models.CharField(max_length=20, null=True,blank=True)
    product_name = models.CharField(max_length=200)
    product_stock = models.FloatField(default=0)  # Stock in grams or kilograms
    unit = models.CharField(max_length=10, choices=[('g', 'grams'), ('kg', 'kilograms')], default='kg')  # Default to kilograms
    min_stock_level = models.FloatField(default=0)  # Minimum stock level for alerts
    last_purchase_date = models.DateField(auto_now_add=False, null=True, blank=True)
    last_purchase_amount = models.FloatField(null=True, blank=True, default=0)
    stock_alert = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Generate purchase order number if it doesn't exist
        if not self.product_code:
            self.product_code = self.generate_order_number()
        super().save(*args, **kwargs)

    def generate_order_number(self):
        # Loop to ensure uniqueness
        while True:
            random_number = random.randint(1000, 9999)  # 5-digit random number
            order_number = f"ST-{random_number}"
            if not InventoryStock.objects.filter(product_code=order_number).exists():
                return order_number


    def reduce_stock(self, amount):
        self.product_stock -= amount
        if self.product_stock <= self.min_stock_level:
            # Trigger stock alert
            self.trigger_stock_alert()

    def trigger_stock_alert(self):
        self.stock_alert = True

    def __str__(self):
        return f"{self.product_name}"




class Product(models.Model):
    product_code = models.CharField(max_length=20, null=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null =True, blank=True)
    name = models.CharField(max_length=255)
    inventory = models.ForeignKey(InventoryStock, on_delete=models.SET_NULL, null=True, blank=True)
    # image = models.FileField(upload_to='foodimage', null=True, blank=True)
    unit_quantity = models.FloatField()
    unit_price = models.FloatField()
    status = models.BooleanField(default=True)
    Number_of_stock = models.IntegerField()
    description = models.CharField(max_length=1000, null=True, blank=True)
    create_date = models.DateField(auto_now_add=True)
    # Additional fields
    price_before_tax = models.FloatField(null=True, blank=True, default=0)
    tax_amount = models.FloatField(null=True, blank=True,)
    unit = models.ForeignKey(Units, on_delete=models.SET_NULL, null=True, blank=True)

    # product description
    barcode_number = models.CharField(max_length=200, null= True, blank=True)

    # Tax calculation
    TAX_CHOICES = (
        ("Inclusive", "Inclusive"),
        ("Exclusive", "Exclusive"),
    )
    tax = models.CharField(max_length=20, choices=TAX_CHOICES, default="Inclusive")
    tax_value = models.ForeignKey(Tax, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.unit_price is not None:
            self.unit_price = float(self.unit_price)  # Ensure self.price is a float
            if self.tax_value:
                tax_rate = self.tax_value.tax_percentage / 100
                if self.tax == "Exclusive":
                    self.tax_amount = round(self.unit_price * tax_rate, 2)
                    self.price_before_tax = round(self.unit_price, 2)
                    self.unit_price = round(self.unit_price + self.tax_amount, 2)
                elif self.tax == "Inclusive":
                    self.price_before_tax = round(self.unit_price / (1 + tax_rate), 2)
                    self.tax_amount = round(self.unit_price - self.price_before_tax, 2)
            else:
                self.price_before_tax = round(self.unit_price, 2)
                self.tax_amount = 0.0
        else:
            self.price_before_tax = 0.0
            self.tax_amount = 0.0

        if not self.product_code:
            self.product_code = self.generate_order_number()

        super(Product, self).save(*args, **kwargs)

   

    def generate_order_number(self):
        # Loop to ensure uniqueness
        while True:
            random_number = random.randint(1000, 9999)  # 5-digit random number
            order_number = f"IT-{random_number}"
            if not Product.objects.filter(product_code=order_number).exists():
                return order_number

    def __str__(self):
        return str (self.name + " " +str(self.unit_quantity) + " " + self.unit.unit) 
    

class Batch(models.Model):
    product = models.ForeignKey(Product, related_name='batches', on_delete=models.CASCADE)
    batch_code = models.CharField(max_length=64, unique=True)  # Batch code for tracking
    expiry_date = models.DateField(null=True, blank=True)  # Expiry date for this batch
    stock_quantity = models.PositiveIntegerField(default=0)  # Stock for this specific batch
    manufactured_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.batch_code:
                self.batch_code = self.generate_batch_code()

        super(Batch, self).save(*args, **kwargs)

    def generate_batch_code(self):
        # Loop to ensure uniqueness
        while True:
            random_number = random.randint(1000, 9999)  # 5-digit random number
            order_number = f"BATCH-{random_number}"
            if not Batch.objects.filter(batch_code=order_number).exists():
                return order_number

    def is_expired(self):
        """Check if the batch is expired."""
        if self.expiry_date and timezone.now().date() > self.expiry_date:
            return True
        return False

    def __str__(self):
        return f"{self.batch_code} of {self.product.name} expiry {self.expiry_date}"

    

class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, null=True)
    email = models.EmailField(null=True)
    gst_number = models.CharField(max_length=15, validators=[MinLengthValidator(15), MaxLengthValidator(15)], blank=True, null=True)
    city = models.CharField(max_length=255)
    state = models.CharField(null=True, blank=True, max_length=255)
    country = models.CharField(max_length=255, null=True, blank=True)
    pincode = models.CharField(max_length=100, null=True, blank=True)
    contact_info = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)
    

class PurchaseOrder(models.Model):
    PURCHASE_TYPES = [
        ('Credit', 'Credit'),
        ('Cash', 'Cash'),
       
    ]
    
    ORDER_STATUS_CHOICES = [
        ('Closed', 'Closed'),
        ('Active', 'Active'),
        ('Expired', 'Expired'),
    ]
    
    purchase_order_number = models.CharField(max_length=20, unique=True)
    purchase_type = models.CharField(max_length=20, choices=PURCHASE_TYPES, default="Cash")
    bill_date = models.DateTimeField(auto_now_add=True)
    valid_till = models.DateField()
    supplier = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    place_of_supply = models.CharField(max_length=100)
    purchase_item = models.ForeignKey(InventoryStock, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.FloatField()
    purchase_price = models.FloatField()
    discount = models.FloatField(help_text='in %', null=True, blank=True)
    tax = models.FloatField(default=0)
    cess = models.FloatField(default=0)
    unit = models.CharField(max_length=255, choices=(("g", "gram"), ("kg", "kilograms")), default="kg")
    amount = models.FloatField()
    status = models.BooleanField(default=True)
    order_status = models.CharField(max_length=30, choices=ORDER_STATUS_CHOICES)

    def save(self, *args, **kwargs):
        # Generate purchase order number if it doesn't exist
        if not self.purchase_order_number:
            self.purchase_order_number = self.generate_order_number()
        super().save(*args, **kwargs)

    def generate_order_number(self):
        # Loop to ensure uniqueness
        while True:
            random_number = random.randint(10000, 999999)  # 5-digit random number
            order_number = f"PRO-{random_number}"
            if not PurchaseOrder.objects.filter(purchase_order_number=order_number).exists():
                return order_number

    def create_purchase(self):
        # Check the unit in InventoryStock and adjust accordingly
        stock = self.purchase_item

        if not stock:
            raise ValueError("No inventory item selected for purchase.")

        # Adjust quantity based on the units in PurchaseOrder and InventoryStock
        purchase_quantity = self.quantity

        # If stock is in grams but purchase is in kilograms, convert purchase to grams
        if stock.unit == 'g' and self.unit == 'kg':
            purchase_quantity *= 1000  # Convert kilograms to grams

        # If stock is in kilograms but purchase is in grams, convert purchase to kilograms
        elif stock.unit == 'kg' and self.unit == 'g':
            purchase_quantity /= 1000  # Convert grams to kilograms

        # Create a Purchase instance based on this PurchaseOrder
        purchase = Purchase.objects.create(
            purchase_type=self.purchase_type,
            supplier=self.supplier,
            place_of_supply=self.place_of_supply,
            purchase_order_number=self.purchase_order_number,
            purchase_order_date=self.bill_date,
            purchase_item=self.purchase_item,
            quantity=purchase_quantity,  # Adjusted quantity
            purchase_price=self.purchase_price,
            discount=self.discount,
            tax=self.tax,
            unit=stock.unit,  # Use the InventoryStock unit
            amount=self.amount,
            paid_amount=0,  # Default value, can be updated later
            balance_amount=self.amount,  # Initially, balance equals the total amount
            payment_status="UNPAID",  # Default status, can be updated later
            shipping_cost=0,  # Default value, update as needed
        )

        # Update the inventory stock based on the adjusted quantity
        stock.product_stock += purchase_quantity
        stock.last_purchase_date = purchase.bill_date
        stock.last_purchase_amount = purchase.amount
        stock.save()

        return purchase

    def __str__(self):
        return f"PurchaseOrder {self.purchase_order_number} - {self.supplier}"


class Purchase(models.Model):
    PURCHASE_TYPES = [
        ('Credit', 'Credit'),
        ('Cash', 'Cash'),
        
    ]
    PAYMENT_STATUS = (
        ("UNPAID","UNPAID"),
        ("PAID","PAID"),
        ("PARTIALLY","PARTIALLY")
    )
    
    purchase_type = models.CharField(max_length=20, choices=PURCHASE_TYPES)
    bill_date = models.DateTimeField(auto_now_add=True)
    supplier = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    payment_terms = models.CharField(help_text='Number of days, Credit Period',max_length=255, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    place_of_supply = models.CharField(max_length=100)
    purchase_bill_number = models.CharField(max_length=255, null=True, blank=True)
    purchase_order_number = models.CharField(max_length=20, null=True, blank=True)
    purchase_order_date = models.DateField(null=True, blank=True)
    purchase_item = models.ForeignKey(InventoryStock, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.FloatField()
    purchase_price = models.FloatField()
    discount = models.FloatField(help_text='in %', null=True, blank=True)
    unit = models.CharField(max_length=255, choices=(("g","gram"),("kg","kilograms")), default="kg")
    tax = models.FloatField(null=True, blank=True)
    amount = models.FloatField()
    paid_amount = models.FloatField()
    balance_amount = models.FloatField()
    payment_status = models.CharField(max_length=20,choices=PAYMENT_STATUS)
    shipping_cost = models.FloatField(null=True, blank=True)
    recived_date = models.DateField(auto_now_add=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate purchase order number if it doesn't exist
        if not self.purchase_bill_number:
            self.purchase_bill_number = self.generate_order_number()

        # Apply discount if available
        discount_factor = 1 - (self.discount / 100) if self.discount else 1
        total_amount = self.amount * discount_factor
        
        # Calculate balance amount
        self.balance_amount = total_amount - self.paid_amount

        # Update payment status
        if self.balance_amount <= 0:
            self.payment_status = "PAID"
            self.balance_amount = 0  # Ensure no negative balance
        elif 0 < self.paid_amount < total_amount:
            self.payment_status = "PARTIALLY"
        else:
            self.payment_status = "UNPAID"
            
        super().save(*args, **kwargs)


    def generate_order_number(self):
        # Loop to ensure uniqueness
        while True:
            random_number = random.randint(10000, 999999)  # 5-digit random number
            order_number = f"PR-{random_number}"
            if not Purchase.objects.filter(purchase_bill_number=order_number).exists():
                return order_number


    def __str__(self):
        return f"Purchase {self.id} - {self.supplier}"






