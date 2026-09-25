from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd


# ==========================================================
# CONFIGURACIÓN
# ==========================================================

START_URL = "https://science.nasa.gov/exoplanets/exoplanet-catalog/"

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

    # Si el hyperlink viene como:
    # [https://...](https://...)

    if hyperlink.startswith("[") and "](" in hyperlink:

        hyperlink = hyperlink.split("](")[1]

        if hyperlink.endswith(")"):

            hyperlink = hyperlink[:-1]

    return hyperlink


# ==========================================================
# FUNCIÓN PARA EXTRAER DATOS DE CADA PLANETA
# ==========================================================

def scrape_more_data(hyperlink):

    print("\n")
    print("==========================================================")
    print("VISITANDO:")
    print(hyperlink)
    print("==========================================================")

    try:

        # --------------------------------------------------
        # LIMPIAR HYPERLINK
        # --------------------------------------------------

        hyperlink = limpiar_hyperlink(hyperlink)

        # --------------------------------------------------
        # ABRIR LA PÁGINA DEL PLANETA
        # --------------------------------------------------

        browser.get(hyperlink)

        time.sleep(5)

        # --------------------------------------------------
        # OBTENER NOMBRE DEL PLANETA
        # --------------------------------------------------

        try:

            titulo = browser.find_element(
                By.TAG_NAME,
                "h1"
            )

            print(
                "Planeta:",
                titulo.text
            )

        except:

            print(
                "No se encontró el nombre del planeta"
            )


        # --------------------------------------------------
        # VARIABLES
        # --------------------------------------------------

        planet_type = ""
        discovery_date = ""
        mass = ""
        planet_radius = ""
        orbital_radius = ""
        orbital_period = ""
        eccentricity = ""
        detection_method = ""


        # ==================================================
        # FUNCIÓN INTERNA PARA OBTENER UN VALOR
        # ==================================================

        def obtener_valor(etiqueta):

            try:

                # Buscar la etiqueta

                elemento = browser.find_element(
                    By.XPATH,
                    f"//*[normalize-space(text())='{etiqueta}']"
                )


                # Buscar el elemento que contiene
                # el valor inmediatamente después

                siguiente = elemento.find_element(
                    By.XPATH,
                    "following::*[normalize-space()][1]"
                )


                return siguiente.text.strip()


            except:

                return ""


        # ==================================================
        # EXTRAER CADA CAMPO
        # ==================================================

        planet_radius = obtener_valor(
            "Planet Radius:"
        )


        planet_type = obtener_valor(
            "Planet Type:"
        )


        detection_method = obtener_valor(
            "Discovery Method:"
        )


        mass = obtener_valor(
            "Planet Mass:"
        )


        discovery_date = obtener_valor(
            "Discovery Date:"
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


        # ==================================================
        # MOSTRAR DATOS
        # ==================================================

        print("\nDATOS ENCONTRADOS")

        print(
            "Planet Type:",
            planet_type
        )

        print(
            "Discovery Date:",
            discovery_date
        )

        print(
            "Planet Mass:",
            mass
        )

        print(
            "Planet Radius:",
            planet_radius
        )

        print(
            "Orbital Radius:",
            orbital_radius
        )

        print(
            "Orbital Period:",
            orbital_period
        )

        print(
            "Eccentricity:",
            eccentricity
        )

        print(
            "Detection Method:",
            detection_method
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


    except Exception as e:

        print(
            "\nERROR AL EXTRAER DATOS:"
        )

        print(e)


# ==========================================================
# LEER CSV DEL PRIMER SCRAPER
# ==========================================================

planet_df_1 = pd.read_csv(
    "scraped_data_prueba.csv"
)


# ==========================================================
# MOSTRAR COLUMNAS
# ==========================================================

print("\n")
print("==========================================================")
print("COLUMNAS DEL CSV")
print("==========================================================")


print(
    planet_df_1.columns.tolist()
)


# ==========================================================
# RECORRER LOS HYPERLINKS
# ==========================================================

for index, row in planet_df_1.iterrows():

    hyperlink = row["hyperlink"]


    # ------------------------------------------------------
    # COMPROBAR QUE EXISTE HYPERLINK
    # ------------------------------------------------------

    if pd.isna(hyperlink):

        print(
            "No existe hyperlink para el registro:",
            index
        )

        continue


    # ------------------------------------------------------
    # EXTRAER DATOS
    # ------------------------------------------------------

    scrape_more_data(
        hyperlink
    )


    print(
        f"\nLa extracción del hipervínculo "
        f"{index + 1} se ha completado."
    )


# ==========================================================
# MOSTRAR DATOS EXTRAÍDOS
# ==========================================================

print("\n")
print("==========================================================")
print("NEW PLANETS DATA")
print("==========================================================")


print(
    new_planets_data
)


# ==========================================================
# CREAR DATAFRAME
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


new_planet_df_1 = pd.DataFrame(

    new_planets_data,

    columns=headers

)


# ==========================================================
# MOSTRAR DATAFRAME
# ==========================================================

print("\n")
print("==========================================================")
print("DATAFRAME FINAL")
print("==========================================================")


print(
    new_planet_df_1.to_string(
        index=True
    )
)


# ==========================================================
# GUARDAR CSV
# ==========================================================

new_planet_df_1.to_csv(

    "new_scraped_data_prueba.csv",

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

print("\n")
print("==========================================================")
print("SCRAPING TERMINADO")
print("==========================================================")


print(
    "Total de planetas procesados:",
    len(new_planet_df_1)
)


print(
    "Archivo creado: new_scraped_data_prueba.csv"
)


print("==========================================================")

