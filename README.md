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
