import flet as ft

def LoginView(page: ft.Page, auth_controller):

    def rellenar_campos(datos):
        correo.value = datos.get('email', '')
        contraseña.focus()
        page.update()

    correo = ft.TextField(
        label="Correo electrónico",
        prefix_icon=ft.Icons.PERSON,
        width=400,
        border_radius=10,
        border_color="purple",
        keyboard_type=ft.KeyboardType.EMAIL
    )

    contraseña = ft.TextField(
        label="Contraseña",
        prefix_icon=ft.Icons.KEY,
        password=True,
        can_reveal_password=True,
        width=400,
        border_radius=10,
        border_color="purple"
    )
    
    mensaje = ft.Text("", color="red")

    def mostrar_snackbar(mensaje_texto, color=ft.Colors.GREEN):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(mensaje_texto),
            bgcolor=color,
            duration=2000,
        )
        page.snack_bar.open = True
        page.update()

    def login_click(e):
        if not correo.value or not contraseña.value:
            mensaje.value = "Por favor, llene todos los campos"
            mensaje.color = "red"
            page.update()
            return
        
        user, msg = auth_controller.login(correo.value, contraseña.value, page)
        
        if user:
            try:
                cuentas = page.client_storage.get("perfiles_activos") or []
                if not any(c['id'] == user['id_usuario'] for c in cuentas):
                    cuentas.append({
                        "id": user['id_usuario'],
                        "nombre": user['nombre'],
                        "email": user['email'],
                    })
            except Exception as ex:
                print(f"Error guardando perfil localmente: {ex}")

            page.user_data = user
            mostrar_snackbar("¡Sesión iniciada correctamente!", ft.Colors.GREEN)
            page.go("/dashboard")
        else:
            mensaje.value = msg
            mensaje.color = "red"
            page.update()

    iniciar_sesion = ft.ElevatedButton(
        "Iniciar sesión",
        width=250,
        on_click=login_click,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.PURPLE_200,
            color=ft.Colors.WHITE,
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
    )
    
    btn_registro = ft.TextButton(
        "¿No tienes cuenta? Regístrate",
        on_click=lambda _: page.go("/register")
    )
    
    contraseña.on_submit = login_click

    return ft.View(
        route="/",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        appbar=ft.AppBar(
            title=ft.Text("SIGE - Login"),
            bgcolor=ft.Colors.PURPLE_200,
            color=ft.Colors.WHITE
        ),
        controls=[
            ft.Column(
                [
                    ft.Text("Acceso al Sistema", size=35, weight="bold", color="purple"),
                    ft.Container(height=10),
                    correo,
                    ft.Container(height=10),
                    contraseña,
                    ft.Container(height=10),
                    mensaje,
                    ft.Container(height=10),
                    ft.Row(
                        [iniciar_sesion],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Container(height=10),
                    btn_registro
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True,
                spacing=10
            )
        ]
    )

