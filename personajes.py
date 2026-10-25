from abc import ABC, abstractmethod
from math import floor


class Personaje(ABC):
    def __init__(self, nombre, vida, ataque, defensa):
        self.nombre = nombre
        self.vida = vida
        self.ataque = ataque
        self.defensa = defensa

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre debe ser un texto no vacío.")
        self.__nombre = valor.strip()

    @property
    def vida(self):
        return self.__vida

    @vida.setter
    def vida(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise TypeError("La vida debe ser un número entero.")
        if not 0 <= valor <= 100:
            raise ValueError("La vida debe estar entre 0 y 100.")
        self.__vida = valor

    @property
    def ataque(self):
        return self.__ataque

    @ataque.setter
    def ataque(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise TypeError("El ataque debe ser un número entero.")
        if valor <= 0:
            raise ValueError("El ataque debe ser positivo.")
        self.__ataque = valor

    @property
    def defensa(self):
        return self.__defensa

    @defensa.setter
    def defensa(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise TypeError("La defensa debe ser un número entero.")
        if valor < 0:
            raise ValueError("La defensa no puede ser negativa.")
        self.__defensa = valor

    def recibir_danio(self, cantidad):
        if isinstance(cantidad, bool) or not isinstance(cantidad, int):
            raise TypeError("El daño debe ser un número entero.")
        if cantidad < 0:
            raise ValueError("El daño no puede ser negativo.")

        danio_efectivo = min(cantidad, self.vida)
        self.vida -= danio_efectivo
        return danio_efectivo

    def esta_vivo(self):
        return self.vida > 0

    def mostrar_estado(self):
        return (
            f"{self.nombre} | Vida: {self.vida} | "
            f"Ataque: {self.ataque} | Defensa: {self.defensa}"
        )

    def _validar_objetivo(self, objetivo):
        if not isinstance(objetivo, Personaje):
            raise TypeError("El objetivo debe ser un personaje.")
        if not self.esta_vivo():
            raise ValueError(f"{self.nombre} no puede atacar porque está derrotado.")
        if not objetivo.esta_vivo():
            raise ValueError(f"{objetivo.nombre} ya está derrotado.")
        if objetivo is self:
            raise ValueError("Un personaje no puede atacarse a sí mismo.")

    @abstractmethod
    def atacar(self, objetivo):
        pass


class Guerrero(Personaje):
    def atacar(self, objetivo):
        self._validar_objetivo(objetivo)
        danio = max(0, floor(self.ataque * 1.20) - objetivo.defensa)
        return objetivo.recibir_danio(danio)


class Mago(Personaje):
    def atacar(self, objetivo):
        self._validar_objetivo(objetivo)
        return objetivo.recibir_danio(self.ataque)


class Arquero(Personaje):
    def atacar(self, objetivo):
        self._validar_objetivo(objetivo)
        if self.ataque > objetivo.defensa:
            danio_base = max(0, self.ataque - objetivo.defensa)
            danio = danio_base * 2
        else:
            danio = 0
        return objetivo.recibir_danio(danio)


class Combate:
    MAX_RONDAS = 50

    def __init__(self, personaje1, personaje2):
        if not isinstance(personaje1, Personaje) or not isinstance(personaje2, Personaje):
            raise TypeError("Combate requiere dos objetos Personaje.")
        if personaje1 is personaje2:
            raise ValueError("Un personaje no puede combatir contra sí mismo.")
        self.personaje1 = personaje1
        self.personaje2 = personaje2
        self.turno_actual = personaje1
        self.ganador = None
        self.empate = False
        self.rondas = 0

    def cambiar_turno(self):
        self.turno_actual = (
            self.personaje2 if self.turno_actual is self.personaje1 else self.personaje1
        )
        return self.turno_actual

    def verificar_ganador(self):
        if not self.personaje1.esta_vivo() and not self.personaje2.esta_vivo():
            self.ganador = None
            self.empate = True
        elif not self.personaje1.esta_vivo():
            self.ganador = self.personaje2
            self.empate = False
        elif not self.personaje2.esta_vivo():
            self.ganador = self.personaje1
            self.empate = False
        else:
            self.ganador = None
            return False
        return True

    def iniciar(self):
        if not self.personaje1.esta_vivo() or not self.personaje2.esta_vivo():
            self.verificar_ganador()
            self.mostrar_resultado()
            return self.ganador

        self.turno_actual = self.personaje1
        for ronda in range(1, self.MAX_RONDAS + 1):
            self.rondas = ronda
            danio_en_ronda = 0

            for _ in range(2):
                atacante = self.turno_actual
                objetivo = (
                    self.personaje2 if atacante is self.personaje1 else self.personaje1
                )

                if atacante.esta_vivo() and objetivo.esta_vivo():
                    danio = atacante.atacar(objetivo)
                    danio_en_ronda += danio
                    print(f"Ronda {ronda}: {atacante.nombre} causa {danio} de daño a {objetivo.nombre}.")
                    print(f"  {self.personaje1.mostrar_estado()}")
                    print(f"  {self.personaje2.mostrar_estado()}")

                if self.verificar_ganador():
                    self.mostrar_resultado()
                    return self.ganador

                self.cambiar_turno()

            if danio_en_ronda == 0:
                self.empate = True
                self.mostrar_resultado("Empate técnico: ambos personajes completaron la ronda sin causar daño.")
                return None

        self.empate = True
        self.mostrar_resultado(
            f"Empate: se completaron {self.MAX_RONDAS} rondas sin un ganador."
        )
        return None

    def mostrar_resultado(self, mensaje=None):
        if mensaje:
            print(mensaje)
        elif self.ganador:
            print(f"Ganador: {self.ganador.nombre}")
        elif self.empate:
            print("El combate terminó en empate.")
        else:
            print("El combate todavía no tiene un resultado.")
