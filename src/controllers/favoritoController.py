from models.favoritoModel import FavoritoModel

class FavoritoController:
    def __init__(self):
        self.model = FavoritoModel()

    def listar(self, id_usuario):
        return self.model.obtener_por_usuario(id_usuario)

    def guardar(self, id_usuario, titulo, anio, rating, plataforma):
        return self.model.agregar(id_usuario, titulo, anio, rating, plataforma)

    def actualizar(self, id_favorito, nueva_plataforma):
        return self.model.actualizar_plataforma(id_favorito, nueva_plataforma)

    def borrar(self, id_favorito):
        return self.model.eliminar(id_favorito)