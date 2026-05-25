from .databaseModel import Database
class FavoritoModel:

    def __init__(self):
        self.db = Database()

    def agregar(self, id_usuario, titulo, anio, rating, plataforma):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            sql = """
            INSERT INTO pelicula_favorita
            (id_usuario, titulo, anio, rating, plataforma)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(
                sql,
                (id_usuario, titulo, anio, rating, plataforma)
            )
            conn.commit()
            return True, "Película agregada correctamente"
        except Exception as e:
            return False, f"Error: {e}"
        finally:
            conn.close()

    def obtener_por_usuario(self, id_usuario):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            sql = """
            SELECT *
            FROM pelicula_favorita
            WHERE id_usuario = %s
            """
            cursor.execute(sql, (id_usuario,))
            return cursor.fetchall()
        except Exception:
            return []
        finally:
            conn.close()

    def actualizar_plataforma(
        self,
        id_favorito,
        nueva_plataforma
    ):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            sql = """
            UPDATE pelicula_favorita
            SET plataforma = %s
            WHERE id_favorito = %s
            """
            cursor.execute(
                sql,
                (nueva_plataforma, id_favorito)
            )
            conn.commit()
            return True, "Favorito actualizado"
        except Exception as e:
            return False, f"Error: {e}"
        finally:
            conn.close()

    def eliminar(self, id_favorito):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            sql = """
            DELETE FROM pelicula_favorita
            WHERE id_favorito = %s
            """
            cursor.execute(sql, (id_favorito,))
            conn.commit()
            return True, "Favorito eliminado"
        except Exception as e:
            return False, f"Error: {e}"
        finally:
            conn.close()