import mysql.connector

class FavoritoController:
    def __init__(self):
        self.config = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': '',
            'database': 'catalogo'
        }

    def guardar(self, id_usuario, titulo, anio, rating, plataforma_nombre):
        conexion = mysql.connector.connect(**self.config)
        cursor = conexion.cursor()
        try:
            conexion.start_transaction()
            query_plat = "SELECT id_plataforma FROM plataforma_streaming WHERE nombre = %s"
            cursor.execute(query_plat, (plataforma_nombre,))
            resultado_plat = cursor.fetchone()
            if resultado_plat:
                id_plataforma = resultado_plat[0]
            else:
                insert_plat = "INSERT INTO plataforma_streaming (nombre) VALUES (%s)"
                cursor.execute(insert_plat, (plataforma_nombre,))
                id_plataforma = cursor.lastrowid
            insert_contenido = """
                INSERT INTO contenido (título, año_lanzamiento, tipo_contenido, género) 
                VALUES (%s, %s, 'Película', 'N/A')
            """
            cursor.execute(insert_contenido, (titulo, anio))
            id_contenido = cursor.lastrowid 
            insert_peli = "INSERT INTO pelicula (id_pelicula, recaudación, estudio) VALUES (%s, 0.00, 'Desconocido')"
            cursor.execute(insert_peli, (id_contenido,))
            insert_disp = """
                INSERT INTO disponibilidad (id_contenido, id_plataforma, visualización_del_enlace, calidad, idioma) 
                VALUES (%s, %s, '#', 'HD', 'Español')
            """
            cursor.execute(insert_disp, (id_contenido, id_plataforma))
            insert_fav = """
                INSERT INTO favoritos (id_usuario, id_contenido, fecha_agregado) 
                VALUES (%s, %s, CURDATE())
            """
            cursor.execute(insert_fav, (id_usuario, id_contenido))
            insert_espejo = """
                INSERT INTO pelicula_favorita (id_usuario, titulo, anio, rating, plataforma) 
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_espejo, (id_usuario, titulo, anio, rating, plataforma_nombre))

            conexion.commit()
            return True, "Película añadida perfectamente"
            
        except mysql.connector.Error as err:
            conexion.rollback()
            print("\n============ ERROR EN GUARDAR PELICULA ============")
            print(f"Código de error: {err.errno}")
            print(f"Mensaje de la Base de Datos: {err.msg}")
            print("===================================================\n")
            
            try:
                print("Intentando guardado directo de emergencia en pelicula_favorita...")
                insert_emergencia = "INSERT INTO pelicula_favorita (id_usuario, titulo, anio, rating, plataforma) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(insert_emergencia, (id_usuario, titulo, anio, rating, plataforma_nombre))
                conexion.commit()
                return True, "Guardado en lista de favoritos (Tablas relacionales omitidas)"
            except Exception as e_err:
                print(f"Error crítico de emergencia: {e_err}")
                return False, f"Error en la base de datos: {err.msg}"
        finally:
            cursor.close()
            conexion.close()

    def guardar_serie(self, id_usuario, titulo, anio, rating, plataforma_nombre):
        conexion = mysql.connector.connect(**self.config)
        cursor = conexion.cursor()
        try:
            conexion.start_transaction()
            query_plat = "SELECT id_plataforma FROM plataforma_streaming WHERE nombre = %s"
            cursor.execute(query_plat, (plataforma_nombre,))
            resultado_plat = cursor.fetchone()
            if resultado_plat:
                id_plataforma = resultado_plat[0]
            else:
                insert_plat = "INSERT INTO plataforma_streaming (nombre) VALUES (%s)"
                cursor.execute(insert_plat, (plataforma_nombre,))
                id_plataforma = cursor.lastrowid
            insert_contenido = """
                INSERT INTO contenido (título, año_lanzamiento, tipo_contenido, género) 
                VALUES (%s, %s, 'Serie', 'N/A')
            """
            cursor.execute(insert_contenido, (titulo, anio))
            id_contenido = cursor.lastrowid 
            insert_tabla_serie = """
                INSERT INTO serie (id_serie, cantidad_temporadas, estado_serie) 
                VALUES (%s, 1, 'Activa')
            """
            cursor.execute(insert_tabla_serie, (id_contenido,))
            insert_disp = """
                INSERT INTO disponibilidad (id_contenido, id_plataforma, visualización_del_enlace, calidad, idioma) 
                VALUES (%s, %s, '#', 'HD', 'Español')
            """
            cursor.execute(insert_disp, (id_contenido, id_plataforma))
            insert_fav = """
                INSERT INTO favoritos (id_usuario, id_contenido, fecha_agregado) 
                VALUES (%s, %s, CURDATE())
            """
            cursor.execute(insert_fav, (id_usuario, id_contenido))
            insert_espejo = """
                INSERT INTO pelicula_favorita (id_usuario, titulo, anio, rating, plataforma) 
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_espejo, (id_usuario, titulo, anio, rating, plataforma_nombre))

            conexion.commit()
            return True, "Serie añadida perfectamente"
            
        except mysql.connector.Error as err:
            conexion.rollback()
            print("\n============ ERROR EN GUARDAR SERIE ============")
            print(f"Código de error: {err.errno}")
            print(f"Mensaje de la Base de Datos: {err.msg}")
            print("===================================================\n")
            
            try:
                print("Intentando guardado directo de emergencia de serie...")
                insert_emergencia = "INSERT INTO pelicula_favorita (id_usuario, titulo, anio, rating, plataforma) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(insert_emergencia, (id_usuario, titulo, anio, rating, plataforma_nombre))
                conexion.commit()
                return True, "Serie guardada en lista de favoritos (Tablas relacionales omitidas)"
            except Exception as e_err:
                print(f"Error crítico de emergencia serie: {e_err}")
                return False, f"Error en la base de datos: {err.msg}"
        finally:
            cursor.close()
            conexion.close()

    def listar(self, id_usuario):
        conexion = mysql.connector.connect(**self.config)
        cursor = conexion.cursor(dictionary=True)
        try:
            query = "SELECT id_favorito, titulo, anio, rating, plataforma FROM pelicula_favorita WHERE id_usuario = %s"
            cursor.execute(query, (id_usuario,))
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error al listar: {err}")
            return []
        finally:
            cursor.close()
            conexion.close()

    def actualizar(self, id_favorito, nueva_plataforma):
        conexion = mysql.connector.connect(**self.config)
        cursor = conexion.cursor()
        try:
            query = "UPDATE pelicula_favorita SET plataforma = %s WHERE id_favorito = %s"
            cursor.execute(query, (nueva_plataforma, id_favorito))
            conexion.commit()
            return True, "Plataforma actualizada correctamente"
        except mysql.connector.Error as err:
            print(f"Error al actualizar: {err}")
            return False, f"No se pudo actualizar: {err.msg}"
        finally:
            cursor.close()
            conexion.close()

    def borrar(self, id_favorito):
        conexion = mysql.connector.connect(**self.config)
        cursor = conexion.cursor()
        try:
            query = "DELETE FROM pelicula_favorita WHERE id_favorito = %s"
            cursor.execute(query, (id_favorito,))
            conexion.commit()
            return True, "Eliminado de tus favoritos"
        except mysql.connector.Error as err:
            print(f"Error al borrar: {err}")
            return False, f"No se pudo eliminar: {err.msg}"
        finally:
            cursor.close()
            conexion.close()