import pandas as pd
import numpy as np
from fractions import Fraction

def leer_matriz_csv(ruta):
    df = pd.read_csv(ruta, sep=";", index_col=0, encoding="utf-8-sig")
    # Convertir fracciones tipo '1/3' en decimales
    def convertir_valor(x):
        try:
            return float(Fraction(str(x).strip()))
        except:
            return float(x)
    df = df.map(convertir_valor)
    return df.values

def calcular_pesos(matriz):
    valores, vectores = np.linalg.eig(matriz)
    indice_max = np.argmax(valores)
    vector_pesos = np.real(vectores[:, indice_max])
    return vector_pesos / np.sum(vector_pesos)

def razon_consistencia(matriz):
    n = matriz.shape[0]
    valores, _ = np.linalg.eig(matriz)
    lambda_max = np.max(np.real(valores))
    CI = (lambda_max - n) / (n - 1)
    RI = {1:0, 2:0, 3:0.58, 4:0.9, 5:1.12, 6:1.24, 7:1.32, 8:1.41, 9:1.45, 10:1.49}
    return CI / RI[n]

def agregar_matrices(matrices):
    log_matrices = [np.log(m) for m in matrices]
    promedio_log = sum(log_matrices) / len(log_matrices)
    matriz_agregada = np.exp(promedio_log)
    return matriz_agregada

def sintetizar_global(pesos_criterios, pesos_social, pesos_org, pesos_terr, pesos_alternativas):
    global_alternativas = np.zeros(7)

    # --- Criterio Social (6 subcriterios) ---
    for i in range(6):
        global_alternativas += pesos_criterios[0] * pesos_social[i] * pesos_alternativas[i]

    # --- Criterio Organizacional (7 subcriterios) ---
    for i in range(7):
        global_alternativas += pesos_criterios[1] * pesos_org[i] * pesos_alternativas[6 + i]

    # --- Criterio Territorial (6 subcriterios) ---
    for i in range(6):
        global_alternativas += pesos_criterios[2] * pesos_terr[i] * pesos_alternativas[13 + i]

    return global_alternativas / np.sum(global_alternativas)

def main():
    # ==============================
    # 1. MATRICES DE CRITERIOS (3x3 por especialista)
    # ==============================
    matrices_criterios = [leer_matriz_csv(f"criterios3x3_especialista{i}.csv") for i in range(1, 7)]
    matriz_criterios_agregada = agregar_matrices(matrices_criterios)
    pesos_criterios = calcular_pesos(matriz_criterios_agregada)
    cr_criterios = razon_consistencia(matriz_criterios_agregada)
    print("Pesos criterios agregados:", pesos_criterios)
    print("Consistencia criterios agregada:", cr_criterios)

    # ==============================
    # 2. MATRICES SOCIALES (6x6 por especialista)
    # ==============================
    matrices_social = [leer_matriz_csv(f"criterios6x6s_especialista{i}.csv") for i in range(1, 7)]
    matriz_social_agregada = agregar_matrices(matrices_social)
    pesos_social = calcular_pesos(matriz_social_agregada)
    cr_social = razon_consistencia(matriz_social_agregada)
    print("Pesos subcriterios - Social:", pesos_social)
    print("Consistencia Social:", cr_social)

    # ==============================
    # 3. MATRICES ORGANIZACIONALES (7x7 por especialista, solo 6 especialistas)
    # ==============================
    matrices_org = [leer_matriz_csv(f"criterios7x7o_especialista{i}.csv") for i in range(1, 7)]
    matriz_org_agregada = agregar_matrices(matrices_org)
    pesos_org = calcular_pesos(matriz_org_agregada)
    cr_org = razon_consistencia(matriz_org_agregada)
    print("Pesos subcriterios - Organizacional:", pesos_org)
    print("Consistencia Organizacional:", cr_org)

    # ==============================
    # 4. MATRICES TERRITORIALES (6x6 por especialista)
    # ==============================
    matrices_terr = [leer_matriz_csv(f"criterios6x6t_especialista{i}.csv") for i in range(1, 7)]
    matriz_terr_agregada = agregar_matrices(matrices_terr)
    pesos_terr = calcular_pesos(matriz_terr_agregada)
    cr_terr = razon_consistencia(matriz_terr_agregada)
    print("Pesos subcriterios - Territorial:", pesos_terr)
    print("Consistencia Territorial:", cr_terr)

    # ==============================
    # 5. MATRICES DE ALTERNATIVAS (19 archivos de revisión documental)
    # ==============================
    alternativas_files = [
        # Sociales
        "alternativas7x7_empleo.csv",
        "alternativas7x7_joven.csv",
        "alternativas7x7_mujer.csv",
        "alternativas7x7_impacto.csv",
        "alternativas7x7_emprendedores.csv",
        "alternativas7x7_capacidad.csv",
        # Organizacionales
        "alternativas7x7_produc.csv",
        "alternativas7x7_costos.csv",
        "alternativas7x7_mercado.csv",
        "alternativas7x7_aliados.csv",
        "alternativas7x7_tecnologia.csv",
        "alternativas7x7_calidad.csv",
        "alternativas7x7_certificaciones.csv",
        # Territoriales
        "alternativas7x7_acceso.csv",
        "alternativas7x7_servicios.csv",
        "alternativas7x7_electricidad.csv",
        "alternativas7x7_comunica.csv",
        "alternativas7x7_medio.csv",
        "alternativas7x7_instrumento.csv"
    ]

    pesos_alternativas = []
    for i, archivo in enumerate(alternativas_files, start=1):
        matriz = leer_matriz_csv(archivo)
        pesos_alt = calcular_pesos(matriz)
        cr_alt = razon_consistencia(matriz)
        print(f"Pesos alternativas - Subcriterio {i} ({archivo}):", pesos_alt)
        print(f"Consistencia alternativas - Subcriterio {i}:", cr_alt)
        pesos_alternativas.append(pesos_alt)

    # ==============================
    # 6. SÍNTESIS GLOBAL
    # ==============================
    ranking_final = sintetizar_global(pesos_criterios, pesos_social, pesos_org, pesos_terr, pesos_alternativas)

    cadenas = {
        "CP1": "CP - HORTALIZAS",
        "CP2": "CP - CUY",
        "CP3": "CP - GALLINAS",
        "CP4": "CP - PALTA",
        "CP5": "CP - TRUCHA",
        "CP6": "CP - CRIANZA DE PORCINOS",
        "CP7": "CP - QUINUA"
    }

    resultados = pd.DataFrame({
        "Cadena Productiva": [cadenas[f"CP{i+1}"] for i in range(7)],
        "Ponderación Global": ranking_final
    }).sort_values(by="Ponderación Global", ascending=False)

    print("\n--- Ranking final de las 7 cadenas productivas ---")
    print(resultados.to_string(index=False))

    resultados.to_csv("ranking_cadenas_productivas.csv", index=False, encoding="utf-8-sig")
    print("\n✅ Ranking exportado a 'ranking_cadenas_productivas.csv'")

if __name__ == "__main__":
    main()
