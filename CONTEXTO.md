# Contexto del proyecto

## Propósito
Este repositorio contiene material actualizado para enseñar usos introductorios de **Magpylib** a estudiantes de Física que cursan el Laboratorio de Electricidad y Magnetismo.

## Idea pedagógica
Se busca que los alumnos puedan:
- crear una fuente magnética simple
- calcular el campo magnético en puntos del espacio
- visualizar perfiles y mapas de campo
- comparar resultados numéricos con intuiciones físicas

## Decisiones tomadas
- Se usa **Magpylib 5**.
- Se gestiona el entorno con **Pixi**.
- Se incluye un **notebook ejecutable en Google Colab**.
- Se incorpora una **clase simplificada** en `src/` para ocultar detalles repetitivos de Magpylib.
- Se agregan **diapositivas en Quarto** para clase.

## Casos incluidos
1. **Imán cilíndrico**: perfil del campo sobre el eje y medición en puntos.
2. **Solenoide discreto**: mapa del campo en un plano y comparación cualitativa con lo esperado.

## Estado esperado
Al finalizar, el proyecto debe quedar listo para:
- abrirse localmente con Pixi
- ejecutarse como notebook en Colab
- mostrarse en clase como diapositivas
- versionarse con Git
- subirse a GitHub
