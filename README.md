# labo3_magpylib

Material para alumnos del **Laboratorio de Electricidad y Magnetismo** sobre uso introductorio de **Magpylib**.

La idea de este repositorio es que puedan abrir un notebook ya preparado, ejecutarlo paso a paso y explorar simulaciones simples de:

- una **bobina modelada como colección de espiras**
- una **bobina helicoidal** un poco más detallada
- un **imán cilíndrico** como ejemplo extra

---

## Qué archivo tengo que abrir

El notebook principal del curso es:

- `notebooks/01_introduccion_magpylib.ipynb`

Si van a trabajar localmente en su computadora, ese es el archivo que tienen que abrir con Jupyter.

---

## Opción 1: usarlo en Google Colab

Si no quieren instalar nada en su computadora, pueden:

1. descargar o subir este repositorio,
2. abrir en Colab el archivo `notebooks/01_introduccion_magpylib.ipynb`,
3. ejecutar las celdas en orden.

El notebook ya tiene una celda inicial para instalar dependencias si hiciera falta.

---

## Opción 2: usarlo localmente con Pixi

Esta es la opción recomendada si van a trabajar varias veces con el material.

### ¿Qué es Pixi?

**Pixi** es una herramienta que arma un entorno de trabajo con las versiones correctas de Python y de las bibliotecas necesarias. Eso evita tener que instalar paquetes uno por uno.

En este proyecto, Pixi instala y configura automáticamente:

- Python
- Jupyter
- Magpylib
- NumPy
- Matplotlib
- Pandas
- Quarto

---

## Paso 1: instalar Pixi

### En Windows

La forma más directa es abrir **PowerShell** y ejecutar:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://pixi.sh/install.ps1 | iex"
```

Cuando termine, cierren la terminal y ábranla de nuevo.

### Verificar que quedó instalado

En una terminal nueva, escriban:

```bash
pixi --version
```

Si aparece un número de versión, entonces Pixi quedó bien instalado.

### Si necesitan ayuda extra

La documentación oficial de instalación está en:

- https://pixi.sh/latest/

---

## Paso 2: ubicarse en la carpeta correcta del proyecto

Antes de ejecutar nada, tienen que abrir una terminal **dentro de la carpeta del repositorio** `labo3_magpylib`.

### Forma recomendada en Windows

1. Abran el explorador de archivos.
2. Entren en la carpeta del proyecto `labo3_magpylib`.
3. Hagan **Shift + clic derecho** en un espacio vacío de la carpeta.
4. Elijan una opción similar a:
   - **Abrir en Terminal**
   - **Open in Terminal**
   - o, en algunas versiones de Windows, **Abrir ventana de PowerShell aquí**
5. Se abrirá una terminal ya ubicada en esa carpeta.

### ¿Cómo verificar que estoy en la carpeta correcta?

Escriban:

```bash
pwd
```

La ruta debería terminar en algo parecido a:

```text
.../labo3_magpylib
```

Si usan `cmd`, también pueden mirar la línea actual de la terminal o usar:

```cmd
cd
```

---

## Paso 3: instalar el entorno del proyecto

Una vez dentro de la carpeta correcta, ejecuten:

```bash
pixi install
```

Esto puede tardar unos minutos la primera vez.

Pixi descargará automáticamente todas las dependencias necesarias.

---

## Paso 4: abrir Jupyter con el notebook correcto

Este repositorio ya trae tareas de Pixi para abrir directamente el notebook que tienen que usar.

### Abrir con JupyterLab

```bash
pixi run lab
```

Esta tarea:

- usa el entorno correcto del proyecto,
- verifica que todo esté funcionando,
- y abre directamente `notebooks/01_introduccion_magpylib.ipynb`.

### Abrir con Jupyter Notebook clásico

Si prefieren la interfaz clásica:

```bash
pixi run notebook
```

---

## Qué hacer una vez que se abre Jupyter

1. Verifiquen que esté abierto el archivo:
   - `notebooks/01_introduccion_magpylib.ipynb`
2. Ejecuten las celdas **en orden**, de arriba hacia abajo.
3. Modifiquen parámetros y vuelvan a correr las celdas para explorar.

---

## Tareas útiles de Pixi

### Comprobar que todo está bien instalado

```bash
pixi run chequear
```

### Abrir el notebook en JupyterLab

```bash
pixi run lab
```

### Abrir el notebook en Jupyter Notebook clásico

```bash
pixi run notebook
```

### Renderizar las diapositivas

```bash
pixi run render-slides
```

Esto genera el archivo:

- `slides/clase_magpylib.html`

---

## Diapositivas

El archivo fuente de las diapositivas es:

- `slides/clase_magpylib.qmd`

La versión renderizada en HTML es:

- `slides/clase_magpylib.html`

### ¿Por qué antes no se veían en GitHub?

Había dos motivos:

1. el archivo HTML renderizado no estaba siendo versionado,
2. GitHub no muestra un `.html` como presentación interactiva dentro del listado de archivos del repositorio.

Para verlas como sitio web hay que publicarlas con **GitHub Pages**.

Cuando GitHub Pages esté activo, el enlace esperado será:

- https://acorbat.github.io/labo3_magpylib/slides/clase_magpylib.html

---

## Contenido del repositorio

- `notebooks/01_introduccion_magpylib.ipynb`: notebook principal para alumnos
- `slides/clase_magpylib.qmd`: fuente de las diapositivas
- `slides/clase_magpylib.html`: diapositivas renderizadas
- `pixi.toml`: configuración del entorno y tareas de Pixi
- `CONTEXTO.md`: resumen del proyecto
- `PLAN_DE_TRABAJO.md`: planificación general

---

## Si algo no funciona

Prueben, en este orden:

1. cerrar la terminal y volver a abrirla en la carpeta correcta,
2. verificar que `pixi --version` funcione,
3. correr de nuevo:

```bash
pixi install
```

4. luego ejecutar:

```bash
pixi run chequear
```

Si eso funciona, prueben otra vez con:

```bash
pixi run lab
```

---

## Repositorio

- GitHub: https://github.com/acorbat/labo3_magpylib
