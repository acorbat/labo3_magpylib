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
- El notebook principal quedó **auto-contenido**, sin depender de importar clases auxiliares externas.
- Se agregan **diapositivas en Quarto** para clase.

## Casos incluidos
1. **Bobina simplificada con `Collection`**: superposición de espiras circulares.
2. **Bobina helicoidal con `Polyline`**: modelo más detallado del conductor.
3. **Imán cilíndrico**: ejemplo adicional para explorar fuera de clase.

## Estado esperado
Al finalizar, el proyecto debe quedar listo para:
- abrirse localmente con Pixi
- ejecutarse como notebook en Colab
- mostrarse en clase como diapositivas
- versionarse con Git
- subirse a GitHub
