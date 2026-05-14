from models.UserModel import UsuarioModel

class AuthController:
    def __init__(self):
        self.usuario_model = UsuarioModel()

    def login(self, email, password, page): 
        try:
            user_db = self.usuario_model.validar_login(email, password)

            if not user_db:
                return None, "Correo o contraseña incorrectos"

            user = {
                "id_usuario": user_db["id_usuario"],
                "nombre": user_db["nombre"],
                "apellido": user_db["apellido"],
                "email": user_db["email"],
                "ultimo_acceso": user_db.get("ultimo_acceso", "Reciente"),
            }

            self.guardar_perfil_en_historial(page, user)

            return user, "Login exitoso"

        except Exception as e:
            return None, f"Error en login: {str(e)}"
    
    def guardar_perfil_en_historial(self, page, user_data):
        """Lógica para recordar la cuenta en el dispositivo"""
        try:
            cuentas = page.client_storage.get("perfiles_activos") or []
            
            nuevo_perfil = {
                "id": user_data['id_usuario'],
                "nombre": user_data['nombre'],
                "email": user_data['email'],
                "fecha": user_data['ultimo_acceso'],
                "foto": user_data['foto_perfil']
            }
            
            if not any(p['id'] == nuevo_perfil['id'] for p in cuentas):
                cuentas.append(nuevo_perfil)
        except Exception as e:
            print(f"No se pudo guardar el perfil local: {e}")

    def registrar(self, usuario_data):
        try:
            if self.usuario_model.email_existe(usuario_data.email):
                return False, "El correo electrónico ya está registrado"
            exito = self.usuario_model.registrar(usuario_data)
            
            if exito:
                return True, "Usuario registrado exitosamente"
            else:
                return False, "Error al registrar usuario"
                
        except Exception as e:
            return False, f"Error en registro: {str(e)}"

def login_exitoso(page, user_data): 
    page.user_data = user_data
    page.go("/dashboard")