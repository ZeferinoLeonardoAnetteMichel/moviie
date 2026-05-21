import flet as ft
import requests

def DashboardView(page: ft.Page):
    OMDB_API_KEY = "d55033dc" 
    URL_BASE = "https://www.omdbapi.com/"
    peliculas_actuales = []
    plataforma_seleccionada = "Todas"
    PLATAFORMAS_MAP = {
        "inception": ["Netflix", "Max"],
        "the dark knight": ["Max"],
        "interstellar": ["Prime Video", "Max"],
        "spirited away": ["Netflix"],
        "pulp fiction": ["Netflix", "Prime Video"],
        "parasite": ["Netflix"],
        "avengers": ["Disney+"],
        "batman": ["Max", "Prime Video"],
        "star wars": ["Disney+"],
    }
    STREAMING_BADGES = {
        "Netflix": {"color": ft.Colors.RED_700, "bg": ft.Colors.RED_50},
        "Max": {"color": ft.Colors.BLUE_800, "bg": ft.Colors.BLUE_50},
        "Prime Video": {"color": ft.Colors.CYAN_700, "bg": ft.Colors.CYAN_50},
        "Disney+": {"color": ft.Colors.INDIGO_900, "bg": ft.Colors.INDIGO_50},
        "Predeterminado": {"color": ft.Colors.PURPLE_700, "bg": ft.Colors.PURPLE_50}
    }

    def obtener_plataformas(titulo):
        """Busca qué plataformas tienen la película en nuestro mapa local."""
        titulo_min = titulo.lower()
        for clave, plataformas in PLATAFORMAS_MAP.items():
            if clave in titulo_min:
                return plataformas
        return ["Prime Video"]

    def crear_tarjeta_pelicula(pelicula_data):
        titulo = pelicula_data.get("Title", "Sin título")
        año = pelicula_data.get("Year", "N/A")
        rating = pelicula_data.get("imdbRating", "N/A")
        
        imagen = pelicula_data.get("Poster")
        if imagen == "N/A" or not imagen:
            imagen = "https://images.unsplash.com/photo-1594909122845-11baa439b7bf?w=500"

        plataformas = obtener_plataformas(titulo)

        plataformas_chips = []
        for plat in plataformas:
            estilo = STREAMING_BADGES.get(plat, STREAMING_BADGES["Predeterminado"])
            plataformas_chips.append(
                ft.Container(
                    content=ft.Text(plat, size=9, color=estilo["color"], weight="bold"),
                    bgcolor=estilo["bg"],
                    padding=4,
                    border_radius=4,
                )
            )

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Container(
                            image=ft.DecorationImage(src=imagen, fit="cover"),
                            border_radius=ft.BorderRadius(top_left=10, top_right=10, bottom_left=0, bottom_right=0),
                            height=190,
                        ),
                        ft.Container(
                            padding=8,
                            content=ft.Column(
                                [
                                    ft.Text(titulo, size=14, weight="bold", max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                                    ft.Text(f"Año: {año}", size=11, color=ft.Colors.GREY_600),
                                    ft.Row(plataformas_chips, spacing=4, wrap=True),
                                    ft.Divider(height=8, color=ft.Colors.GREY_200),
                                    ft.Row(
                                        [
                                            ft.Row(
                                                [
                                                    ft.Icon(ft.Icons.STAR, color=ft.Colors.AMBER, size=14),
                                                    ft.Text(rating, size=12, weight="bold"),
                                                ],
                                                spacing=2,
                                            ),
                                            ft.IconButton(
                                                icon=ft.Icons.PLAY_ARROW_ROUNDED,
                                                icon_color=ft.Colors.WHITE,
                                                bgcolor=ft.Colors.PURPLE_400,
                                                icon_size=16,
                                                padding=4,
                                                on_click=lambda _: print(f"Reproduciendo: {titulo}")
                                            )
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    )
                                ],
                                spacing=4,
                            )
                        )
                    ],
                    spacing=0,
                ),
                width=180,
            ),
            elevation=3,
        )

    catalogo_grid = ft.GridView(
        expand=True,
        runs_count=2,
        max_extent=200,
        child_aspect_ratio=0.55, 
        spacing=10,
        run_spacing=10,
    )

    status_text = ft.Text("", size=14, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER)

    def renderizar_catalogo_filtrado():
        """Filtra la lista en memoria y redibuja las tarjetas."""
        catalogo_grid.controls.clear()
        
        peliculas_filtradas = []
        for p in peliculas_actuales:
            if plataforma_seleccionada == "Todas":
                peliculas_filtradas.append(p)
            else:
                plats_peli = obtener_plataformas(p.get("Title", ""))
                if plataforma_seleccionada in plats_peli:
                    peliculas_filtradas.append(p)

        if not peliculas_filtradas:
            status_text.value = f"No hay resultados en {plataforma_seleccionada}."
        else:
            status_text.value = ""
            for p_detalle in peliculas_filtradas:
                catalogo_grid.controls.append(crear_tarjeta_pelicula(p_detalle))
        
        page.update()

    def realizar_busqueda_api(busqueda_termino):
        """Descarga las películas de OMDb."""
        nonlocal peliculas_actuales
        if not busqueda_termino.strip():
            return

        catalogo_grid.controls.clear()
        peliculas_actuales = []
        status_text.value = "Buscando películas..."
        page.update()

        try:
            params_busqueda = {
                "apikey": OMDB_API_KEY,
                "s": busqueda_termino.strip(),
                "type": "movie"
            }
            
            response = requests.get(URL_BASE, params=params_busqueda, timeout=5).json()
            
            if response.get("Response") == "True":
                status_text.value = "Cargando detalles..."
                page.update()

                for p_resumen in response.get("Search", [])[:6]:
                    id_imdb = p_resumen["imdbID"]
                    params_detalle = {"apikey": OMDB_API_KEY, "i": id_imdb}
                    p_detalle = requests.get(URL_BASE, params=params_detalle, timeout=5).json()
                    peliculas_actuales.append(p_detalle)
                
                renderizar_catalogo_filtrado()
            else:
                status_text.value = f"Error de la API: {response.get('Error', 'Sin resultados')}"
                page.update()
                
        except Exception as ex:
            status_text.value = f"Error de conexión: {ex}"
            page.update()

    def al_cambiar_buscador(e):
        if len(buscador.value.strip()) >= 3:
            realizar_busqueda_api(buscador.value)

    def al_seleccionar_filtro(e):
        """Maneja el clic de los filtros."""
        nonlocal plataforma_seleccionada
        plataforma_seleccionada = e.control.data
        for chip in barra_filtros.controls:
            if chip.data == plataforma_seleccionada:
                chip.bgcolor = ft.Colors.PURPLE_400
                chip.content.color = ft.Colors.WHITE
            else:
                plat_nombre = chip.data
                estilo_base = STREAMING_BADGES.get(plat_nombre, {"bg": ft.Colors.GREY_100, "color": ft.Colors.GREY_800})
                chip.bgcolor = estilo_base["bg"] if plat_nombre != "Todas" else ft.Colors.PURPLE_50
                chip.content.color = estilo_base["color"] if plat_nombre != "Todas" else ft.Colors.PURPLE_700
        
        renderizar_catalogo_filtrado()

    buscador = ft.TextField(
        hint_text="Escribe una película (ej: Batman, Inception)...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=10,
        border_color="purple",
        expand=True,
        on_submit=lambda e: realizar_busqueda_api(buscador.value),
        on_change=al_cambiar_buscador
    )

    opciones_filtros = ["Todas", "Netflix", "Max", "Prime Video", "Disney+"]
    botones_filtros = []

    for opcion in opciones_filtros:
        es_todas = opcion == "Todas"
        bg_color = ft.Colors.PURPLE_400 if es_todas else (STREAMING_BADGES.get(opcion, {}).get("bg", ft.Colors.PURPLE_50))
        text_color = ft.Colors.WHITE if es_todas else (STREAMING_BADGES.get(opcion, {}).get("color", ft.Colors.PURPLE_700))
        
        botones_filtros.append(
            ft.Container(
                content=ft.Text(opcion, size=12, color=text_color, weight="bold"),
                bgcolor=bg_color,
                padding=ft.Padding(12, 6, 12, 6), 
                border_radius=20,                
                alignment=ft.Alignment(0, 0), 
                data=opcion,
                on_click=al_seleccionar_filtro,
                animate=200
            )
        )

    barra_filtros = ft.Row(
        controls=botones_filtros,
        scroll=ft.ScrollMode.AUTO,
        spacing=8
    )

    realizar_busqueda_api("Batman")
    return ft.View(
        route="/dashboard",
        appbar=ft.AppBar(
            title=ft.Text("Moviie - API"),
            bgcolor=ft.Colors.PURPLE_200,
            color=ft.Colors.WHITE,
            actions=[
                ft.IconButton(
                    icon=ft.Icons.LOGOUT, 
                    tooltip="Cerrar Sesión", 
                    on_click=lambda _: page.go("/")
                )
            ]
        ),
        controls=[
            ft.Container(
                padding=15,
                expand=True,
                content=ft.Column(
                    [
                        ft.Text("¡Hola de nuevo!", size=22, weight="bold", color="purple"),
                        ft.Row([buscador]),
                        ft.Text("Filtrar por plataforma:", size=12, color=ft.Colors.GREY_600, weight="bold"),
                        barra_filtros, 
                        status_text,
                        ft.Text("Resultados de la API", size=16, weight="bold"),
                        catalogo_grid
                    ],
                    spacing=10,
                    expand=True
                )
            )
        ]
    )