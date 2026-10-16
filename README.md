# Sistema de monitoreo de fatiga — Línea 111

Aplicación Flask para administración, asignación de rutas, monitoreo GPS, alertas de fatiga y reportes PDF. Se puede elegir entre **MySQL/MariaDB**, **Microsoft SQL Server** o **Firebase Cloud Firestore** mediante una sola variable de configuración. Los módulos de rutas, GPS y alertas funcionan con las tres opciones.

## Requisitos

- Python 3.10 o superior (recomendado: Python 3.11).
- El motor de datos elegido y su base creada.
- Para SQL Server: Microsoft ODBC Driver 18 for SQL Server instalado.

## Instalación común

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edita `.env` localmente. Configura `FLASK_SECRET_KEY` con un valor aleatorio largo; no subas el archivo `.env` al repositorio.

## Elegir el almacenamiento

### Opción A: MySQL o MariaDB (modo original)

1. En `.env`, selecciona `DATA_BACKEND=mysql` y completa `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_DATABASE`, `MYSQL_USER` y `MYSQL_PASSWORD`.
2. En MySQL Workbench o MariaDB, ejecuta `database/schema.sql` para crear una base nueva. Si ya tienes las tablas de antes, ejecuta una vez `database/migracion_gps_alertas.sql` para añadir soporte a mapa y alertas.
3. Crea las cuentas iniciales de forma interactiva (el mismo asistente sirve para MySQL o SQL Server):

   ```powershell
   python scripts/configurar_usuarios_sql.py
   ```

### Opción B: Microsoft SQL Server

1. Asegúrate de tener el **ODBC Driver 18 for SQL Server** instalado.
2. Para una base nueva, abre `database/schema_sqlserver.sql` en SSMS y ejecútalo.
3. En `.env`, configura `DATA_BACKEND=sqlserver`, `SQLSERVER_HOST`, `SQLSERVER_PORT` y `SQLSERVER_DATABASE`. Para una instancia nombrada, ponla en `SQLSERVER_HOST` (por ejemplo `localhost\\SQLEXPRESS`) y deja `SQLSERVER_PORT` vacío. Por defecto se usa autenticación integrada de Windows (`SQLSERVER_TRUSTED=1`). Para SQL Authentication, usa `SQLSERVER_TRUSTED=0` y completa `SQLSERVER_USER` y `SQLSERVER_PASSWORD`.
4. Si tu base SQL Server ya existe y falló al crear `FK_alertas_asignaciones` con el error de múltiples rutas en cascada (Msg 1785), ejecuta una vez `database/fix_sqlserver_alertas_fk.sql` en SSMS. Luego crea usuarios con `python scripts/configurar_usuarios_sql.py` (el asistente usa el motor elegido en `DATA_BACKEND`).

El esquema SQL Server evita la doble cascada: las alertas conservan su historial y su FK a asignaciones usa `NO ACTION`. Antes de eliminar un conductor o vehículo, la aplicación desvincula sus alertas y luego elimina sus asignaciones.

### Opción C: Firebase Cloud Firestore

1. En Firebase Console, crea o elige un proyecto y habilita Cloud Firestore en modo Native.
2. Crea una cuenta de servicio con permisos mínimos de Firestore. Guarda el JSON fuera de esta carpeta, por ejemplo en `%USERPROFILE%\.firebase\serviceAccount.json`. Nunca lo publiques ni lo envíes por chat.
3. En `.env`, configura `DATA_BACKEND=firebase`, `FIREBASE_PROJECT_ID` y `GOOGLE_APPLICATION_CREDENTIALS` con la ruta local al JSON. Cada compañero usa su propio archivo de credenciales, pero el mismo `FIREBASE_PROJECT_ID` para consultar los mismos datos.
4. Crea las cuentas iniciales:

   ```powershell
   python scripts/configurar_usuarios.py
   ```

`firestore.rules` bloquea las llamadas desde clientes web; el servidor Flask accede usando Firebase Admin SDK. Consulta la documentación oficial de [Firebase Admin](https://firebase.google.com/docs/admin/setup) y [Firestore para servidores](https://firebase.google.com/docs/firestore/quickstart-server).

## Ejecutar

```powershell
python app.py
```

Abre <http://127.0.0.1:5000> e inicia sesión con las cuentas que creaste. Permite cámara y ubicación al navegador cuando se solicite. El GPS del navegador requiere localhost o HTTPS.

## Funciones incluidas

- Administración de propietario, operador, conductor y vehículos.
- Asignación de rutas guardadas o dibujadas en el mapa a un conductor y vehículo.
- Inicio y finalización del recorrido por el conductor asignado, con seguimiento GPS.
- Alertas visuales y sonoras por bostezo o cierre prolongado de ojos, con registros detallados de evento, nivel, hora, conductor, ruta, vehículo y estado.
- Reporte PDF de operación y fatiga.

Las contraseñas creadas por los asistentes se almacenan con hash. Los usuarios antiguos con contraseña en texto plano se migran al formato hash al iniciar sesión correctamente. No se incluyen credenciales de demostración en este repositorio.

La app usa un solo backend a la vez. Cambiar `DATA_BACKEND` no copia los datos entre MySQL, SQL Server y Firestore; cada opción conserva su propia base.

## Colecciones Firestore

`usuarios`, `vehiculos`, `rutas`, `asignaciones`, `ubicaciones_gps`, `alertas` y `_contadores`.

La detección visual depende de cámara, iluminación, posición del rostro y permisos del navegador. Es una ayuda de monitoreo y no sustituye descansos ni protocolos de seguridad vial.
