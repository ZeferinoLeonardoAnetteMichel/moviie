import flet as ft
import requests
from controllers.favoritoController import FavoritoController

def DashboardView(page: ft.Page):
    fav_ctrl = FavoritoController()
    usuario_actual = getattr(
        page,
        "user_data",
        {
            "id_usuario": 1,
            "nombre": "Usuario"
        }
    )
    id_usuario = usuario_actual.get("id_usuario")
    OMDB_API_KEY = "d55033dc"
    URL_BASE = "https://www.omdbapi.com/"

    PLATAFORMAS_MAP = {
        "batman": ["Max"],
        "spiderman": ["Netflix"],
        "avengers": ["Disney+"],
        "interstellar": ["Prime Video"],
        "joker": ["Max"]
    }

    STREAMING_BADGES = {
        "Netflix": {
            "bg": ft.Colors.RED_50,
            "color": ft.Colors.RED_700
        },
        "Max": {
            "bg": ft.Colors.BLUE_50,
            "color": ft.Colors.BLUE_700
        },
        "Disney+": {
            "bg": ft.Colors.INDIGO_50,
            "color": ft.Colors.INDIGO_700
        },
        "Prime Video": {
            "bg": ft.Colors.CYAN_50,
            "color": ft.Colors.CYAN_700
        }
    }

    def obtener_plataformas(titulo):
        titulo = titulo.lower()
        for clave, plataformas in PLATAFORMAS_MAP.items():
            if clave in titulo:
                return plataformas
        return ["Netflix"]

    def mostrar_snackbar(
        mensaje,
        color=ft.Colors.GREEN
    ):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(mensaje),
            bgcolor=color
        )
        page.snack_bar.open = True
        page.update()

    def agregar_a_mysql(
        titulo,
        anio,
        rating,
        plataforma
    ):
        exito, msg = fav_ctrl.guardar(
            id_usuario,
            titulo,
            anio,
            rating,
            plataforma
        )
        if exito:
            mostrar_snackbar(msg)
            cargar_favoritos_mysql()
        else:
            mostrar_snackbar(
                msg,
                ft.Colors.RED
            )
    catalogo = ft.Row(
    scroll=ft.ScrollMode.AUTO,
    spacing=20
)
    estado = ft.Text()
    
    def buscar_peliculas(texto):
        if not texto.strip():
            return
        catalogo.controls.clear()
        try:
            params = {
                "apikey": OMDB_API_KEY,
                "s": texto,
                "type": "movie"
            }
            response = requests.get(
                URL_BASE,
                params=params
            ).json()
            if response.get("Response") == "True":
                for peli in response["Search"][:8]:
                    titulo = peli["Title"]
                    anio = peli["Year"]
                    poster = peli["Poster"]
                    plataformas = obtener_plataformas(titulo)
                    chips = []
                    for plat in plataformas:
                        estilo = STREAMING_BADGES.get(plat)
                        chips.append(
                            ft.Container(
                                content=ft.Text(
                                    plat,
                                    size=10,
                                    weight="bold",
                                    color=estilo["color"]
                                ),
                                bgcolor=estilo["bg"],
                                padding=5,
                                border_radius=10
                            )
                        )
                    url_poster = poster if poster != "N/A" else "https://via.placeholder.com/210x260?text=Sin+Imagen"
                    card = ft.Card(
                        elevation=5,
                        content=ft.Container(
                            width=230,
                            height=460,
                            padding=12,
                            border_radius=15,
                            bgcolor=ft.Colors.WHITE,
                            content=ft.Column(
                                [
                    ft.Container(
                        height=240,
                        width=210,
                        border_radius=10,
                        clip_behavior=ft.ClipBehavior.HARD_EDGE, 
                        content=ft.Image(
                        src=url_poster,
                        fit="cover", 
                    ),
                ),
                                    ft.Column(
                                        [
                                            ft.Text(
                                                titulo,
                                                size=15,
                                                weight="bold",
                                                text_align=ft.TextAlign.CENTER,
                                                max_lines=2,
                                                overflow=ft.TextOverflow.ELLIPSIS,
                                            ),
                                            ft.Text(
                                                f"Año: {anio}",
                                                size=12,
                                                color=ft.Colors.GREY_700,
                                            ),
                                            ft.Row(
                                                chips,
                                                alignment=ft.MainAxisAlignment.CENTER,
                                                wrap=True,
                                                spacing=4
                                            ),
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=4,
                                        expand=True, 
                                    ),
                                    ft.ElevatedButton(
                                        "Agregar a favoritos",
                                        icon=ft.Icons.FAVORITE,
                                        bgcolor=ft.Colors.PURPLE_300,
                                        color=ft.Colors.WHITE,
                                        width=200,
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=20),
                                            padding=10,
                                        ),
                                        on_click=lambda e,
                                        t=titulo,
                                        a=anio,
                                        p=plataformas[0]: agregar_a_mysql(
                                            t, a, "N/A", p
                                        )
                                    )
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=8
                            )
                        )
                    )
                    catalogo.controls.append(card)
                estado.value = ""
            else:
                estado.value = "No se encontraron películas"
            page.update()
        except Exception as e:
            estado.value = f"Error: {e}"
            page.update()
    buscador = ft.TextField(
        hint_text="Buscar película...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=12,
        on_submit=lambda e:
        buscar_peliculas(
            buscador.value
        )
    )
    tabla_favoritos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Título")),
            ft.DataColumn(ft.Text("Año")),
            ft.DataColumn(ft.Text("Rating")),
            ft.DataColumn(ft.Text("Plataforma")),
            ft.DataColumn(ft.Text("Acciones"))
        ],
        rows=[]
    )

    def borrar_de_mysql(id_favorito):
        exito, msg = fav_ctrl.borrar(id_favorito)
        if exito:
            mostrar_snackbar(msg)
            cargar_favoritos_mysql()

    def editar_en_mysql(
        id_favorito,
        plataforma_actual
    ):
        dropdown = ft.Dropdown(
            width=200,
            value=plataforma_actual,
            options=[
                ft.dropdown.Option("Netflix"),
                ft.dropdown.Option("Prime Video"),
                ft.dropdown.Option("Disney+"),
                ft.dropdown.Option("Max")
            ]
        )
        def guardar_cambios(e):
            exito, msg = fav_ctrl.actualizar(
                id_favorito,
                dropdown.value
            )
            dialogo.open = False
            if exito:
                mostrar_snackbar(msg)
                cargar_favoritos_mysql()
            page.update()
        dialogo = ft.AlertDialog(
            title=ft.Text(
                "Editar Plataforma"
            ),
            content=dropdown,
            actions=[
                ft.TextButton(
                    "Guardar",
                    on_click=guardar_cambios
                )
            ]
        )
        page.dialog = dialogo
        dialogo.open = True
        page.update()

    def cargar_favoritos_mysql():
        tabla_favoritos.rows.clear()
        datos = fav_ctrl.listar(id_usuario)
        for f in datos:
            fila = ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.Text(f["titulo"])
                    ),
                    ft.DataCell(
                        ft.Text(f["anio"])
                    ),
                    ft.DataCell(
                        ft.Text(f["rating"])
                    ),
                    ft.DataCell(
                        ft.Text(f["plataforma"])
                    ),
                    ft.DataCell(
                        ft.Row(
                            [
                                ft.IconButton(
                                    ft.Icons.EDIT,
                                    icon_color=ft.Colors.BLUE,
                                    on_click=lambda e,
                                    item=f:
                                    editar_en_mysql(
                                        item["id_favorito"],
                                        item["plataforma"]
                                    )
                                ),
                                ft.IconButton(
                                    ft.Icons.DELETE,
                                    icon_color=ft.Colors.RED,
                                    on_click=lambda e,
                                    item=f:
                                    borrar_de_mysql(
                                        item["id_favorito"]
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
            tabla_favoritos.rows.append(fila)
        page.update()
    cargar_favoritos_mysql()

    return ft.View(
        route="/dashboard",
        appbar=ft.AppBar(
            title=ft.Text("Moviie"),
            bgcolor=ft.Colors.PURPLE_200,
            color=ft.Colors.WHITE,
            actions=[
                ft.IconButton(
                    ft.Icons.LOGOUT,
                    on_click=lambda e: page.go("/")
                )
            ]
        ),
        controls=[
            ft.Container(
                padding=20,
                expand=True,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                    scroll=ft.ScrollMode.AUTO, 
                    controls=[
                        ft.Text(
                            f"Hola {usuario_actual['nombre']}",
                            size=30,
                            weight="bold",
                            color="purple"
                        ),                        
                        ft.Container(
                            width=500,
                            content=buscador
                        ),                        
                        estado,
                        catalogo,                        
                        ft.Divider(height=40, thickness=2),                        
                        ft.Text(
                            "Favoritas:",
                            size=22,
                            weight="bold",
                            color="purple"
                        ),                        
                        ft.Container(
                            content=tabla_favoritos,
                            margin=ft.Margin(left=0, top=0, right=0, bottom=40)
                        )
                    ]
                )
            )
        ]
    )