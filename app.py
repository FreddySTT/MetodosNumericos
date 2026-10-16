from flask import Flask, render_template
from config import Config

if Config.DATA_BACKEND == 'firebase':
    from modules.administrador.routes import admin_bp
    from modules.monitoreo.routes import monitoreo_bp
    from modules.alertas_fatiga.routes import alertas_bp
elif Config.DATA_BACKEND in ('mysql', 'sqlserver'):
    from modules.administrador.routes_sql import admin_bp
    from modules.monitoreo.routes_sql import monitoreo_bp
    from modules.alertas_fatiga.routes_sql import alertas_bp
else:
    raise RuntimeError('DATA_BACKEND debe ser mysql, sqlserver o firebase.')

app = Flask(__name__)
app.config.from_object(Config)
if not app.config.get('SECRET_KEY'):
    raise RuntimeError('Falta FLASK_SECRET_KEY. Copie .env.example a .env y configure una clave local.')

# Registrar Blueprints
app.register_blueprint(admin_bp)
app.register_blueprint(monitoreo_bp)
app.register_blueprint(alertas_bp)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False, port=5000)
