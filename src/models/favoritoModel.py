from .databaseModel import Database

class FavoritoModel:
    def __init__(self):
        self.db = Database()

    def agregar(self, id_usuario, titulo, anio, rating, plataforma):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO pelicula_favorita (id_usuario, titulo, anio, rating, plataforma) VALUES (%s, %s, %s, %s, %s)",
                (id_usuario, titulo, anio, rating, plataforma)
            )
            conn.commit()
            return True, "Guardado en MySQL"
        except Exception as e:
            return False, f"Error: {str(e)}"
        finally:
            conn.close()

    def obtener_por_usuario(self, id_usuario):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM pelicula_favorita WHERE id_usuario = %s", (id_usuario,))
            return cursor.fetchall()
        except Exception as e:
            return []
        finally:
            conn.close()

    def actualizar_plataforma(self, id_favorito, nueva_plataforma):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE pelicula_favorita SET plataforma = %s WHERE id_favorito = %s", (nueva_plataforma, id_favorito))
            conn.commit()
            return True, "Actualizado en MySQL"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    def eliminar(self, id_favorito):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM pelicula_favorita WHERE id_favorito = %s", (id_favorito,))
            conn.commit()
            return True, "Eliminado de MySQL"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()