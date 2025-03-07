import customtkinter as ctk


class Calculadora(ctk.CTk):
    def __init__(self):
        super().__init__()
        # * Configuracion de la ventana
        self.geometry("400x600")
        self.resizable(False, False)
        self.title("Calculadora")
        ctk.set_appearance_mode("dark")

        self.color_fondo = "#121212"
        self.color_boton = "#1e1e1e"
        self.color_acento = "#a288e3"

        self.configure(fg_color=self.color_fondo)
        self.expresion_ini = "0"
        self.crear_widgets()
        self.tamano_fuente_actual = 64
        self.ultimo_boton_igual = False

    # * Funcion para crear widgets
    def crear_widgets(self):
        marco_display = ctk.CTkFrame(self, fg_color=self.color_fondo)
        marco_display.pack(fill="x", padx=20, pady=(40, 10))

        signo_igual = ctk.CTkLabel(
            marco_display, text="=", font=("Arial", 45), text_color=self.color_acento
        )
        signo_igual.pack(side="left", padx=(0, 10))

        # * Display de resultado
        self.resultado = ctk.CTkEntry(
            marco_display,
            font=("Arial", 64),
            fg_color=self.color_fondo,
            text_color="white",
            border_width=0,
            justify="right",
        )
        self.resultado.pack(fill="x", expand=True)
        self.resultado.insert(0, "0")
        self.resultado.configure(state="readonly")

        # * Display de operación
        self.operacion = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 24),
            fg_color=self.color_fondo,
            text_color=self.color_acento,
            anchor="e",
        )
        self.operacion.pack(pady=(0, 40), padx=20, fill="x")

        # * Marco de botones
        marco_botones = ctk.CTkFrame(self, fg_color=self.color_fondo)
        marco_botones.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        botones = [
            "CE",
            "+/-",
            "%",
            "/",
            "7",
            "8",
            "9",
            "*",
            "4",
            "5",
            "6",
            "-",
            "1",
            "2",
            "3",
            "+",
            "0",
            ".",
            "=",
        ]

        # * Crear botones
        fila, col = 0, 0
        for boton in botones:
            if boton in ["CE", "+/-", "%", "/", "*", "-", "+", "="]:
                color = self.color_acento
                color_texto = "black"
                color_hover = self.aclarar_color(self.color_acento, 0.1)
            else:
                color = self.color_boton
                color_texto = "white"
                color_hover = self.aclarar_color(self.color_boton, 0.1)

            # Crear botón
            btn = ctk.CTkButton(
                marco_botones,
                text=boton,
                width=60,
                height=60,
                fg_color=color,
                text_color=color_texto,
                font=("Arial", 24),
                corner_radius=10,
                hover_color=color_hover,
                command=lambda x=boton: self.click_boton(x),
            )

            # * Caso para  botón '0'
            if boton == "0":
                btn.grid(
                    row=fila, column=col, columnspan=2, padx=5, pady=5, sticky="nsew"
                )
                col += 2
            else:
                btn.grid(row=fila, column=col, padx=5, pady=5, sticky="nsew")
                col += 1

            if col > 3:
                col = 0
                fila += 1

        # * Configuracion grid
        for i in range(5):
            marco_botones.grid_rowconfigure(i, weight=1)
        for i in range(4):
            marco_botones.grid_columnconfigure(i, weight=1)

    # * Funcion para aclarar color
    def aclarar_color(self, color, factor=0.1):
        # Convertir hex a RGB
        color = color.lstrip("#")
        rgb = tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))

        # Aclarar
        nuevo_rgb = [min(int(c + (255 - c) * factor), 255) for c in rgb]

        # Convertir de nuevo a hex
        return "#{:02x}{:02x}{:02x}".format(*nuevo_rgb)

    # * Funcion para manejar eventos de botones
    def click_boton(self, tecla):
        if tecla == "=":
            self.calcular()
        elif tecla == "CE":
            self.limpiar()
        elif tecla == "+/-":
            self.negar()
        elif tecla == "%":
            self.porcentaje()
        else:
            self.agregar_a_expresion(tecla)

    # * Funciones de la calculadora
    def agregar_a_expresion(self, valor):
        if self.ultimo_boton_igual:
            self.expresion_ini = str(valor)
            self.ultimo_boton_igual = False
        else:
            if self.expresion_ini == "0" or self.expresion_ini == "":
                self.expresion_ini = str(valor)
            else:
                self.expresion_ini += str(valor)
        self.actualizar_resultado()
        self.actualizar_operacion()

    # * Funcion para actualizar la operacion
    def actualizar_operacion(self):
        self.operacion.configure(text=self.expresion_ini)

    # * Funcion para calcular la expresion
    def calcular(self):
        try:
            resultado = eval(self.expresion_ini)
            self.expresion_ini = str(resultado)
        except (SyntaxError, ZeroDivisionError):
            self.expresion_ini = "Error"
        self.actualizar_resultado()
        self.actualizar_operacion()
        self.ultimo_boton_igual = True

    # * Funciones para limpiar y negar
    def limpiar(self):
        self.expresion_ini = "0"
        self.actualizar_resultado()
        self.actualizar_operacion()

    def negar(self):
        try:
            valor = float(self.resultado.get())
            self.expresion_ini = str(-valor)
        except ValueError:
            pass
        self.actualizar_resultado()
        self.actualizar_operacion()

    # * Funcion para calcular el porcentaje
    def porcentaje(self):
        try:
            valor = float(self.resultado.get())
            self.expresion_ini = str(valor / 100)
        except ValueError:
            pass
        self.actualizar_resultado()
        self.actualizar_operacion()

    # * Funcion para actualizar el resultado
    def actualizar_resultado(self):
        self.resultado.configure(state="normal")
        self.resultado.delete(0, ctk.END)
        self.resultado.insert(0, self.expresion_ini)

        # Ajustar tamaño de fuente basado en longitud del texto
        longitud_texto = len(self.expresion_ini)
        nuevo_tamano_fuente = 40 if longitud_texto > 7 else 64

        self.resultado.configure(font=("Arial", nuevo_tamano_fuente))
        self.resultado.configure(state="readonly")


# * Correr main
if __name__ == "__main__":
    app = Calculadora()
    app.mainloop()
