from personajes import Guerrero, Mago, Arquero, Combate


def demostrar_habilidades():
    print("=== Prueba de habilidades ===")

    guerrero = Guerrero("Arthas", 100, 30, 20)
    objetivo = Mago("Rival", 100, 10, 10)
    danio = guerrero.atacar(objetivo)
    print(f"Guerrero: daño efectivo {danio}; vida del objetivo: {objetivo.vida}")

    mago = Mago("Gandalf", 80, 40, 10)
    objetivo = Guerrero("Guardia", 100, 10, 25)
    danio = mago.atacar(objetivo)
    print(f"Mago: daño efectivo {danio}; vida del objetivo: {objetivo.vida}")

    arquero = Arquero("Legolas", 90, 35, 8)
    objetivo = Guerrero("Orco", 100, 10, 15)
    danio = arquero.atacar(objetivo)
    print(f"Arquero: daño efectivo {danio}; vida del objetivo: {objetivo.vida}")


def demostrar_validaciones():
    print("\\n=== Prueba de validaciones ===")
    casos = [
        ("vida superior a 100", lambda: Guerrero("Inválido", 101, 10, 0)),
        ("vida negativa", lambda: Mago("Inválido", -1, 10, 0)),
        ("nombre vacío", lambda: Arquero("   ", 50, 10, 0)),
        ("ataque cero", lambda: Guerrero("Inválido", 50, 0, 0)),
        ("defensa negativa", lambda: Mago("Inválido", 50, 10, -1)),
    ]

    for descripcion, crear in casos:
        try:
            crear()
        except (TypeError, ValueError) as error:
            print(f"Correcto: {descripcion} rechazado ({error})")
        else:
            print(f"ERROR: se aceptó {descripcion}")


def ejecutar_combate():
    print("\\n=== Combate completo ===")
    arthas = Guerrero("Arthas", 100, 30, 20)
    gandalf = Mago("Gandalf", 80, 40, 10)
    Combate(arthas, gandalf).iniciar()


if __name__ == "__main__":
    demostrar_habilidades()
    demostrar_validaciones()
    ejecutar_combate()
