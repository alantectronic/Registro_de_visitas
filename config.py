import os

PATH = os.path.abspath(__file__).replace('\\', '/')
ROOT_MAIN = os.path.dirname(PATH)

DATA_CONFIG = {
    "var_value_1": "Pasi\u00f3n",
    "var_value_2": "Email",
    "var_value_3": "Nombre",
    "var_value_4": "Tel\u00e9fono",
    "bussiness_name": "Corporaci\u00f3n Tectronic",
    "path_dat": f"{ROOT_MAIN}/assets/data.csv",
    "path_logo": f"{ROOT_MAIN}/assets/Logo.png",
    "name_GoogleSheet": "Data Posada (Responses)",
    "jsonFile": f"{ROOT_MAIN}/assets/tectronic-2fdf637b4bc6.json",
    "path_tag": f"{ROOT_MAIN}/assets/etiqueta.png",
    "var": "False",
    "help": "Este software esta configurado para etiquetas de 76mm x 51mm, con el fin de lograr un control de los visitantes de la empresa. Su registros quedan grabados en un archivo Gooogle Sheets el cual puede ser utilizado con fines anal\u00edticos o para extraer reportes. Es recomendable no modificar este archivo y extraer copias cada vez que necessiten una modificaci\u00f3n",
    "about": {
        "author": "Corporaci\u00f3n Tectronic",
        "version": "1.0.0",
        "support": "joetectronic@gmail.com"
    }
}

