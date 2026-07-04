# Sistema de Facturación y Compras (Django)

Aplicación web desarrollada en **Django 6** para la gestión de facturación, inventario, clientes, proveedores y compras de una empresa. Usa **SQLite** como base de datos por defecto y el **ORM de Django** para todo el acceso a datos.

## 📋 Características

- Gestión de **marcas**, **grupos de productos**, **productos** (con foto e inventario) y **proveedores**.
- Gestión de **clientes** con perfil extendido (tipo de contribuyente, condiciones de pago, límite de crédito).
- **Facturación** (`billing`): generación de facturas con numeración correlativa automática (`FAC-000001`) y detalle de líneas.
- **Compras** (`purchasing`): registro de compras a proveedores con numeración correlativa (`PUR-000001`) y detalle de líneas.
- Autenticación de usuarios (login / signup) usando el sistema de auth de Django.
- Exportación de datos con `openpyxl` y generación de PDF con `reportlab`.

## 🗂️ Estructura del proyecto

```
proyecto_traducido/
├── billing/             # App: marcas, productos, clientes, facturas
├── purchasing/          # App: compras a proveedores
├── shared/              # Validadores y utilidades compartidas (ej. validación de cédula EC)
├── config/              # Configuración del proyecto (settings, urls, wsgi/asgi)
├── templates/           # Plantillas HTML globales
├── media/               # Archivos subidos (fotos de productos)
├── docs/
│   └── orm/             # 📘 Guía completa de comandos del ORM de Django
├── db.sqlite3           # Base de datos SQLite
├── manage.py
└── requirements.txt
```

## ⚙️ Requisitos previos

- Python 3.11+ (probado con 3.13)
- pip

## 🚀 Instalación

1. **Clonar / descomprimir el proyecto** y entrar en la carpeta:
   ```bash
   cd proyecto_traducido
   ```

2. **Crear y activar un entorno virtual:**
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Linux / Mac
   source venv/bin/activate
   ```

3. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Aplicar las migraciones** (crea/actualiza las tablas en la base de datos):
   ```bash
   python manage.py migrate
   ```

5. **Crear un superusuario** (para acceder al panel de administración):
   ```bash
   python manage.py createsuperuser
   ```

6. **Levantar el servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```

7. Abrir en el navegador:
   - App: http://127.0.0.1:8000/
   - Panel admin: http://127.0.0.1:8000/admin/

## 🧩 Apps del proyecto

| App         | Descripción                                                              |
|-------------|---------------------------------------------------------------------------|
| `billing`   | Marcas, grupos de productos, productos, proveedores, clientes y facturas |
| `purchasing`| Compras a proveedores (reutiliza `Supplier` y `Product` de `billing`)    |
| `shared`    | Validadores y mixins reutilizables (ej. validación de cédula ecuatoriana)|

## 🗄️ Modelos principales

- **Brand**, **ProductGroup**, **Supplier**, **Product** (FK a Brand/Group, M2M a Supplier)
- **Customer** ↔ **CustomerProfile** (relación uno a uno)
- **Invoice** → **InvoiceDetail** (cabecera/detalle de factura)
- **Purchase** → **PurchaseDetail** (cabecera/detalle de compra)

## 📘 Trabajar con el ORM de Django

Toda la lógica de acceso a datos (crear, leer, actualizar, eliminar) se hace a través del **ORM de Django**, sin escribir SQL manualmente.

👉 Consulta la guía completa con todos los comandos básicos en:

**[`docs/orm/README.md`](docs/orm/README.md)**

Ahí encontrarás ejemplos reales de **CRUD** (Crear, Leer, Actualizar, Eliminar) usando los modelos de este mismo proyecto, tanto desde el `shell` de Django como desde código (vistas).

## 🧪 Comandos útiles de Django

```bash
python manage.py runserver          # Levantar servidor de desarrollo
python manage.py makemigrations     # Generar migraciones a partir de cambios en los modelos
python manage.py migrate            # Aplicar migraciones a la base de datos
python manage.py createsuperuser    # Crear usuario administrador
python manage.py shell              # Abrir consola interactiva con el entorno de Django cargado
python manage.py test               # Ejecutar pruebas
```

## 📦 Dependencias principales

| Paquete    | Uso                                                |
|------------|-----------------------------------------------------|
| Django     | Framework web y ORM                                 |
| Pillow     | Manejo de imágenes (fotos de productos)             |
| openpyxl   | Exportación de datos a Excel                        |
| reportlab  | Generación de reportes en PDF                        |
| sqlparse   | Dependencia interna de Django                        |
| asgiref    | Soporte ASGI de Django                               |
| tzdata     | Datos de zonas horarias                              |

## 📝 Licencia

Proyecto educativo / interno. Ajusta esta sección según corresponda.
---

## 🆕 Nuevos Requerimientos Implementados

Se implementaron 5 requerimientos críticos sobre roles, perfil de usuario y facturación con validación de saldo. Resumen de la arquitectura y decisiones de diseño:

### 1. Asignación de Rol Automático al Registrarse
- `security/signals.py`: señal `post_save` sobre `auth.User`. Cuando se crea un usuario nuevo (p. ej. desde `/signup/`, ver `billing/views.py::signup_view` + `billing/forms.py::SignUpForm`), automáticamente:
  - Se le crea su `Profile` (ver punto 2).
  - Se le asigna el rol/grupo **"Usuario"** (se crea con `get_or_create` la primera vez, junto con sus permisos de módulo: `view_products`, `view_invoices`).
- Se conecta en `security/apps.py::SecurityConfig.ready()`.
- Los roles base (`Administrador`, `Trabajador`, `Usuario`) además se siembran vía migración de datos: `security/migrations/0003_seed_roles.py`.

### 2. Vista de Perfil ("Mis Datos") + campo `dinero`
- `security/models.py::Profile`: modelo `OneToOne` a `User` con el campo `dinero` (`DecimalField`, default `1000.00`). Nombre/Apellido/Correo se reutilizan de los campos nativos de `auth.User` (`first_name`, `last_name`, `email`) para no duplicar información.
- `security/forms.py::ProfileUpdateForm`: formulario editable de Nombre/Apellido/Correo.
- `security/views.py::ProfileView` (`/security/profile/`, name=`my_profile`): el usuario logueado ve y edita sus datos; `dinero` y `rango` (propiedad de solo lectura sobre `user.groups`) se muestran pero **no son editables** desde este formulario.
- Enlace "Mis Datos" agregado al menú de usuario en `templates/billing/base.html`.

### 3. Permisos de Productos (Ver y Filtrar solamente)
- `shared/mixins.py::StaffOrAdminRequiredMixin` (`LoginRequiredMixin` + `UserPassesTestMixin`, tal como pide el enunciado): solo permite el acceso a superusuarios o a los grupos `Administrador`/`Trabajador`.
- Aplicado a `ProductCreateView`, `ProductUpdateView` y `ProductDeleteView` en `billing/views.py`. `ProductListView`/`ProductDetailView` NO lo usan, por lo que el rango "Usuario" conserva acceso de solo lectura (con filtros).
- Los botones "Nuevo/Editar/Eliminar Producto" también se ocultan en los templates (`product_list.html`, `product_detail.html`) para ese rango (protección de UX; la protección real está en el servidor).

### 4. Gestión de Facturas propia
- `billing/models.py::Customer.user`: FK `OneToOne` opcional a `auth.User`, que vincula un Cliente de negocio con su cuenta de acceso. `Customer.get_or_create_for_user(user)` obtiene/crea ese registro la primera vez que un "Usuario" se autofactura (el campo `dni` se vuelve opcional para este caso).
- `billing/views.py::invoice_list`: si `_is_self_service_user(request.user)` (no es `Administrador`/`Trabajador`/superusuario), el queryset se filtra con `.filter(customer__user=request.user)`. Lo mismo aplica a `invoice_detail` (evita ver facturas de terceros por URL directa).
- `invoice_update`/`invoice_delete` quedan bloqueados para ese rango (solo pueden crear y consultar su propio historial).
- `billing/forms.py::InvoiceForm(hide_customer=True)`: oculta el selector de cliente para que el "Usuario" nunca pueda facturarle a otra persona.

### 5. Validación de Saldo en la Facturación
- `billing/views.py::invoice_create`: para el flujo de autoservicio, ANTES de guardar nada se calcula el total prospectivo (subtotal + IVA 15 %) a partir del formset y se compara contra `request.user.profile.dinero`:
  - Si el saldo **no alcanza** → `messages.error(request, "Saldo insuficiente para realizar la compra")`, no se crea la factura ni se descuenta stock.
  - Si el saldo **sí alcanza** → se resta el total de `profile.dinero`, la factura se guarda con `status='PAGADA'` (`Invoice.status`, nuevo campo) y se descuenta el stock normalmente, todo dentro de una transacción atómica.
- Administrador/Trabajador (facturando a un cliente de negocio) no están sujetos a esta validación.

### Migraciones nuevas
- `security/migrations/0002_profile.py`, `0003_seed_roles.py`, `0004_backfill_profiles.py`
- `billing/migrations/0005_customer_user_and_invoice_status.py`

### Notas / supuestos
- El proyecto ya usaba `django.contrib.auth.Group` + `Permission` (no un modelo de Rol propio), así que el "rango" se implementó sobre esa misma base para no romper el resto del sistema de permisos (`ModulePermissionRequiredMixin`, navbar dinámico, etc.).
- `Customer.dni` (cédula/RUC ecuatoriana) se volvió opcional (`blank=True, null=True`) porque un cliente autogenerado desde `/signup/` todavía no ha proporcionado ese dato; los clientes creados manualmente por Admin/Trabajador (`CustomerCreateView`) conservan la validación completa si se llena.
