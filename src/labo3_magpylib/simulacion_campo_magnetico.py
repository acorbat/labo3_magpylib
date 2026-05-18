from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import magpylib as magpy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


_LONGITUD_A_METROS = {
    "m": 1.0,
    "cm": 1e-2,
    "mm": 1e-3,
}

_CAMPO_A_TESLA = {
    "T": 1.0,
    "mT": 1e-3,
    "uT": 1e-6,
}


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
    """
    Envoltorio sencillo sobre Magpylib para actividades introductorias.

    La clase trabaja internamente en unidades SI, tal como recomienda Magpylib 5:
    - longitud en metros [m]
    - corriente en ampere [A]
    - campo magnético en tesla [T]

    Para facilitar la transición desde materiales antiguos del laboratorio,
    los métodos de visualización permiten mostrar resultados en mm, cm, mT o uT.
    """

    def __init__(self, fuente, nombre: str = "fuente"):
        self.fuente = fuente
        self.nombre = nombre

    @classmethod
    def iman_cilindrico(
        cls,
        polarizacion: Sequence[float] = (0, 0, 1.2),
        dimension: Sequence[float] = (0.015, 0.005),
        posicion: Sequence[float] = (0, 0, 0),
        nombre: str = "imán cilíndrico",
    ) -> "SimulacionCampoMagnetico":
        """
        Crea un imán cilíndrico uniforme.

        Parameters
        ----------
        polarizacion:
            Vector de polarización en tesla.
        dimension:
            Tupla (diámetro, altura) en metros.
        posicion:
            Posición del centro del imán en metros.
        """
        fuente = magpy.magnet.Cylinder(
            polarization=tuple(polarizacion),
            dimension=tuple(dimension),
            position=tuple(posicion),
        )
        return cls(fuente=fuente, nombre=nombre)

    @classmethod
    def solenoide_discreto(
        cls,
        corriente: float = 1.0,
        radio: float = 0.01,
        largo: float = 0.04,
        espiras: int = 20,
        centro: Sequence[float] = (0, 0, 0),
        nombre: str = "solenoide discreto",
    ) -> "SimulacionCampoMagnetico":
        """
        Aproxima un solenoide mediante una colección de espiras circulares.

        Parameters
        ----------
        corriente:
            Corriente en ampere.
        radio:
            Radio de cada espira en metros.
        largo:
            Longitud total del solenoide en metros.
        espiras:
            Cantidad de espiras igualmente espaciadas.
        centro:
            Centro geométrico del solenoide en metros.
        """
        cx, cy, cz = np.asarray(centro, dtype=float)
        zs = np.linspace(-largo / 2, largo / 2, espiras)
        coleccion = magpy.Collection()
        for z in zs:
            espira = magpy.current.Circle(
                current=float(corriente),
                diameter=2 * float(radio),
                position=(cx, cy, cz + z),
            )
            coleccion.add(espira)
        return cls(fuente=coleccion, nombre=nombre)

    def campo(self, puntos: Sequence[Sequence[float]]) -> np.ndarray:
        """Devuelve el campo magnético B en tesla para una lista de puntos."""
        puntos = np.asarray(puntos, dtype=float)
        return np.asarray(magpy.getB(self.fuente, puntos), dtype=float)

    def medir_en_puntos(
        self,
        puntos: Sequence[Sequence[float]],
        etiquetas: Iterable[str] | None = None,
        unidad_longitud: str = "m",
        unidad_campo: str = "mT",
    ) -> pd.DataFrame:
        """
        Calcula el campo en puntos arbitrarios y devuelve una tabla amigable.
        """
        puntos = np.asarray(puntos, dtype=float)
        B = self.campo(puntos)
        B_mod = np.linalg.norm(B, axis=1)

        long_factor = self._factor_longitud(unidad_longitud)
        field_factor = self._factor_campo(unidad_campo)

        data = {
            f"x [{unidad_longitud}]": puntos[:, 0] / long_factor,
            f"y [{unidad_longitud}]": puntos[:, 1] / long_factor,
            f"z [{unidad_longitud}]": puntos[:, 2] / long_factor,
            f"Bx [{unidad_campo}]": B[:, 0] / field_factor,
            f"By [{unidad_campo}]": B[:, 1] / field_factor,
            f"Bz [{unidad_campo}]": B[:, 2] / field_factor,
            f"|B| [{unidad_campo}]": B_mod / field_factor,
        }
        tabla = pd.DataFrame(data)
        if etiquetas is not None:
            tabla.insert(0, "punto", list(etiquetas))
        return tabla

    def perfil_eje(
        self,
        eje: str = "z",
        rango: tuple[float, float] = (0.01, 0.15),
        n: int = 200,
        punto_base: Sequence[float] = (0, 0, 0),
        unidad_longitud: str = "m",
        unidad_campo: str = "mT",
    ) -> pd.DataFrame:
        """
        Muestra cómo varía el campo sobre un eje cartesiano.

        Parameters
        ----------
        eje:
            Uno de 'x', 'y' o 'z'.
        rango:
            Intervalo en metros donde se toman los puntos.
        n:
            Cantidad de puntos del barrido.
        punto_base:
            Punto fijo desde el cual se modifica la coordenada elegida.
        """
        eje = eje.lower()
        indices = {"x": 0, "y": 1, "z": 2}
        if eje not in indices:
            raise ValueError("eje debe ser 'x', 'y' o 'z'")

        puntos = np.repeat(np.asarray(punto_base, dtype=float)[None, :], n, axis=0)
        coordenada = np.linspace(rango[0], rango[1], n)
        puntos[:, indices[eje]] = coordenada

        B = self.campo(puntos)
        B_mod = np.linalg.norm(B, axis=1)

        long_factor = self._factor_longitud(unidad_longitud)
        field_factor = self._factor_campo(unidad_campo)

        return pd.DataFrame(
            {
                f"{eje} [{unidad_longitud}]": coordenada / long_factor,
                f"Bx [{unidad_campo}]": B[:, 0] / field_factor,
                f"By [{unidad_campo}]": B[:, 1] / field_factor,
                f"Bz [{unidad_campo}]": B[:, 2] / field_factor,
                f"|B| [{unidad_campo}]": B_mod / field_factor,
            }
        )

    def mapa_plano(
        self,
        plano: str = "xz",
        rango1: tuple[float, float] = (-0.05, 0.05),
        rango2: tuple[float, float] = (-0.05, 0.05),
        n1: int = 80,
        n2: int = 80,
        fijo: float = 0.0,
        unidad_longitud: str = "m",
    ) -> ResultadoMapa:
        """
        Calcula el campo en una malla regular dentro de un plano.
        """
        plano = plano.lower()
        if plano not in {"xy", "xz", "yz"}:
            raise ValueError("plano debe ser 'xy', 'xz' o 'yz'")

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

        factor = self._factor_longitud(unidad_longitud)
        return ResultadoMapa(
            plano=plano,
            coord1=coord1 / factor,
            coord2=coord2 / factor,
            puntos=puntos,
            B=B,
            B_mod=B_mod,
            ejes=ejes,
            unidad_longitud=unidad_longitud,
        )

    def graficar_perfil_eje(
        self,
        eje: str = "z",
        componente: str | None = None,
        rango: tuple[float, float] = (0.01, 0.15),
        n: int = 200,
        punto_base: Sequence[float] = (0, 0, 0),
        unidad_longitud: str = "cm",
        unidad_campo: str = "mT",
        ax=None,
    ):
        tabla = self.perfil_eje(
            eje=eje,
            rango=rango,
            n=n,
            punto_base=punto_base,
            unidad_longitud=unidad_longitud,
            unidad_campo=unidad_campo,
        )
        if componente is None:
            componente = f"B{eje.lower()} [{unidad_campo}]"
        if componente not in tabla.columns:
            raise ValueError(
                f"componente debe ser una de: {', '.join(c for c in tabla.columns if c != tabla.columns[0])}"
            )
        if ax is None:
            _, ax = plt.subplots(figsize=(7, 4))
        ax.plot(tabla.iloc[:, 0], tabla[componente], lw=2)
        ax.set_xlabel(tabla.columns[0])
        ax.set_ylabel(componente)
        ax.set_title(f"{self.nombre}: perfil sobre el eje {eje}")
        ax.grid(True, alpha=0.3)
        return ax, tabla

    def graficar_mapa(
        self,
        plano: str = "xz",
        rango1: tuple[float, float] = (-0.05, 0.05),
        rango2: tuple[float, float] = (-0.05, 0.05),
        n1: int = 80,
        n2: int = 80,
        fijo: float = 0.0,
        unidad_longitud: str = "cm",
        unidad_campo: str = "mT",
        mostrar_vectores: bool = True,
        ax=None,
    ):
        mapa = self.mapa_plano(
            plano=plano,
            rango1=rango1,
            rango2=rango2,
            n1=n1,
            n2=n2,
            fijo=fijo,
            unidad_longitud=unidad_longitud,
        )
        if ax is None:
            _, ax = plt.subplots(figsize=(6, 5))

        field_factor = self._factor_campo(unidad_campo)
        intensidad = mapa.B_mod / field_factor
        cont = ax.contourf(mapa.coord1, mapa.coord2, intensidad, levels=30, cmap="viridis")

        if mostrar_vectores:
            i1 = self._indice_eje(mapa.ejes[0])
            i2 = self._indice_eje(mapa.ejes[1])
            salto = max(1, min(n1, n2) // 20)
            ax.quiver(
                mapa.coord1[::salto, ::salto],
                mapa.coord2[::salto, ::salto],
                mapa.B[::salto, ::salto, i1] / field_factor,
                mapa.B[::salto, ::salto, i2] / field_factor,
                color="white",
                alpha=0.9,
                scale=None,
            )

        ax.set_xlabel(f"{mapa.ejes[0]} [{unidad_longitud}]")
        ax.set_ylabel(f"{mapa.ejes[1]} [{unidad_longitud}]")
        ax.set_title(f"{self.nombre}: |B| en el plano {plano}")
        ax.set_aspect("equal")
        plt.colorbar(cont, ax=ax, label=f"|B| [{unidad_campo}]")
        return ax, mapa

    @staticmethod
    def _indice_eje(eje: str) -> int:
        return {"x": 0, "y": 1, "z": 2}[eje]

    @staticmethod
    def _factor_longitud(unidad: str) -> float:
        if unidad not in _LONGITUD_A_METROS:
            raise ValueError(f"Unidad de longitud no soportada: {unidad}")
        return _LONGITUD_A_METROS[unidad]

    @staticmethod
    def _factor_campo(unidad: str) -> float:
        if unidad not in _CAMPO_A_TESLA:
            raise ValueError(f"Unidad de campo no soportada: {unidad}")
        return _CAMPO_A_TESLA[unidad]
