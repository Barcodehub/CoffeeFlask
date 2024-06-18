# Declarando nombre de la aplicación e inicializando, crear la aplicación Flask
from app import app

# Importando todos mis Routers (Rutas)
from routers.router_login import *
from routers.router_home import *
from routers.router_edicion import *
from routers.router_page_not_found import *


# Ejecutando el objeto Flask
if __name__ == '__main__':
    init_scheduler(app)
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
    #app.run(debug=True, port=5000)
