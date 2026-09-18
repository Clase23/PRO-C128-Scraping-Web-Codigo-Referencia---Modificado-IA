from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd


# ==========================================================
# CONFIGURACIÓN
# ==========================================================

START_URL = "https://science.nasa.gov/exoplanets/exoplanet-catalog/"

browser = webdriver.Chrome()

planets_data = []


# ==========================================================
# FUNCIÓN PARA EXTRAER PLANETAS
# ==========================================================

def extraer_planetas():

    soup = BeautifulSoup(
        browser.page_source,
        "html.parser"
    )

    parsec_elements = soup.find_all(
        "span",
        class_="font-weight-bold"
    )

    print(
        "Elementos encontrados:",
        len(parsec_elements)
    )

    planetas_nuevos = 0

    for elemento in parsec_elements:

        texto = elemento.get_text(
            " ",
            strip=True
        )

        # --------------------------------------------------
        # BUSCAR "Parsecs from Earth:"
        # --------------------------------------------------

        if texto != "Parsecs from Earth:":
            continue

        # --------------------------------------------------
        # BUSCAR EL CONTENEDOR DEL PLANETA
        # --------------------------------------------------

        container = elemento

        for _ in range(10):

            if container.parent is None:
                break

            container = container.parent

            container_text = container.get_text(
                " ",
                strip=True
            )

            if (
                "Parsecs from Earth:" in container_text
                and "Planet Mass:" in container_text
                and "Stellar Magnitude:" in container_text
                and "Discovery Date:" in container_text
            ):
                break

        # --------------------------------------------------
        # MOSTRAR DATOS EN CONSOLA
        # --------------------------------------------------

        datos = container.get_text(
            "\n",
            strip=True
        )

        print("\n--------------------------------")
        print(datos)
        print("--------------------------------")

        # --------------------------------------------------
        # OBTENER NOMBRE Y HYPERLINK
        # --------------------------------------------------

        planet_link = container.find("a")

        if planet_link is None:
            continue

        # Nombre del planeta
        name = planet_link.get_text(
            strip=True
        )

        # Obtener hyperlink
        hyperlink = planet_link.get(
            "href",
            ""
        )

        # --------------------------------------------------
        # CONVERTIR LINK RELATIVO EN LINK COMPLETO
        # --------------------------------------------------

        if hyperlink.startswith("/"):
            hyperlink = "https://science.nasa.gov" + hyperlink

        # --------------------------------------------------
        # MOSTRAR HYPERLINK
        # --------------------------------------------------

        print(
            "Hyperlink:",
            hyperlink
        )

        # --------------------------------------------------
        # OBTENER TEXTOS
        # --------------------------------------------------

        textos = list(
            container.stripped_strings
        )

        parsecs = ""
        planet_mass = ""
        stellar_magnitude = ""
        discovery_date = ""

        # --------------------------------------------------
        # BUSCAR LOS CAMPOS
        # --------------------------------------------------

        for i, texto in enumerate(textos):

            if texto == "Parsecs from Earth:":

                if i + 1 < len(textos):
                    parsecs = textos[i + 1]

            elif texto == "Planet Mass:":

                if i + 1 < len(textos):
                    planet_mass = textos[i + 1]

            elif texto == "Stellar Magnitude:":

                if i + 1 < len(textos):
                    stellar_magnitude = textos[i + 1]

            elif texto == "Discovery Date:":

                if i + 1 < len(textos):
                    discovery_date = textos[i + 1]

        # --------------------------------------------------
        # CREAR REGISTRO
        # --------------------------------------------------

        temp_list = [
            name,
            parsecs,
            planet_mass,
            stellar_magnitude,
            discovery_date,
            hyperlink
        ]

        # --------------------------------------------------
        # EVITAR DUPLICADOS
        # --------------------------------------------------

        if temp_list not in planets_data:

            planets_data.append(
                temp_list
            )

            planetas_nuevos += 1

            print(
                "Planeta encontrado:",
                name
            )

    return planetas_nuevos


# ==========================================================
# FUNCIÓN PARA HACER CLIC EN "NEXT"
# ==========================================================

def siguiente_pagina():

    try:

        # Buscar todos los elementos que tengan el texto Next
        elementos_next = browser.find_elements(
            By.XPATH,
            "//*[normalize-space(text())='Next']"
        )

        print(
            "Elementos 'Next' encontrados:",
            len(elementos_next)
        )

        if len(elementos_next) == 0:

            print(
                "No se encontró el botón Next."
            )

            return False

        # --------------------------------------------------
        # BUSCAR EL ELEMENTO VISIBLE
        # --------------------------------------------------

        boton_next = None

        for elemento in elementos_next:

            try:

                if elemento.is_displayed():

                    boton_next = elemento

                    break

            except:
                pass

        if boton_next is None:

            print(
                "El botón Next no está visible."
            )

            return False

        # --------------------------------------------------
        # HACER SCROLL HASTA EL BOTÓN
        # --------------------------------------------------

        browser.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            boton_next
        )

        time.sleep(1)

        # --------------------------------------------------
        # HACER CLIC
        # --------------------------------------------------

        browser.execute_script(
            "arguments[0].click();",
            boton_next
        )

        print(
            "Clic realizado en Next."
        )

        # --------------------------------------------------
        # ESPERAR A QUE CAMBIE EL CONTENIDO
        # --------------------------------------------------

        time.sleep(5)

        return True

    except Exception as e:

        print(
            "Error al hacer clic en Next:"
        )

        print(e)

        return False


# ==========================================================
# SCRAPING
# ==========================================================

def scrape():

    print("\n")
    print("==========================================================")
    print("INICIANDO SCRAPING NASA EXOPLANET CATALOG")
    print("==========================================================")

    # ------------------------------------------------------
    # CARGAR PÁGINA INICIAL
    # ------------------------------------------------------

    browser.get(START_URL)

    print("\nCargando NASA...")

    time.sleep(10)

    pagina = 1

    # ------------------------------------------------------
    # CICLO DE PÁGINAS
    # ------------------------------------------------------

    while True:

        print("\n")
        print("==========================================================")
        print("PÁGINA:", pagina)
        print("==========================================================")

        # --------------------------------------------------
        # EXTRAER PLANETAS DE LA PÁGINA ACTUAL
        # --------------------------------------------------

        planetas_nuevos = extraer_planetas()

        print("\n------------------------------------------")

        print(
            "Planetas nuevos encontrados en página",
            pagina,
            ":",
            planetas_nuevos
        )

        print(
            "Total acumulado:",
            len(planets_data)
        )

        print("------------------------------------------")

        # --------------------------------------------------
        # SI NO HAY PLANETAS NUEVOS
        # --------------------------------------------------

        if planetas_nuevos == 0:

            print(
                "\nNo se encontraron planetas nuevos."
            )

            print(
                "Se detiene el scraping."
            )

            break

        # --------------------------------------------------
        # INTENTAR IR A LA SIGUIENTE PÁGINA
        # --------------------------------------------------

        print("\nBuscando botón Next...")

        resultado = siguiente_pagina()

        if resultado is False:

            print(
                "\nNo fue posible pasar a la siguiente página."
            )

            break

        pagina += 1

        # --------------------------------------------------
        # PROTECCIÓN
        # --------------------------------------------------

        if pagina > 424:

            print(
                "\nSe alcanzó el máximo de páginas indicado por NASA."
            )

            break


# ==========================================================
# EJECUTAR SCRAPING
# ==========================================================

scrape()


# ==========================================================
# CERRAR NAVEGADOR
# ==========================================================

browser.quit()


# ==========================================================
# CREAR DATAFRAME
# ==========================================================

headers = [
    "name",
    "parsecs_from_earth",
    "planet_mass",
    "stellar_magnitude",
    "discovery_date",
    "hyperlink"
]

planet_df_1 = pd.DataFrame(
    planets_data,
    columns=headers
)


# ==========================================================
# MOSTRAR DATAFRAME
# ==========================================================

print("\n\n")
print("==========================================================")
print("DATAFRAME")
print("==========================================================")

print(
    planet_df_1.to_string(
        index=True
    )
)


# ==========================================================
# GUARDAR CSV
# ==========================================================

planet_df_1.to_csv(
    "scraped_data.csv",
    index=True,
    index_label="id"
)


# ==========================================================
# RESULTADO FINAL
# ==========================================================

print("\n")
print("==========================================================")
print("SCRAPING TERMINADO")
print("==========================================================")

print(
    "Total de exoplanetas:",
    len(planet_df_1)
)

print(
    "Archivo creado: scraped_data.csv"
)

print("==========================================================")

