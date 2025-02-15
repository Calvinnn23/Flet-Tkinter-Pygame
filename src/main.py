import flet as ft
import random
import os

palabras = ["Manolo", "Maximiliano", "Auditore"]
max_intentos = 7
rest_intentos = max_intentos
alfabeto = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"


# * Elegir palabra
def elegir_palabra(palabras):
    palabra = random.choice(palabras).upper()
    letras = list(palabra)
    return letras


# * Mostrar guiones
def mostrar_guiones(palabra):
    guiones = list("_" * len(palabra))
    return guiones


# * Mostrar imagenes
def mostrar_imagenes():
    ruta = os.path.join(os.path.dirname(__file__), "images")
    imagenes = [
        os.path.join(ruta, img) for img in os.listdir(ruta) if img.endswith(".png")
    ]
    return imagenes


# * Validar letra
def validar_letra(
    pagina, letra, guiones_display, imagenes_display, mensaje_display, palabra, guiones
):
    global rest_intentos

    if letra in palabra:
        for i, l in enumerate(palabra):
            if l == letra:
                guiones[i] = letra
        guiones_display.value = " ".join(guiones)
        guiones_display.update()
    else:
        rest_intentos -= 1
        imagenes_display.src = mostrar_imagenes()[max_intentos - rest_intentos]
        imagenes_display.update()

    if "_" not in guiones:
        mensaje_display.value = "Melany, Ganaste"
        mensaje_display.update()
        desactivar_botones(pagina)
    elif rest_intentos == 0:
        mensaje_display.color = "red"
        mensaje_display.value = f"F, Perdiste, la palabra era: {"".join(palabra)}"
        mensaje_display.update()
        desactivar_botones(pagina)


# * Desactivar botones
def desactivar_botones(pagina):
    for control in pagina.controls[1].controls:
        control.disabled = True
    pagina.update()


# * Crear botones
def crear_botones(
    letra, pagina, guiones_display, imagenes_display, mensaje_display, palabra, guiones
):
    def on_click(e):
        e.control.disabled = True
        e.control.update()
        validar_letra(
            pagina,
            letra,
            guiones_display,
            imagenes_display,
            mensaje_display,
            palabra,
            guiones,
        )

    boton = ft.ElevatedButton(letra, on_click=on_click)
    return boton


# * main
def main(pagina: ft.Page):
    pagina.title = "Juego del ahorcado"
    palabra = elegir_palabra(palabras)
    guiones = mostrar_guiones(palabra)
    guiones_display = ft.Text(" ".join(guiones), size=30)
    imagenes_display = ft.Image(mostrar_imagenes()[0], width=400, height=400)
    mensaje_display = ft.Text("", size=50, color="green")

    letras_botones = [
        crear_botones(
            letra,
            pagina,
            guiones_display,
            imagenes_display,
            mensaje_display,
            palabra,
            guiones,
        )
        for letra in alfabeto
    ]
    botones_display = ft.Row(controls=letras_botones, wrap=True, spacing=5)

    pagina.add(guiones_display, botones_display, imagenes_display, mensaje_display)


# * Correr main
ft.app(target=main)
