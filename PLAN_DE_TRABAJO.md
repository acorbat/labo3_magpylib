# Plan de trabajo

## Objetivo general
Preparar material docente actualizado para el Laboratorio de Electricidad y Magnetismo usando **Magpylib 5**, con foco en ejemplos simples, reproducibles y ejecutables tanto en una computadora local como en **Google Colab**.

## Acciones a realizar
1. **Inicializar el proyecto con Pixi** para fijar dependencias y entorno reproducible.
2. **Versionar el trabajo con Git** desde el inicio.
3. **Diseñar una clase actualizada** que simplifique el uso de Magpylib para alumnos.
4. **Preparar un notebook didáctico** con al menos dos casos simples:
   - campo de un imán cilíndrico
   - campo de un solenoide modelado con espiras
5. **Generar diapositivas** en formato Quarto para acompañar la clase y mostrar código + resultados.
6. **Documentar el proyecto** con instrucciones de uso local, en Colab y de renderizado de diapositivas.
7. **Resumir el estado del proyecto** en un archivo de contexto.
8. **Crear el repositorio GitHub y subir el contenido** si hay autenticación disponible.

## Criterios de diseño
- Priorizar ejemplos cortos y visuales.
- Explicar el cambio de unidades respecto de materiales antiguos.
- Hacer que el notebook pueda correr en Colab sin depender del entorno local.
- Mantener una versión reutilizable del código en `src/`.
- Dejar tareas de Pixi para facilitar uso futuro.

## Entregables previstos
- `pixi.toml`
- `src/labo3_magpylib/simulacion_campo_magnetico.py`
- `notebooks/01_introduccion_magpylib.ipynb`
- `slides/clase_magpylib.qmd`
- `README.md`
- `CONTEXTO.md`

## Estrategia de implementación
1. Configurar entorno.
2. Crear módulo Python reutilizable.
3. Generar notebook autoexplicativo.
4. Crear diapositivas con el mismo hilo pedagógico.
5. Probar importación y ejecución básica.
6. Registrar cambios en Git y publicar en GitHub.
