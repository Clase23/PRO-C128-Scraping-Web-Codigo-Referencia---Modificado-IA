# Aqui 120926 Revisar de nuevo este archivo de Aza
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd


# ==========================================================
# CONFIGURACIÓN
# ==========================================================

START_URL = "https://science.nasa.gov/exoplanets/exoplanet-catalog/"

# Archivo generado por el PRIMER SCRAPER
INPUT_CSV = "scraped_data.csv"

# Archivo que generará ESTE SEGUNDO SCRAPER
OUTPUT_CSV = "new_scraped_data.csv"


# ==========================================================
# INICIAR NAVEGADOR
# ==========================================================

browser = webdriver.Chrome()


# ==========================================================
# LISTA PARA GUARDAR LOS DATOS
# ==========================================================

new_planets_data = []


# ==========================================================
# FUNCIÓN PARA LIMPIAR EL HYPERLINK
# ==========================================================

def limpiar_hyperlink(hyperlink):

    hyperlink = str(hyperlink).strip()

    # En caso de que venga así:
    #
    # [https://science.nasa.gov/exoplanet-catalog/toi-6158-b/]
    # (https://science.nasa.gov/exoplanet-catalog/toi-6158-b/)

    if hyperlink.startswith("[") and "](" in hyperlink:

        hyperlink = hyperlink.split("](")[1]

        if hyperlink.endswith(")"):

            hyperlink = hyperlink[:-1]

    return hyperlink


# ==========================================================
# FUNCIÓN PARA EXTRAER UN VALOR
# ==========================================================

def obtener_valor(etiqueta):

    try:

        # Buscar la etiqueta.
        #
        # Ejemplo:
        # Planet Radius:
        # Planet Mass:
        # Orbital Period:

        elemento = browser.find_element(
            By.XPATH,
            f"//*[normalize-space(text())='{etiqueta}']"
        )


        # Buscar el primer elemento con texto
        # que aparece después de la etiqueta.

        siguiente = elemento.find_element(
            By.XPATH,
            "following::*[normalize-space()][1]"
        )


        valor = siguiente.text.strip()


        return valor


    except Exception:

        return ""


# ==========================================================
# FUNCIÓN PARA EXTRAER LOS DATOS DE UN PLANETA
# ==========================================================

def scrape_more_data(hyperlink, numero, total):

    #print()
    #print("==========================================================")
    #print(f"PLANETA {numero} DE {total}")
    #print("==========================================================")

    #print("VISITANDO:")
    #print(hyperlink)


    try:

        # --------------------------------------------------
        # LIMPIAR HYPERLINK
        # --------------------------------------------------

        hyperlink = limpiar_hyperlink(hyperlink)


        # --------------------------------------------------
        # ABRIR PÁGINA
        # --------------------------------------------------

        browser.get(hyperlink)


        # --------------------------------------------------
        # ESPERAR A QUE APAREZCA EL TÍTULO
        # --------------------------------------------------

        try:

            WebDriverWait(
                browser,
                15
            ).until(

                EC.presence_of_element_located(
                    (By.TAG_NAME, "h1")
                )

            )

        except:

            print(
                "No apareció el título dentro del tiempo esperado."
            )


        # --------------------------------------------------
        # PEQUEÑA ESPERA
        # --------------------------------------------------

        time.sleep(2)


        # --------------------------------------------------
        # OBTENER NOMBRE
        # --------------------------------------------------

        try:

            titulo = browser.find_element(
                By.TAG_NAME,
                "h1"
            )

            nombre_planeta = titulo.text.strip()

        except:

            nombre_planeta = "Desconocido"


        #print()
        #print("Planeta:", nombre_planeta)


        # ==================================================
        # EXTRAER LOS 8 CAMPOS
        # ==================================================

        planet_type = obtener_valor(
            "Planet Type:"
        )


        discovery_date = obtener_valor(
            "Discovery Date:"
        )


        mass = obtener_valor(
            "Planet Mass:"
        )


        planet_radius = obtener_valor(
            "Planet Radius:"
        )


        orbital_radius = obtener_valor(
            "Orbital Radius:"
        )


        orbital_period = obtener_valor(
            "Orbital Period:"
        )


        eccentricity = obtener_valor(
            "Eccentricity:"
        )


        detection_method = obtener_valor(
            "Discovery Method:"
        )


        

        # ==================================================
        # CREAR REGISTRO
        # ==================================================

        temp_list = [

            planet_type,
            discovery_date,
            mass,
            planet_radius,
            orbital_radius,
            orbital_period,
            eccentricity,
            detection_method

        ]


        # ==================================================
        # GUARDAR REGISTRO
        # ==================================================

        new_planets_data.append(
            temp_list
        )


        #print()
        print(
            f"La extracción del planeta "
            f"{numero} se ha completado correctamente."
        )


        return True


    except Exception as e:

        #print()
        #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        #print("ERROR AL EXTRAER EL PLANETA")
        #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        print(
            "Planeta:",
            nombre_planeta if "nombre_planeta" in locals()
            else "Desconocido"
        )

        print(
            "Hyperlink:",
            hyperlink
        )

        print(
            "Error:",
            e
        )


        # --------------------------------------------------
        # GUARDAR REGISTRO VACÍO
        # --------------------------------------------------

        temp_list = [

            "",
            "",
            "",
            "",
            "",
            "",
            "",
            ""

        ]


        new_planets_data.append(
            temp_list
        )


        print(
            "El programa continuará con el siguiente planeta."
        )


        return False


# ==========================================================
# LEER CSV DEL PRIMER SCRAPER
# ==========================================================

#print()
#print("==========================================================")
#print("LEYENDO ARCHIVO DEL PRIMER SCRAPER")
#print("==========================================================")


planet_df_1 = pd.read_csv(
    INPUT_CSV
)


# ==========================================================
# MOSTRAR COLUMNAS
# ==========================================================

#print()
#print("COLUMNAS ENCONTRADAS:")

print(
    planet_df_1.columns.tolist()
)


# ==========================================================
# VERIFICAR QUE EXISTA LA COLUMNA HYPERLINK
# ==========================================================

if "hyperlink" not in planet_df_1.columns:

    #print()
    #print("ERROR:")
    print(
        "El archivo CSV no contiene la columna 'hyperlink'."
    )

    browser.quit()

    raise SystemExit


# ==========================================================
# TOTAL DE REGISTROS
# ==========================================================

total_planetas = len(
    planet_df_1
)


#print()
#print("==========================================================")
#print("INICIO DEL SEGUNDO SCRAPING")
#print("==========================================================")

print(
    "Total de registros:",
    total_planetas
)


# ==========================================================
# RECORRER TODOS LOS REGISTROS
# ==========================================================

for numero, (index, row) in enumerate(
    planet_df_1.iterrows(),
    start=1
):


    # ------------------------------------------------------
    # OBTENER HYPERLINK
    # ------------------------------------------------------

    hyperlink = row["hyperlink"]


    # ------------------------------------------------------
    # COMPROBAR SI EXISTE
    # ------------------------------------------------------

    if pd.isna(hyperlink):

        #print()
        print(
            f"Registro {numero}: "
            "no tiene hyperlink."
        )


        # Guardar registro vacío

        new_planets_data.append([

            "",
            "",
            "",
            "",
            "",
            "",
            "",
            ""

        ])


        continue


    # ------------------------------------------------------
    # EXTRAER DATOS
    # ------------------------------------------------------

    scrape_more_data(

        hyperlink,
        numero,
        total_planetas

    )


# ==========================================================
# MOSTRAR TODOS LOS DATOS EXTRAÍDOS
# ==========================================================

#print()
#print("==========================================================")
#print("NEW PLANETS DATA")
#print("==========================================================")


print(
    new_planets_data
)


# ==========================================================
# ENCABEZADOS DEL SEGUNDO CSV
# ==========================================================

headers = [

    "planet_type",
    "discovery_date",
    "mass",
    "planet_radius",
    "orbital_radius",
    "orbital_period",
    "eccentricity",
    "detection_method"

]


# ==========================================================
# CREAR DATAFRAME
# ==========================================================

new_planet_df_1 = pd.DataFrame(

    new_planets_data,

    columns=headers

)


# ==========================================================
# MOSTRAR DATAFRAME
# ==========================================================

#print()
#print("==========================================================")
#print("DATAFRAME FINAL")
#print("==========================================================")


print(
    new_planet_df_1.to_string(
        index=True
    )
)


# ==========================================================
# GUARDAR CSV
# ==========================================================

new_planet_df_1.to_csv(

    OUTPUT_CSV,

    index=True,

    index_label="id"

)


# ==========================================================
# CERRAR NAVEGADOR
# ==========================================================

browser.quit()


# ==========================================================
# RESULTADO FINAL
# ==========================================================

#print()
#print("==========================================================")
#print("SCRAPING TERMINADO")
#print("==========================================================")


print(
    "Total de registros procesados:",
    len(new_planet_df_1)
)


print(
    "Archivo creado:",
    OUTPUT_CSV
)


#print("==========================================================")

