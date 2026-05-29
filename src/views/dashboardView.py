import flet as ft
import requests
from controllers.favoritoController import FavoritoController

def DashboardView(page: ft.Page):
    # --- 1. CONFIGURACIÓN INICIAL Y CONTROLADORES ---
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

    # --- 2. MAPEOS Y DICCIONARIOS DE ESTILO ---
    PLATAFORMAS_MAP = {
        "batman": ["Max"],
        "spiderman": ["Netflix"],
        "avengers": ["Disney+"],
        "interstellar": ["Prime Video"],
        "joker": ["Max"],
        "breaking bad": ["Netflix"],
        "stranger things": ["Netflix"]
    }

    STREAMING_BADGES = {
        "Netflix": {"bg": ft.Colors.RED_50, "color": ft.Colors.RED_700},
        "Max": {"bg": ft.Colors.BLUE_50, "color": ft.Colors.BLUE_700},
        "Disney+": {"bg": ft.Colors.INDIGO_50, "color": ft.Colors.INDIGO_700},
        "Prime Video": {"bg": ft.Colors.CYAN_50, "color": ft.Colors.CYAN_700}
    }

    # --- 3. COMPONENTES INTERACTIVOS PERSONALIZADOS ---
    class BarraEstrellas(ft.Container):
        def __init__(self):
            super().__init__()
            self.rating_actual = 5  
            self.estrellas_ui = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=2)
            self.content = self.estrellas_ui
            self.actualizar_estrellas()

        def cambiar_rating(self, nuevo_rating):
            self.rating_actual = nuevo_rating
            self.actualizar_estrellas()
            self.update()

        def actualizar_estrellas(self):
            self.estrellas_ui.controls.clear()
            for i in range(1, 6):
                def asignar_click(idx=i):
                    return lambda e: self.cambiar_rating(idx)
                
                es_activa = i <= self.rating_actual
                self.estrellas_ui.controls.append(
                    ft.IconButton(
                        icon=ft.Icons.STAR if es_activa else ft.Icons.STAR_BORDER,
                        icon_color=ft.Colors.AMBER_600 if es_activa else ft.Colors.GREY_400,
                        icon_size=20,
                        padding=0,
                        on_click=asignar_click()
                    )
                )

    # --- 4. CONTROLES PRINCIPALES DE LA UI ---
    catalogo = ft.Row(scroll=ft.ScrollMode.AUTO, spacing=20)
    catalogo_favoritos = ft.Row(scroll=ft.ScrollMode.AUTO, spacing=20)
    estado = ft.Text()

    # --- 5. FUNCIONES AUXILIARES Y LÓGICA DE INTERACCIÓN ---
    def obtener_plataformas(titulo):
        titulo = titulo.lower()
        for clave, plataformas in PLATAFORMAS_MAP.items():
            if clave in titulo:
                return plataformas
        return ["Netflix"]

    def mostrar_snackbar(mensaje, color=ft.Colors.BLUE_900):
        page.snack_bar = ft.SnackBar(content=ft.Text(mensaje), bgcolor=color)
        page.snack_bar.open = True
        page.update()

    def cerrar_dialogo(dialogo):
        dialogo.open = False
        page.update()

    def ver_detalles_pelicula(imdb_id):
        try:
            params = {"apikey": OMDB_API_KEY, "i": imdb_id, "plot": "full"}
            peli = requests.get(URL_BASE, params=params).json()
            
            if peli.get("Response") == "True":
                dialogo_detalles = ft.AlertDialog(
                    title=ft.Text(peli.get("Title"), weight="bold", size=22),
                    content=ft.Container(
                        width=450,
                        content=ft.Column(
                            [
                                ft.Row([
                                    ft.Text(f"📅 {peli.get('Year')}", size=12, weight="bold"),
                                    ft.Text(f"⏳ {peli.get('Runtime')}", size=12, weight="bold"),
                                    ft.Text(f"⭐ {peli.get('imdbRating')}", size=12, weight="bold", color=ft.Colors.AMBER_700),
                                ], spacing=15),
                                ft.Divider(),
                                ft.Text("Sinopsis:", weight="bold", size=14, color=ft.Colors.BLUE_900),
                                ft.Text(peli.get("Plot"), size=13, max_lines=6, overflow=ft.TextOverflow.ELLIPSIS),
                                ft.Container(height=5),
                                ft.Text(f"Director/Creador: {peli.get('Director')}", size=12, weight="bold"),
                                ft.Text(f"Elenco: {peli.get('Actors')}", size=12, color=ft.Colors.GREY_700),
                            ],
                            tight=True,
                            spacing=8
                        )
                    ),
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialogo(dialogo_detalles))
                    ]
                )
                page.dialog = dialogo_detalles
                dialogo_detalles.open = True
                page.update()
        except Exception as ex:
            mostrar_snackbar(f"Error al cargar detalles: {ex}", ft.Colors.RED_ACCENT)

    # Lógica inteligente para decidir si guarda Película o Serie
    def agregar_a_mysql(titulo, anio, rating, plataforma, tipo_contenido):
        if tipo_contenido == "series":
            exito, msg = fav_ctrl.guardar_serie(id_usuario, titulo, anio, str(rating), plataforma)
        else:
            exito, msg = fav_ctrl.guardar(id_usuario, titulo, anio, str(rating), plataforma)
            
        if exito:
            mostrar_snackbar(msg)
            cargar_favoritos_mysql()
        else:
            mostrar_snackbar(msg, ft.Colors.RED_ACCENT)

    def buscar_peliculas(texto):
        if not texto.strip():
            return
        catalogo.controls.clear()
        buscador.value = texto
        page.update()
        try:
            # Quitamos type="movie" para que busque películas Y series juntas de forma híbrida
            params = {"apikey": OMDB_API_KEY, "s": texto}
            response = requests.get(URL_BASE, params=params).json()
            if response.get("Response") == "True":
                for peli in response["Search"][:8]:
                    titulo = peli["Title"]
                    anio = peli["Year"]
                    poster = peli["Poster"]
                    imdb_id = peli["imdbID"]
                    tipo_contenido = peli["Type"] # Puede ser 'movie' o 'series'
                    
                    plataformas = obtener_plataformas(titulo)
                    
                    chips = []
                    for plat in plataformas:
                        estilo = STREAMING_BADGES.get(plat, {"bg": ft.Colors.GREY_200, "color": ft.Colors.GREY_800})
                        chips.append(
                            ft.Container(
                                content=ft.Text(plat, size=10, weight="bold", color=estilo["color"]),
                                bgcolor=estilo["bg"], padding=5, border_radius=10
                            )
                        )
                    
                    # Añadir una etiqueta visual que indique si es Serie o Película
                    es_serie = tipo_contenido == "series"
                    chips.append(
                        ft.Container(
                            content=ft.Text("SERIE" if es_serie else "PELÍCULA", size=10, weight="bold", color=ft.Colors.WHITE),
                            bgcolor=ft.Colors.AMBER_700 if es_serie else ft.Colors.BLUE_700, padding=5, border_radius=10
                        )
                    )

                    url_poster = poster if poster != "N/A" else "https://via.placeholder.com/210x260?text=Sin+Imagen"
                    selector_estrellas = BarraEstrellas()

                    card = ft.Card(
                        elevation=5,
                        content=ft.Container(
                            width=230,
                            height=495,
                            padding=12,
                            border_radius=15,
                            bgcolor=ft.Colors.WHITE,
                            content=ft.Column(
                                [
                                    ft.GestureDetector(
                                        on_tap=lambda e, idx=imdb_id: ver_detalles_pelicula(idx),
                                        mouse_cursor=ft.MouseCursor.CLICK,
                                        content=ft.Container(
                                            height=220,
                                            width=210,
                                            border_radius=10,
                                            clip_behavior=ft.ClipBehavior.HARD_EDGE, 
                                            content=ft.Image(src=url_poster, fit="cover"),
                                        ),
                                    ),
                                    ft.Column(
                                        [
                                            ft.TextButton(
                                                titulo,
                                                style=ft.ButtonStyle(
                                                    color=ft.Colors.BLACK,
                                                    text_style=ft.TextStyle(weight="bold", size=15)
                                                ),
                                                on_click=lambda e, idx=imdb_id: ver_detalles_pelicula(idx),
                                            ),
                                            ft.Text(f"Año: {anio}", size=11, color=ft.Colors.GREY_700),
                                            ft.Row(chips, alignment=ft.MainAxisAlignment.CENTER, wrap=True, spacing=4),
                                            selector_estrellas,
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=2,
                                        expand=True, 
                                    ),
                                    ft.ElevatedButton(
                                        "Agregar",
                                        icon=ft.Icons.FAVORITE,
                                        bgcolor=ft.Colors.BLUE_900, 
                                        color=ft.Colors.WHITE,
                                        width=200,
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20), padding=8),
                                        on_click=lambda e, t=titulo, a=anio, p=plataformas[0], tc=tipo_contenido, sel=selector_estrellas: agregar_a_mysql(
                                            t, a, sel.rating_actual, p, tc
                                        )
                                    )
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=6
                            )
                        )
                    )
                    catalogo.controls.append(card)
                estado.value = ""
            else:
                estado.value = "No se encontraron resultados"
            page.update()
        except Exception as e:
            estado.value = f"Error: {e}"
            page.update()

    # --- 6. ELEMENTOS INTERACTIVOS ADICIONALES DE BÚSQUEDA ---
    buscador = ft.TextField(
        hint_text="Buscar película o serie...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=12,
        border_color=ft.Colors.BLUE_400,
        focused_border_color=ft.Colors.BLUE_900,
        on_submit=lambda e: buscar_peliculas(buscador.value)
    )

    def chip_click(e):
        buscar_peliculas(e.control.label.value)

    chips_categorias = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
        controls=[
            ft.Chip(label=ft.Text("Acción"), on_click=chip_click, bgcolor=ft.Colors.BLUE_50),
            ft.Chip(label=ft.Text("Comedia"), on_click=chip_click, bgcolor=ft.Colors.BLUE_50),
            ft.Chip(label=ft.Text("Terror"), on_click=chip_click, bgcolor=ft.Colors.BLUE_50),
            ft.Chip(label=ft.Text("Sci-Fi"), on_click=chip_click, bgcolor=ft.Colors.BLUE_50),
            ft.Chip(label=ft.Text("Breaking Bad"), on_click=chip_click, bgcolor=ft.Colors.BLUE_50),
        ]
    )

    # --- 7. MÉTODOS CRUD PARA FAVORITOS ---
    def borrar_de_mysql(id_favorito):
        exito, msg = fav_ctrl.borrar(id_favorito)
        if exito:
            mostrar_snackbar(msg)
            cargar_favoritos_mysql()

    def editar_en_mysql(id_favorito, plataforma_actual):
        dropdown = ft.Dropdown(
            width=200, value=plataforma_actual,
            border_color=ft.Colors.BLUE_400, focused_border_color=ft.Colors.BLUE_900,
            options=[
                ft.dropdown.Option("Netflix"), ft.dropdown.Option("Prime Video"),
                ft.dropdown.Option("Disney+"), ft.dropdown.Option("Max")
            ]
        )
        def guardar_cambios(e):
            exito, msg = fav_ctrl.actualizar(id_favorito, dropdown.value)
            dialogo.open = False
            if exito:
                mostrar_snackbar(msg)
                cargar_favoritos_mysql()
            page.update()

        dialogo = ft.AlertDialog(
            title=ft.Text("Editar Plataforma"),
            content=dropdown,
            actions=[ft.TextButton("Guardar", style=ft.ButtonStyle(color=ft.Colors.BLUE_900), on_click=guardar_cambios)]
        )
        page.dialog = dialogo
        dialogo.open = True
        page.update()

    def cargar_favoritos_mysql():
        catalogo_favoritos.controls.clear()
        try:
            datos = fav_ctrl.listar(id_usuario)
        except AttributeError:
            datos = []
            catalogo_favoritos.controls.append(
                ft.Text("Error en los métodos del controlador.", color=ft.Colors.RED_ACCENT, weight="bold")
            )
            page.update()
            return
        
        if not datos:
            catalogo_favoritos.controls.append(
                ft.Text("Aún no tienes elementos guardados.", color=ft.Colors.GREY_500, italic=True)
            )
        else:
            for f in datos:
                estrellas_guardadas = []
                try:
                    num_estrellas = int(float(f.get("rating", 5)))
                except:
                    num_estrellas = 5
                    
                for idx in range(5):
                    estrellas_guardadas.append(
                        ft.Icon(
                            ft.Icons.STAR if idx < num_estrellas else ft.Icons.STAR_BORDER,
                            color=ft.Colors.AMBER_600 if idx < num_estrellas else ft.Colors.GREY_400,
                            size=14
                        )
                    )

                card_fav = ft.Card(
                    elevation=4,
                    content=ft.Container(
                        width=200,
                        height=180,
                        padding=12,
                        border_radius=12,
                        bgcolor=ft.Colors.WHITE,
                        content=ft.Column(
                            [
                                ft.Icon(ft.Icons.THEATER_COMEDY, color=ft.Colors.BLUE_900, size=22),
                                ft.Text(f["titulo"], size=13, weight="bold", max_lines=1, overflow=ft.TextOverflow.ELLIPSIS, text_align=ft.TextAlign.CENTER),
                                ft.Text(f"Streaming: {f['plataforma']}", size=11, color=ft.Colors.GREY_700),
                                ft.Row(estrellas_guardadas, alignment=ft.MainAxisAlignment.CENTER, spacing=1),
                                ft.Row(
                                    [
                                        ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.BLUE_700, icon_size=16, on_click=lambda e, item=f: editar_en_mysql(item["id_favorito"], item["plataforma"])),
                                        ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_ACCENT, icon_size=16, on_click=lambda e, item=f: borrar_de_mysql(item["id_favorito"]))
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER, spacing=2
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        )
                    )
                )
                catalogo_favoritos.controls.append(card_fav)
        page.update()

    # --- 8. EJECUCIÓN INICIAL ---
    cargar_favoritos_mysql()

    # --- 9. RENDERIZADO DE LA VISTA ---
    return ft.View(
        route="/dashboard",
        appbar=ft.AppBar(
            title=ft.Text("Moviie"),
            bgcolor=ft.Colors.BLUE_900, 
            color=ft.Colors.WHITE,
            actions=[ft.IconButton(ft.Icons.LOGOUT, icon_color=ft.Colors.WHITE, on_click=lambda e: page.go("/"))]
        ),
        controls=[
            ft.Container(
                padding=20,
                expand=True,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                    scroll=ft.ScrollMode.AUTO, 
                    controls=[
                        ft.Text(f"Hola {usuario_actual['nombre']}", size=30, weight="bold", color=ft.Colors.BLUE_900),                        
                        ft.Container(width=500, content=buscador),                        
                        chips_categorias,
                        estado,
                        catalogo,                        
                        ft.Divider(height=30, thickness=2),                        
                        ft.Text("Mis Favoritas:", size=22, weight="bold", color=ft.Colors.BLUE_900),                        
                        ft.Container(content=catalogo_favoritos, margin=ft.Margin(left=0, top=0, right=0, bottom=40))
                    ]
                )
            )
        ]
    )