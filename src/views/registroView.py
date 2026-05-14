import flet as ft
import re
from models.schemasModel import UsuarioSchema  

def RegisterView(page: ft.Page, auth_controller):
    
    nombre = ft.TextField(
        label="Nombre(s)",
        prefix_icon=ft.Icons.PERSON,
        width=400,
        border_radius=10,
        border_color="purple"
    )
    
    apellido = ft.TextField(
        label="Apellidos",
        prefix_icon=ft.Icons.PERSON,
        width=400,
        border_radius=10,
        border_color="purple"
    )
    
    email = ft.TextField(
        label="Correo electrónico",
        prefix_icon=ft.Icons.EMAIL,
        width=400,
        border_radius=10,
        border_color="purple",
        keyboard_type=ft.KeyboardType.EMAIL
    )
    
    password = ft.TextField(
        label="Contraseña",
        prefix_icon=ft.Icons.LOCK,
        password=True,
        can_reveal_password=True,
        width=400,
        border_radius=10,
        border_color="purple"
    )
    
    confirm_password = ft.TextField(
        label="Confirmar contraseña",
        prefix_icon=ft.Icons.LOCK,
        password=True,
        can_reveal_password=True,
        width=400,
        border_radius=10,
        border_color="purple"
    )
    
    mensaje = ft.Text("", color="red", size=12)
    
    def mostrar_snackbar(mensaje_texto, color=ft.Colors.GREEN):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(mensaje_texto),
            bgcolor=color,
            duration=2000,
        )
        page.snack_bar.open = True
        page.update()
    
    def registrar_click(e):
        if not nombre.value or not email.value or not password.value or not confirm_password.value:
            mensaje.value = "Todos los campos son obligatorios"
            mensaje.color = "red"
            page.update()
            return
        
        if password.value != confirm_password.value:
            mensaje.value = "Las contraseñas no coinciden"
            mensaje.color = "red"
            page.update()
            return
        
        if len(password.value) < 6:
            mensaje.value = "La contraseña debe tener al menos 6 caracteres"
            mensaje.color = "red"
            page.update()
            return
        
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email.value):
            mensaje.value = "Correo electrónico inválido"
            mensaje.color = "red"
            page.update()
            return
        
        usuario_data = UsuarioSchema(
            nombre=nombre.value,
            apellido=apellido.value,
            email=email.value,
            password=password.value
        )
        
        exito, msg = auth_controller.registrar(usuario_data)
        
        if exito:
            mostrar_snackbar("¡Registro exitoso! Ahora inicia sesión", ft.Colors.GREEN)
            nombre.value = ""
            email.value = ""
            password.value = ""
            confirm_password.value = ""
            mensaje.value = ""
            page.update()
            page.go("/")
        else:
            mensaje.value = msg or "Error al registrar usuario"
            mensaje.color = "red"
            page.update()
    
    def ir_login(e):
        page.go("/")
    
    btn_registrar = ft.ElevatedButton(
        "Registrarse",
        width=250,
        on_click=registrar_click,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.PURPLE_200,
            color=ft.Colors.WHITE,
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
    )
    
    btn_login = ft.TextButton(
        "¿Ya tienes cuenta? Inicia sesión",
        on_click=ir_login
    )
    
    return ft.View(
        route="/register",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        appbar=ft.AppBar(
            title=ft.Text("SIGE - Registro"),
            bgcolor=ft.Colors.PURPLE_200,
            color=ft.Colors.WHITE,
            leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/"))
        ),
        controls=[
            ft.Column(
                [
                    ft.Text("Crear Nueva Cuenta", size=35, weight="bold",color="purple"),
                    ft.Container(height=10),
                    nombre,
                    apellido,
                    email,
                    password,
                    confirm_password,
                    mensaje,
                    ft.Container(height=10),
                    btn_registrar,
                    ft.Container(height=10),
                    btn_login
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True,
                spacing=15
            )
        ]
    )