# AHP Chain Global Invest - Modelo de Decisión Multicriterio

## Resumen Ejecutivo
Este repositorio contiene el script de priorización de cadenas productivas de la plataforma Chain Global Invest:

https://chainglobalinvest.com/

Desarrollada por **José Alan Párraga Condezo**. Está diseñada para el análisis multicriterio de siete cadenas productivas de Andahuaylas (Perú) en su primera versión demo.

## Metodología y Fundamento Matemático
El motor decisor se basa en el **Proceso Analítico Jerárquico (AHP)**, incorporando la técnica de **Agregación de Prioridades Individuales (AIP)**. Este marco metodológico garantiza:
* **Rigor Matemático:** Cálculo preciso de pesos de prioridad y descomposición de autovectores.
* **Validación de Consistencia:** Monitoreo automatizado de la Razón de Consistencia (CR) para asegurar la confiabilidad de los juicios de los expertos.
* **Escalabilidad Operativa:** Estructurado para gestionar conjuntos complejos de datos orientados al análisis territorial, pero bajo las consignas y disposiciones técnicas recomendadas por Thomás Satty.

## Arquitectura del Proyecto
* **`motor-chain-global-invest-demo.py`**: Script principal que gestiona la ejecución del motor de decisión AHP.
* **Datos (`*.csv`)**: Repositorio de matrices de comparación por pares y conjuntos de datos de evaluación multicriterio para priorizar cadenas productivas.
* **Dependencias**: Construido sobre librerías como `pandas` y `numpy`.

## Propiedad intelectual
* **Autor**: José Alan Párraga Condezo.
* **Modelado**: Realidad productiva bajo el contexto de la provincia de Andahuaylas en el marco del programa de estado PROCOMPITE de la república del Perú.
* **License**: CC BY-NC 4.0

## Ejecución Local
Para desplegar el modelo en tu entorno local, asegúrate de tener Python instalado y ejecuta los siguientes comandos en tu terminal:

```bash
# Instalar las dependencias necesarias
pip install -r requirements.txt
