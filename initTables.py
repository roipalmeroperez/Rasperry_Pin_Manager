import json
import mysql.connector

# Configuration
conf_file = open('./config.json')
conf = json.loads(conf_file.read())

# Configuración de MySQL
configBD = {
    'user': conf["DATABASE_USER"],
    'password': conf["DATABASE_PASSWORD"],
    'host': conf["DATABASE_HOST"],
    'database': conf["DATABASE_DB"]
}

def createTables():
    try:
        # Conectarse a la base de datos
        cnx = mysql.connector.connect(**configBD)
        cursor = cnx.cursor()
        
        # Leer el archivo SQL
        with open('schema.sql', 'r') as f:
            sql = f.read()
        
        # Ejecutar el archivo SQL
        cursor.execute(sql)
        cnx.commit()
        print("Tablas creadas con éxito.")
    
    except Exception as e:
        print(f"Error creando tablas: {e}")
    
    finally:
        # Cerrar la conexión
        cursor.close()
        cnx.close()

if __name__ == '__main__': 
    createTables()
