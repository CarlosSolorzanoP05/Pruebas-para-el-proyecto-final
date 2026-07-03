# 📘 Guía del ORM de Django — Comandos Básicos (CRUD)

Esta guía explica cómo usar el **ORM (Object-Relational Mapping)** de Django para **crear**, **leer**, **actualizar** y **eliminar** datos en este proyecto, usando los modelos reales de las apps `billing` y `purchasing`.

El ORM permite trabajar con la base de datos usando **código Python** en vez de SQL.

## 🖥️ Cómo abrir la consola del ORM

Todos los ejemplos de esta guía se pueden ejecutar desde el shell interactivo de Django:

```bash
python manage.py shell
```

Esto abre una consola de Python con el entorno del proyecto ya cargado, lista para importar modelos y ejecutar consultas.

---

## 1️⃣ CREATE — Crear datos

### Importar los modelos

```python
from billing.models import Brand, ProductGroup, Supplier, Product, Customer, CustomerProfile, Invoice, InvoiceDetail
from purchasing.models import Purchase, PurchaseDetail
```

### Crear y guardar en un solo paso (`create`)

```python
brand = Brand.objects.create(name="Samsung", description="Electrónica")
group = ProductGroup.objects.create(name="Celulares")

product = Product.objects.create(
    name="Galaxy A55",
    brand=brand,
    group=group,
    unit_price=450.00,
    stock=20,
)
```

### Crear instanciando el objeto y luego usando `save()`

```python
supplier = Supplier(name="Tecno Import S.A.", email="ventas@tecnoimport.com")
supplier.save()
```

### Asignar relaciones ManyToMany (proveedores de un producto)

```python
product.suppliers.add(supplier)          # agregar un proveedor
product.suppliers.set([supplier])        # reemplazar todos los proveedores
product.suppliers.remove(supplier)       # quitar un proveedor
```

### Crear un registro relacionado OneToOne (perfil de cliente)

```python
customer = Customer.objects.create(
    dni="1712345678",
    first_name="Juan",
    last_name="Pérez",
    email="juan@example.com",
)

CustomerProfile.objects.create(
    customer=customer,
    taxpayer_type="ruc",
    payment_terms="credit_30",
    credit_limit=1000,
)
```

### Crear una factura con sus líneas de detalle

```python
invoice = Invoice.objects.create(customer=customer)  # invoice_number se genera solo (FAC-000001)

InvoiceDetail.objects.create(
    invoice=invoice,
    product=product,
    quantity=2,
    unit_price=product.unit_price,
)
```

### Crear una compra a un proveedor

```python
purchase = Purchase.objects.create(
    supplier=supplier,
    document_number="001-001-000123",
)

PurchaseDetail.objects.create(
    purchase=purchase,
    product=product,
    quantity=10,
    unit_cost=300.00,
)
```

> 💡 `Invoice.invoice_number` y `Purchase.purchase_number` se generan **automáticamente** al guardar (ver `generate_invoice_number()` / `generate_purchase_number()` en `models.py`), por lo que no es necesario indicarlos manualmente.

### Crear varios registros a la vez (`bulk_create`)

```python
Brand.objects.bulk_create([
    Brand(name="LG"),
    Brand(name="Sony"),
    Brand(name="Apple"),
])
```

---

## 2️⃣ READ — Leer / consultar datos

### Obtener todos los registros

```python
Product.objects.all()
```

### Obtener un único registro (lanza error si no existe o hay más de uno)

```python
Product.objects.get(pk=1)
Customer.objects.get(dni="1712345678")
```

### Filtrar registros (`filter`) — devuelve un QuerySet

```python
Product.objects.filter(is_active=True)
Product.objects.filter(brand__name="Samsung")
Product.objects.filter(unit_price__gte=100)         # precio >= 100
Product.objects.filter(stock__lt=5)                  # poco stock
Product.objects.filter(name__icontains="galaxy")     # búsqueda parcial sin distinguir mayúsculas
```

### Excluir registros (`exclude`)

```python
Product.objects.exclude(is_active=False)
```

### Obtener el primero / verificar existencia

```python
Product.objects.filter(brand=brand).first()
Product.objects.filter(stock=0).exists()
```

### Ordenar resultados

```python
Product.objects.order_by("unit_price")        # ascendente
Product.objects.order_by("-unit_price")       # descendente
```

### Contar registros

```python
Product.objects.filter(is_active=True).count()
```

### Navegar relaciones (FK, M2M, O2O)

```python
product.brand.name                   # ForeignKey (producto -> marca)
brand.products.all()                  # related_name inverso (marca -> productos)
product.suppliers.all()               # ManyToMany
customer.profile                      # OneToOne (related_name='profile')
invoice.details.all()                 # Invoice -> InvoiceDetail (related_name='details')
purchase.details.all()                # Purchase -> PurchaseDetail
```

### Combinar condiciones

```python
from django.db.models import Q

Product.objects.filter(Q(brand__name="Samsung") | Q(brand__name="Sony"))
Product.objects.filter(is_active=True, stock__gt=0)
```

### Optimizar consultas con relaciones (evitar N+1 queries)

```python
Product.objects.select_related("brand", "group").all()
Invoice.objects.prefetch_related("details").all()
```

### Agregaciones

```python
from django.db.models import Sum, Avg, Count

Product.objects.aggregate(total_stock=Sum("stock"))
Invoice.objects.aggregate(promedio=Avg("total"))
Customer.objects.annotate(num_facturas=Count("invoices"))
```

---

## 3️⃣ UPDATE — Actualizar datos

### Actualizar un objeto puntual

```python
product = Product.objects.get(pk=1)
product.unit_price = 499.99
product.stock = 15
product.save()
```

### Actualizar un campo específico (más eficiente)

```python
product.save(update_fields=["unit_price"])
```

### Actualizar varios registros a la vez (`update`) — no llama a `save()` de cada objeto

```python
Product.objects.filter(brand=brand).update(is_active=True)
Product.objects.filter(stock=0).update(is_active=False)
```

### Obtener o crear (evita duplicados)

```python
brand, created = Brand.objects.get_or_create(
    name="Xiaomi",
    defaults={"description": "Electrónica"}
)
```

### Actualizar o crear

```python
Brand.objects.update_or_create(
    name="Xiaomi",
    defaults={"description": "Tecnología móvil"}
)
```

### Actualizar relaciones ManyToMany

```python
product.suppliers.set([supplier1, supplier2])   # reemplaza la lista completa
product.suppliers.add(supplier3)                 # agrega uno
product.suppliers.remove(supplier1)               # quita uno
product.suppliers.clear()                         # quita todos
```

---

## 4️⃣ DELETE — Eliminar datos

### Eliminar un solo registro

```python
product = Product.objects.get(pk=5)
product.delete()
```

### Eliminar varios registros que cumplen una condición

```python
Product.objects.filter(is_active=False).delete()
```

### Eliminar todos los registros de un modelo (⚠️ usar con cuidado)

```python
Brand.objects.all().delete()
```

> ⚠️ **Importante sobre `on_delete`:** en este proyecto, modelos como `Product`, `Customer`, `Invoice` y `Purchase` usan `on_delete=models.PROTECT` en sus llaves foráneas (ej. `Product.brand`, `Invoice.customer`). Esto significa que **Django impedirá eliminar** una `Brand`, `Customer` o `Supplier` si todavía tiene productos/facturas/compras asociadas, para proteger la integridad de los datos. Primero debes eliminar (o reasignar) los registros relacionados.
>
> En cambio, `InvoiceDetail.invoice` y `PurchaseDetail.purchase` usan `on_delete=models.CASCADE`: si eliminas una `Invoice` o `Purchase`, sus detalles (`details`) se eliminan automáticamente en cascada.

---

## 5️⃣ Ejemplo completo: ciclo CRUD de un producto

```python
from billing.models import Brand, ProductGroup, Product

# CREATE
brand = Brand.objects.create(name="HP")
group = ProductGroup.objects.create(name="Laptops")
product = Product.objects.create(
    name="HP Pavilion 15",
    brand=brand,
    group=group,
    unit_price=750.00,
    stock=8,
)

# READ
print(Product.objects.get(pk=product.pk))
print(Product.objects.filter(brand__name="HP"))

# UPDATE
product.stock = 5
product.save()
Product.objects.filter(pk=product.pk).update(unit_price=699.99)

# DELETE
product.delete()
```

---

## 6️⃣ Usar el ORM dentro de las vistas (views.py)

Dentro del código del proyecto (por ejemplo en `billing/views.py` o `purchasing/views.py`), el ORM se usa exactamente igual que en el shell. Ejemplo simplificado:

```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product

def product_list(request):
    products = Product.objects.filter(is_active=True).select_related("brand", "group")
    return render(request, "billing/product_list.html", {"products": products})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.name = request.POST.get("name")
        product.save()
        return redirect("billing:product_list")
    return render(request, "billing/product_form.html", {"product": product})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect("billing:product_list")
```

---

## 7️⃣ Tabla resumen de comandos

| Operación              | Comando                                              |
|-------------------------|-------------------------------------------------------|
| Crear y guardar          | `Modelo.objects.create(**campos)`                    |
| Crear sin guardar        | `obj = Modelo(**campos)` luego `obj.save()`           |
| Crear varios              | `Modelo.objects.bulk_create([...])`                  |
| Obtener todos            | `Modelo.objects.all()`                                |
| Obtener uno               | `Modelo.objects.get(pk=1)`                            |
| Filtrar                   | `Modelo.objects.filter(campo=valor)`                  |
| Excluir                   | `Modelo.objects.exclude(campo=valor)`                 |
| Ordenar                   | `Modelo.objects.order_by("campo")`                    |
| Contar                    | `Modelo.objects.count()`                              |
| Obtener o crear           | `Modelo.objects.get_or_create(**campos)`              |
| Actualizar o crear        | `Modelo.objects.update_or_create(**campos)`           |
| Actualizar un objeto      | `obj.campo = valor; obj.save()`                       |
| Actualizar en masa        | `Modelo.objects.filter(...).update(campo=valor)`      |
| Eliminar un objeto        | `obj.delete()`                                        |
| Eliminar en masa          | `Modelo.objects.filter(...).delete()`                 |

---

## 8️⃣ Comandos de terminal relacionados con el ORM

```bash
python manage.py makemigrations   # detecta cambios en los modelos y crea archivos de migración
python manage.py migrate          # aplica las migraciones a la base de datos
python manage.py shell            # abre la consola interactiva para probar el ORM
python manage.py dbshell          # abre el cliente de la base de datos directamente (SQL)
```

---

📌 **Tip:** Si haces cambios en algún `models.py` (de `billing` o `purchasing`), siempre debes correr `makemigrations` y luego `migrate` para que la base de datos `db.sqlite3` quede sincronizada con los modelos.
