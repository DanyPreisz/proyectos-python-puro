# Proyectos en Python Puro

Proyectos realizables **solo con la biblioteca estándar** de Python. Sin frameworks ni dependencias externas. Listos para usar en Google Colab o localmente.

## Calculadora

Archivo: [`calculadora.py`](https://github.com/DanyPreisz/proyectos-python-puro/blob/main/calculadora.py)

### Características
- Modo interactivo (por defecto)
- Uso por línea de comandos
- Operaciones: `+ - * / **` (potencia), `sqrt()`, porcentaje (`%`)

### Uso en Google Colab

```python
# Descargar y ejecutar
!wget -q https://raw.githubusercontent.com/DanyPreisz/proyectos-python-puro/main/calculadora.py
!python calculadora.py
```

También puedes copiar el contenido del archivo en una celda y ejecutarlo.

### Uso local

```bash
python calculadora.py                  # modo interactivo
python calculadora.py "5 + 3 * 2"      # una expresión
python calculadora.py "sqrt(16)"
python calculadora.py -i               # forzar interactivo
```

### Ejemplos

```
>>> 10 + 5
= 15.0

>>> sqrt(81)
= 9.0

>>> 2 ** 10
= 1024.0

>>> 25%
= 0.25
```

---

Más proyectos se irán añadiendo a este repositorio.
