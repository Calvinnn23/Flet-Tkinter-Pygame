import pygame as pg

pg.init()

# * Configuración de la pantalla
pantalla = pg.display.set_mode((450, 450))
pg.display.set_caption("Tic Tac Toe")

# * Cargar imágenes
fondo = pg.image.load("projects/Tic Tac Toe/assets/tictactoe_background.png")
X = pg.image.load("projects/Tic Tac Toe/assets/x.png")
O = pg.image.load("projects/Tic Tac Toe/assets/circle.png")

# * Escalar imágenes
fondo = pg.transform.scale(fondo, (450, 450))
X = pg.transform.scale(X, (125, 125))
O = pg.transform.scale(O, (125, 125))

# * Dibujar fondo y tablero
coord = [
    [(40, 50), (165, 50), (290, 50)],
    [(40, 175), (165, 175), (290, 175)],
    [(40, 300), (165, 300), (290, 300)],
]

tablero = [["", "", ""], ["", "", ""], ["", "", ""]]

turno = "X"
game_over = False
clock = pg.time.Clock()


# * Graficar tablero
def graficar_tablero():
    pantalla.blit(fondo, (0, 0))

    for i in range(3):
        for j in range(3):
            if tablero[i][j] == "X":
                graficar_X(i, j)
            elif tablero[i][j] == "O":
                graficar_O(i, j)


# * Graficar X y O
def graficar_X(x, y):
    pantalla.blit(X, coord[x][y])


def graficar_O(x, y):
    pantalla.blit(O, coord[x][y])


# * Validar ganador
def validar_ganador():
    for i in range(3):
        if tablero[i][0] == tablero[i][1] == tablero[i][2] != "":
            return True
        elif tablero[0][i] == tablero[1][i] == tablero[2][i] != "":
            return True
    if tablero[0][0] == tablero[1][1] == tablero[2][2] != "":
        return True
    elif tablero[0][2] == tablero[1][1] == tablero[2][0] != "":
        return True

    return False


# * Ciclo del juego
while not game_over:
    clock.tick(30)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_over = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            clic_pos = pg.mouse.get_pos()

            for i in range(3):
                for j in range(3):
                    if coord[i][j][0] < clic_pos[0] < coord[i][j][0] + 125:
                        if coord[i][j][1] < clic_pos[1] < coord[i][j][1] + 125:
                            if tablero[i][j] == "":
                                tablero[i][j] = turno
                                if validar_ganador():
                                    # Mostrar mensaje de ganador
                                    pantalla.fill((255, 255, 255))
                                    font = pg.font.Font(None, 36)
                                    text = font.render(
                                        f"Ganó: {turno}", True, (0, 0, 0)
                                    )
                                    pantalla.blit(text, (150, 200))
                                    pg.display.update()

                                    # Esperar a presionar enter o cerrar pantall
                                    waiting = True
                                    while waiting:
                                        for event in pg.event.get():
                                            if event.type == pg.QUIT:
                                                game_over = True
                                                waiting = False
                                            elif event.type == pg.KEYDOWN:
                                                if event.key == pg.K_RETURN:
                                                    waiting = False

                                    # Limpiar el tablero
                                    tablero = [["", "", ""], ["", "", ""], ["", "", ""]]
                                    turno = "X"

                                turno = "O" if turno == "X" else "X"

    graficar_tablero()

    pg.display.update()

pg.quit()
