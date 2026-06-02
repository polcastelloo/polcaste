[chuleta_python.md](https://github.com/user-attachments/files/28505749/chuleta_python.md)
# 🐍 Chuleta de Python para el Bootcamp

> Guía rápida para tener al lado mientras haces ejercicios, notebooks y prácticas.  
> Objetivo: no memorizar todo, sino saber **qué herramienta usar** y **cómo se escribe**.

---

## 1. Variables

Una variable es una “cajita” donde guardas un dato.

```python
numero = 20
nombre = "Pol"
activo = True
humedad = 35.5
```

### Importante

```python
=   # asigna un valor
==  # compara dos valores
```

Ejemplo:

```python
x = 10      # guardo 10 en x
x == 10     # pregunto si x vale 10
```

---

## 2. Tipos básicos de datos

```python
int       # número entero: 10
float     # número decimal: 10.5
str       # texto: "hola"
bool      # verdadero/falso: True / False
list      # lista: [1, 2, 3]
dict      # diccionario: {"nombre": "Pol"}
None      # nada / vacío
```

Ejemplo:

```python
edad = 25
precio = 3.50
producto = "fresa"
madura = True
fresas = ["fresa1", "fresa2", "fresa3"]
```

---

## 3. Operadores matemáticos

```python
+   # suma
-   # resta
*   # multiplicación
/   # división
//  # división entera
%   # resto de una división
**  # potencia
```

Ejemplos:

```python
5 + 2     # 7
5 * 2     # 10
5 ** 2    # 25
10 % 2    # 0
11 % 2    # 1
```

El `%` se usa mucho para saber si un número es par:

```python
if numero % 2 == 0:
    print("Par")
```

---

## 4. Comparaciones

```python
==   # igual a
!=   # distinto de
>    # mayor que
<    # menor que
>=   # mayor o igual
<=   # menor o igual
```

Ejemplo:

```python
humedad = 25

if humedad < 30:
    print("Regar")
```

---

## 5. Condicionales: `if`, `elif`, `else`

Sirven para tomar decisiones.

```python
if condicion:
    hacer_algo()
elif otra_condicion:
    hacer_otra_cosa()
else:
    hacer_algo_si_no()
```

Ejemplo:

```python
temperatura = 35

if temperatura > 30:
    print("Hace calor")
elif temperatura > 20:
    print("Temperatura buena")
else:
    print("Hace frío")
```

---

## 6. `and`, `or`, `not`

```python
and  # se tienen que cumplir las dos condiciones
or   # basta con que se cumpla una
not  # niega la condición
```

Ejemplo con `and`:

```python
fresa_madura = True
confianza = 0.9

if fresa_madura and confianza > 0.8:
    print("Recoger")
```

Ejemplo con `or`:

```python
if temperatura > 35 or humedad < 20:
    print("Alerta")
```

Ejemplo con `not`:

```python
emergencia = False

if not emergencia:
    print("Sistema puede funcionar")
```

---

## 7. Listas

Una lista guarda varios elementos.

```python
frutas = ["manzana", "fresa", "kiwi"]
```

### Acceder a elementos

```python
frutas[0]   # "manzana"
frutas[1]   # "fresa"
frutas[-1]  # "kiwi"
```

Recuerda: las listas empiezan en **0**, no en 1.

### Añadir elemento

```python
frutas.append("uva")
```

### Eliminar elemento

```python
frutas.remove("fresa")
```

### Longitud de una lista

```python
len(frutas)
```

### Cortar una lista: slicing

```python
frutas[:2]   # primeros 2 elementos
frutas[1:]   # desde posición 1 hasta el final
frutas[1:3]  # desde posición 1 hasta antes de 3
```

---

## 8. Bucles `for`

Sirven para recorrer listas o repetir acciones.

```python
for fruta in frutas:
    print(fruta)
```

Ejemplo:

```python
numeros = [1, 2, 3]

for numero in numeros:
    print(numero)
```

Resultado:

```text
1
2
3
```

---

## 9. `range()`

Sirve para generar una secuencia de números.

```python
for i in range(5):
    print(i)
```

Resultado:

```text
0
1
2
3
4
```

Del 1 al 10:

```python
for i in range(1, 11):
    print(i)
```

---

## 10. Funciones

Una función es una máquina pequeña: le entran datos, hace algo y devuelve un resultado.

```python
def nombre_funcion(entrada):
    return salida
```

Ejemplo:

```python
def doble(numero):
    return numero * 2
```

Uso:

```python
doble(5)
```

Devuelve:

```text
10
```

Ejemplo con decisión:

```python
def decidir_riego(humedad):
    if humedad < 30:
        return "Regar"
    else:
        return "No regar"
```

---

## 11. `return` vs `print`

### `print`

Muestra algo en pantalla.

```python
print("Hola")
```

### `return`

Devuelve un resultado que puede usarse después.

```python
def doble(numero):
    return numero * 2
```

Regla rápida:

```text
Si solo quieres ver algo mientras pruebas → print
Si quieres que la función devuelva algo útil → return
```

En Codewars y ejercicios de funciones, casi siempre necesitarás `return`.

---

## 12. Indentación

En Python los espacios importan.

Correcto:

```python
if humedad < 30:
    print("Regar")
```

Incorrecto:

```python
if humedad < 30:
print("Regar")
```

Después de `if`, `for`, `def`, `else`, etc., lo de dentro va metido a la derecha.

Normalmente son **4 espacios** o una pulsación de **Tab**.

---

## 13. Diccionarios

Un diccionario guarda datos con claves.

```python
fresa = {
    "madurez": 0.92,
    "x": 340,
    "y": 180,
    "confianza": 0.87
}
```

Acceder a un dato:

```python
fresa["madurez"]
```

Ejemplo:

```python
if fresa["madurez"] > 0.85:
    print("Fresa madura")
```

Esto te será útil para representar datos de fresas detectadas por cámara.

---

## 14. Errores típicos

### Olvidar dos puntos

Mal:

```python
if x > 10
```

Bien:

```python
if x > 10:
```

### Mala indentación

Mal:

```python
def saludar():
print("Hola")
```

Bien:

```python
def saludar():
    print("Hola")
```

### Confundir `=` y `==`

Mal:

```python
if x = 10:
```

Bien:

```python
if x == 10:
```

### Usar una variable antes de crearla

Mal:

```python
print(resultado)
resultado = 10
```

Bien:

```python
resultado = 10
print(resultado)
```

---

## 15. Git básico

Ver estado:

```bash
git status
```

Añadir cambios:

```bash
git add .
```

Guardar punto de control:

```bash
git commit -m "mensaje"
```

Subir a GitHub:

```bash
git push
```

Bajar cambios:

```bash
git pull
```

Clonar repo:

```bash
git clone URL
```

---

## 16. Terminal básica en Windows / PowerShell

Ver archivos:

```powershell
dir
```

Entrar en una carpeta:

```powershell
cd nombre_carpeta
```

Salir una carpeta atrás:

```powershell
cd ..
```

Crear carpeta:

```powershell
mkdir sprint_1
```

Abrir VS Code en esa carpeta:

```powershell
code .
```

---

## 17. Jupyter

Abrir Jupyter local con Python 3.10:

```bash
py -3.10 -m notebook
```

Cerrar Jupyter:

```text
Ctrl + C en la consola
```

Ejecutar celda:

```text
Shift + Enter
```

Cambiar celda a Markdown:

```text
Esc + M
```

Cambiar celda a código:

```text
Esc + Y
```

---

## 18. Markdown básico

Título:

```markdown
# Título grande
## Subtítulo
### Subtítulo pequeño
```

Negrita:

```markdown
**texto en negrita**
```

Lista:

```markdown
- elemento 1
- elemento 2
- elemento 3
```

Código:

````markdown
```python
def saludar():
    return "Hola"
```
````

---

## 19. Patrón mental para resolver ejercicios

Cuando veas un ejercicio, pregúntate:

```text
1. ¿Qué entra?
2. ¿Qué tengo que devolver?
3. ¿Necesito una condición if?
4. ¿Necesito recorrer una lista con for?
5. ¿Necesito guardar algo en una variable?
6. ¿Necesito return o print?
```

Ejemplo:

```text
Entra: una lista de fresas
Proceso: revisar cuáles están maduras
Sale: lista de fresas recogibles
```

---

## 20. Ejemplo aplicado a fresas

```python
fresas = [
    {"madurez": 0.92, "confianza": 0.87},
    {"madurez": 0.60, "confianza": 0.95},
    {"madurez": 0.88, "confianza": 0.70}
]

fresas_recogibles = []

for fresa in fresas:
    if fresa["madurez"] > 0.85 and fresa["confianza"] > 0.8:
        fresas_recogibles.append(fresa)

print(fresas_recogibles)
```

Idea:

```text
Recorro todas las fresas.
Si una fresa está madura y el modelo tiene confianza suficiente,
la añado a la lista de fresas recogibles.
```

---

## Regla final

No necesitas memorizar todo. Necesitas entender el mapa:

```text
qué entra → qué proceso hago → qué sale → cómo lo pruebo
```

La chuleta es tu herramienta de taller.
