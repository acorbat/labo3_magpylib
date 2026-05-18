from __future__ import annotations

from pathlib import Path
import textwrap

import nbformat as nbf


FALLBACK_CLASS = r'''
from dataclasses import dataclass

import magpylib as magpy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

_LONGITUD_A_METROS = {"m": 1.0, "cm": 1e-2, "mm": 1e-3}
_CAMPO_A_TESLA = {"T": 1.0, "mT": 1e-3, "uT": 1e-6}

@dataclass
class ResultadoMapa:
    plano: str
    coord1: np.ndarray
    coord2: np.ndarray
    puntos: np.ndarray
    B: np.ndarray
    B_mod: np.ndarray
    ejes: tuple[str, str]
    unidad_longitud: str

class SimulacionCampoMagnetico:
    def __init__(self, fuente, nombre="fuente"):
        self.fuente = fuente
        self.nombre = nombre

    @classmethod
    def iman_cilindrico(cls, polarizacion=(0, 0, 1.2), dimension=(0.015, 0.005), posicion=(0, 0, 0), nombre="imán cilíndrico"):
        fuente = magpy.magnet.Cylinder(polarization=tuple(polarizacion), dimension=tuple(dimension), position=tuple(posicion))
        return cls(fuente=fuente, nombre=nombre)

    @classmethod
    def solenoide_discreto(cls, corriente=1.0, radio=0.01, largo=0.04, espiras=20, centro=(0, 0, 0), nombre="solenoide discreto"):
        cx, cy, cz = np.asarray(centro, dtype=float)
        zs = np.linspace(-largo / 2, largo / 2, espiras)
        coleccion = magpy.Collection()
        for z in zs:
            coleccion.add(magpy.current.Circle(current=float(corriente), diameter=2 * float(radio), position=(cx, cy, cz + z)))
        return cls(fuente=coleccion, nombre=nombre)

    def campo(self, puntos):
        puntos = np.asarray(puntos, dtype=float)
        return np.asarray(magpy.getB(self.fuente, puntos), dtype=float)

    def medir_en_puntos(self, puntos, etiquetas=None, unidad_longitud="m", unidad_campo="mT"):
        puntos = np.asarray(puntos, dtype=float)
        B = self.campo(puntos)
        B_mod = np.linalg.norm(B, axis=1)
        lf = _LONGITUD_A_METROS[unidad_longitud]
        cf = _CAMPO_A_TESLA[unidad_campo]
        tabla = pd.DataFrame({
            f"x [{unidad_longitud}]": puntos[:, 0] / lf,
            f"y [{unidad_longitud}]": puntos[:, 1] / lf,
            f"z [{unidad_longitud}]": puntos[:, 2] / lf,
            f"Bx [{unidad_campo}]": B[:, 0] / cf,
            f"By [{unidad_campo}]": B[:, 1] / cf,
            f"Bz [{unidad_campo}]": B[:, 2] / cf,
            f"|B| [{unidad_campo}]": B_mod / cf,
        })
        if etiquetas is not None:
            tabla.insert(0, "punto", list(etiquetas))
        return tabla

    def perfil_eje(self, eje="z", rango=(0.01, 0.15), n=200, punto_base=(0, 0, 0), unidad_longitud="m", unidad_campo="mT"):
        indices = {"x": 0, "y": 1, "z": 2}
        puntos = np.repeat(np.asarray(punto_base, dtype=float)[None, :], n, axis=0)
        coordenada = np.linspace(rango[0], rango[1], n)
        puntos[:, indices[eje]] = coordenada
        B = self.campo(puntos)
        B_mod = np.linalg.norm(B, axis=1)
        lf = _LONGITUD_A_METROS[unidad_longitud]
        cf = _CAMPO_A_TESLA[unidad_campo]
        return pd.DataFrame({
            f"{eje} [{unidad_longitud}]": coordenada / lf,
            f"Bx [{unidad_campo}]": B[:, 0] / cf,
            f"By [{unidad_campo}]": B[:, 1] / cf,
            f"Bz [{unidad_campo}]": B[:, 2] / cf,
            f"|B| [{unidad_campo}]": B_mod / cf,
        })

    def mapa_plano(self, plano="xz", rango1=(-0.05, 0.05), rango2=(-0.05, 0.05), n1=80, n2=80, fijo=0.0, unidad_longitud="m"):
        ejes = tuple(plano)
        grid1 = np.linspace(rango1[0], rango1[1], n1)
        grid2 = np.linspace(rango2[0], rango2[1], n2)
        coord1, coord2 = np.meshgrid(grid1, grid2)
        puntos = np.zeros(coord1.shape + (3,), dtype=float)
        if plano == "xy":
            puntos[..., 0] = coord1
            puntos[..., 1] = coord2
            puntos[..., 2] = fijo
        elif plano == "xz":
            puntos[..., 0] = coord1
            puntos[..., 1] = fijo
            puntos[..., 2] = coord2
        else:
            puntos[..., 0] = fijo
            puntos[..., 1] = coord1
            puntos[..., 2] = coord2
        B = self.campo(puntos.reshape(-1, 3)).reshape(puntos.shape)
        B_mod = np.linalg.norm(B, axis=-1)
        lf = _LONGITUD_A_METROS[unidad_longitud]
        return ResultadoMapa(plano=plano, coord1=coord1 / lf, coord2=coord2 / lf, puntos=puntos, B=B, B_mod=B_mod, ejes=ejes, unidad_longitud=unidad_longitud)

    def graficar_perfil_eje(self, eje="z", componente="Bz [mT]", rango=(0.01, 0.15), n=200, punto_base=(0, 0, 0), unidad_longitud="cm", unidad_campo="mT", ax=None):
        tabla = self.perfil_eje(eje=eje, rango=rango, n=n, punto_base=punto_base, unidad_longitud=unidad_longitud, unidad_campo=unidad_campo)
        if ax is None:
            _, ax = plt.subplots(figsize=(7, 4))
        ax.plot(tabla.iloc[:, 0], tabla[componente], lw=2)
        ax.set_xlabel(tabla.columns[0])
        ax.set_ylabel(componente)
        ax.set_title(f"{self.nombre}: perfil sobre el eje {eje}")
        ax.grid(alpha=0.3)
        return ax, tabla

    def graficar_mapa(self, plano="xz", rango1=(-0.05, 0.05), rango2=(-0.05, 0.05), n1=80, n2=80, fijo=0.0, unidad_longitud="cm", unidad_campo="mT", mostrar_vectores=True, ax=None):
        mapa = self.mapa_plano(plano=plano, rango1=rango1, rango2=rango2, n1=n1, n2=n2, fijo=fijo, unidad_longitud=unidad_longitud)
        if ax is None:
            _, ax = plt.subplots(figsize=(6, 5))
        cf = _CAMPO_A_TESLA[unidad_campo]
        intensidad = mapa.B_mod / cf
        cont = ax.contourf(mapa.coord1, mapa.coord2, intensidad, levels=30, cmap="viridis")
        if mostrar_vectores:
            idx = {"x": 0, "y": 1, "z": 2}
            i1 = idx[mapa.ejes[0]]
            i2 = idx[mapa.ejes[1]]
            salto = max(1, min(n1, n2) // 20)
            ax.quiver(mapa.coord1[::salto, ::salto], mapa.coord2[::salto, ::salto], mapa.B[::salto, ::salto, i1] / cf, mapa.B[::salto, ::salto, i2] / cf, color="white", alpha=0.9)
        ax.set_xlabel(f"{mapa.ejes[0]} [{unidad_longitud}]")
        ax.set_ylabel(f"{mapa.ejes[1]} [{unidad_longitud}]")
        ax.set_title(f"{self.nombre}: |B| en el plano {plano}")
        ax.set_aspect("equal")
        plt.colorbar(cont, ax=ax, label=f"|B| [{unidad_campo}]")
        return ax, mapa
'''


def main() -> None:
    nb = nbf.v4.new_notebook()
    nb.metadata.update(
        {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
            "colab": {"name": "01_introduccion_magpylib.ipynb"},
        }
    )

    cells = []

    cells.append(
        nbf.v4.new_markdown_cell(
            "# Introducción a Magpylib para Laboratorio 3\n\n"
            "Este notebook muestra dos ejemplos simples para empezar a usar **Magpylib**:\n\n"
            "1. un **imán cilíndrico**\n"
            "2. un **solenoide** modelado como una colección de espiras\n\n"
            "La idea es que puedan **calcular el campo magnético**, **graficarlo** y **medir su intensidad** en distintos puntos del espacio."
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            "## Cómo usar este notebook\n\n"
            "- **En Google Colab**: suban el archivo y ejecuten las celdas en orden.\n"
            "- **En una computadora local**: pueden abrirlo con JupyterLab usando el entorno definido por Pixi.\n\n"
            "**Importante:** Magpylib 5 usa **unidades SI**. En este notebook:\n\n"
            "- longitudes en **metros [m]**\n"
            "- corrientes en **ampere [A]**\n"
            "- campos en **tesla [T]**\n\n"
            "En los gráficos vamos a mostrar con frecuencia distancias en **cm** y campos en **mT** porque son más cómodos para laboratorio."
        )
    )

    cells.append(
        nbf.v4.new_code_cell(
            "import importlib\n"
            "import subprocess\n"
            "import sys\n\n"
            "paquetes = ['magpylib', 'numpy', 'matplotlib', 'pandas']\n"
            "faltantes = []\n"
            "for paquete in paquetes:\n"
            "    try:\n"
            "        importlib.import_module(paquete)\n"
            "    except ImportError:\n"
            "        faltantes.append(paquete)\n\n"
            "if faltantes:\n"
            "    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *faltantes])\n"
            "    print('Se instalaron:', ', '.join(faltantes))\n"
            "else:\n"
            "    print('Dependencias listas.')"
        )
    )

    cells.append(
        nbf.v4.new_code_cell(
            "from pathlib import Path\n"
            "import sys\n\n"
            "import magpylib as magpy\n"
            "import matplotlib.pyplot as plt\n"
            "import numpy as np\n"
            "import pandas as pd\n"
            "from IPython.display import display\n\n"
            "plt.style.use('seaborn-v0_8-whitegrid')\n"
            "print('Magpylib versión:', magpy.__version__)"
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            "## Clase auxiliar actualizada\n\n"
            "La siguiente celda intenta importar la clase reutilizable del repositorio. Si eso no es posible (por ejemplo, en Colab al subir solo el notebook), define una versión equivalente dentro del notebook."
        )
    )

    cells.append(
        nbf.v4.new_code_cell(
            "repo_root = Path.cwd()\n"
            "candidatos = [repo_root / 'src', repo_root.parent / 'src']\n"
            "for candidato in candidatos:\n"
            "    if candidato.exists() and str(candidato) not in sys.path:\n"
            "        sys.path.insert(0, str(candidato))\n\n"
            "try:\n"
            "    from labo3_magpylib import SimulacionCampoMagnetico\n"
            "    print('Clase importada desde src/labo3_magpylib')\n"
            "except Exception:\n"
            + textwrap.indent(FALLBACK_CLASS, "    ")
            + "\n    print('Clase definida dentro del notebook (modo portátil)')"
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            "## Caso 1: un imán cilíndrico\n\n"
            "Vamos a modelar un imán cilíndrico magnetizado en la dirección `z`. Primero observamos cómo cambia `Bz` sobre el eje del imán."
        )
    )

    cells.append(
        nbf.v4.new_code_cell(
            "iman = SimulacionCampoMagnetico.iman_cilindrico(\n"
            "    polarizacion=(0, 0, 1.2),\n"
            "    dimension=(0.015, 0.005),   # diámetro, altura [m]\n"
            "    posicion=(0, 0, 0),\n"
            "    nombre='Imán cilíndrico'\n"
            ")\n\n"
            "fig, ax = plt.subplots(figsize=(7, 4))\n"
            "ax, tabla_iman = iman.graficar_perfil_eje(\n"
            "    eje='z',\n"
            "    componente='Bz [mT]',\n"
            "    rango=(0.005, 0.12),\n"
            "    unidad_longitud='cm',\n"
            "    unidad_campo='mT',\n"
            "    ax=ax,\n"
            ")\n"
            "plt.show()\n\n"
            "display(tabla_iman.head())"
        )
    )

    cells.append(
        nbf.v4.new_code_cell(
            "puntos = [\n"
            "    (0.00, 0.00, 0.01),\n"
            "    (0.00, 0.00, 0.03),\n"
            "    (0.01, 0.00, 0.03),\n"
            "    (0.02, 0.00, 0.05),\n"
            "]\n"
            "tabla_mediciones = iman.medir_en_puntos(\n"
            "    puntos,\n"
            "    etiquetas=['A', 'B', 'C', 'D'],\n"
            "    unidad_longitud='cm',\n"
            "    unidad_campo='mT',\n"
            ")\n"
            "display(tabla_mediciones)"
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            "### Actividades sugeridas\n\n"
            "1. Cambien la **polarización** del imán y observen qué pasa con la amplitud de `Bz`.\n"
            "2. Modifiquen el **diámetro** y la **altura** del imán. ¿Qué parámetro influye más cerca del imán?\n"
            "3. Midan el campo en puntos simétricos respecto del eje. ¿Qué componentes cambian de signo y cuáles no?"
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            "## Caso 2: un solenoide discreto\n\n"
            "Ahora modelamos un solenoide como una colección de espiras circulares. Esto reproduce la idea del script viejo, pero con la API actual de Magpylib."
        )
    )

    cells.append(
        nbf.v4.new_code_cell(
            "solenoide = SimulacionCampoMagnetico.solenoide_discreto(\n"
            "    corriente=2.0,\n"
            "    radio=0.015,\n"
            "    largo=0.05,\n"
            "    espiras=25,\n"
            "    nombre='Solenoide discreto'\n"
            ")\n\n"
            "fig, ax = plt.subplots(figsize=(6, 5))\n"
            "ax, mapa = solenoide.graficar_mapa(\n"
            "    plano='xz',\n"
            "    rango1=(-0.05, 0.05),\n"
            "    rango2=(-0.05, 0.05),\n"
            "    n1=90,\n"
            "    n2=90,\n"
            "    fijo=0.0,\n"
            "    unidad_longitud='cm',\n"
            "    unidad_campo='mT',\n"
            "    mostrar_vectores=True,\n"
            "    ax=ax,\n"
            ")\n"
            "plt.show()"
        )
    )

    cells.append(
        nbf.v4.new_code_cell(
            "fig, ax = plt.subplots(figsize=(7, 4))\n"
            "ax, tabla_sol = solenoide.graficar_perfil_eje(\n"
            "    eje='z',\n"
            "    componente='Bz [mT]',\n"
            "    rango=(-0.08, 0.08),\n"
            "    punto_base=(0, 0, 0),\n"
            "    unidad_longitud='cm',\n"
            "    unidad_campo='mT',\n"
            "    ax=ax,\n"
            ")\n"
            "plt.show()\n\n"
            "display(tabla_sol.iloc[::40].reset_index(drop=True))"
        )
    )

    cells.append(
        nbf.v4.new_code_cell(
            "mediciones_sol = solenoide.medir_en_puntos(\n"
            "    [(0, 0, 0), (0, 0, 0.02), (0.01, 0, 0), (0.02, 0, 0.04)],\n"
            "    etiquetas=['centro', 'sobre eje', 'borde interno', 'afuera'],\n"
            "    unidad_longitud='cm',\n"
            "    unidad_campo='mT',\n"
            ")\n"
            "display(mediciones_sol)"
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            "## Un análisis extra: ¿qué tan rápido cae el campo lejos del imán?\n\n"
            "Lejos de una fuente localizada, el campo suele parecerse al de un dipolo y decrecer aproximadamente como una potencia de la distancia. Podemos inspeccionarlo en un gráfico log-log."
        )
    )

    cells.append(
        nbf.v4.new_code_cell(
            "tabla_lejos = iman.perfil_eje(\n"
            "    eje='z',\n"
            "    rango=(0.03, 0.15),\n"
            "    n=120,\n"
            "    unidad_longitud='m',\n"
            "    unidad_campo='T',\n"
            ")\n\n"
            "z = tabla_lejos['z [m]'].to_numpy()\n"
            "Bz = np.abs(tabla_lejos['Bz [T]'].to_numpy())\n"
            "coef = np.polyfit(np.log10(z), np.log10(Bz), deg=1)\n"
            "pendiente, ordenada = coef\n\n"
            "plt.figure(figsize=(6, 4))\n"
            "plt.loglog(z, Bz, 'o', label='Simulación')\n"
            "plt.loglog(z, 10**ordenada * z**pendiente, '-', label=f'Ajuste: B ~ z^({pendiente:.2f})')\n"
            "plt.xlabel('z [m]')\n"
            "plt.ylabel('|Bz| [T]')\n"
            "plt.legend()\n"
            "plt.show()\n\n"
            "print(f'Pendiente aproximada: {pendiente:.2f}')"
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            "## Preguntas para entregar o discutir en clase\n\n"
            "1. ¿Qué diferencia conceptual hay entre medir `Bz` y medir `|B|`?\n"
            "2. ¿Por qué conviene mirar el campo sobre el eje antes de pasar a un mapa en 2D?\n"
            "3. ¿Qué limitaciones tiene representar un solenoide real como un conjunto de espiras ideales?\n"
            "4. ¿En qué rango parece razonable una ley de potencia para el campo del imán?\n\n"
            "---\n\n"
            "**Sugerencia:** usen este notebook como base, pero agreguen sus propias celdas de exploración y comentarios."
        )
    )

    nb["cells"] = cells

    output = Path("notebooks/01_introduccion_magpylib.ipynb")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as f:
        nbf.write(nb, f)

    print(f"Notebook generado en: {output}")


if __name__ == "__main__":
    main()
