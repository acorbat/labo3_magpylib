# labo3_magpylib

Material docente para una clase introductoria de **Magpylib** orientada a estudiantes del Laboratorio de Electricidad y Magnetismo.

## Contenido
- `src/labo3_magpylib/`: clase simplificada para trabajar con Magpylib.
- `notebooks/01_introduccion_magpylib.ipynb`: notebook para alumnos.
- `slides/clase_magpylib.qmd`: diapositivas para clase en Quarto.
- `PLAN_DE_TRABAJO.md`: hoja de ruta del proyecto.
- `CONTEXTO.md`: resumen ejecutivo.

## Requisitos
- [Pixi](https://pixi.sh)
- Git

## Uso local
```bash
pixi install
pixi run lab
```

## Tareas útiles
```bash
pixi run generar-notebook
pixi run render-slides
pixi run chequear
```

## Uso en Google Colab
El notebook incluye una celda inicial para instalar dependencias en Colab si hace falta. Se recomienda subir el archivo `notebooks/01_introduccion_magpylib.ipynb` directamente a Colab.

## Renderizar diapositivas
```bash
pixi run render-slides
```
El resultado esperado es un HTML en `slides/`.

## Git y GitHub
El proyecto está preparado para versionarse con Git. Si se dispone de autenticación con GitHub CLI, se puede publicar con:
```bash
gh repo create labo3_magpylib --public --source=. --remote=origin --push
```
