import pytest

from personajes import Personaje, Guerrero, Mago, Arquero, Combate


def test_creacion_de_tres_personajes():
    assert Guerrero("A", 100, 10, 0).esta_vivo()
    assert Mago("B", 80, 20, 5).esta_vivo()
    assert Arquero("C", 70, 15, 3).esta_vivo()


@pytest.mark.parametrize("vida", [-1, 101])
def test_rechaza_vida_fuera_de_rango(vida):
    with pytest.raises(ValueError):
        Guerrero("A", vida, 10, 0)


def test_rechaza_nombre_vacio():
    with pytest.raises(ValueError):
        Mago("   ", 50, 10, 0)


def test_rechaza_ataque_y_defensa_invalidos():
    with pytest.raises(ValueError):
        Guerrero("A", 50, 0, 0)
    with pytest.raises(ValueError):
        Guerrero("A", 50, 10, -1)


def test_personaje_es_abstracto():
    with pytest.raises(TypeError):
        Personaje("A", 50, 10, 0)


def test_danio_de_guerrero_redondeado_hacia_abajo():
    atacante = Guerrero("A", 100, 30, 0)
    objetivo = Mago("B", 100, 10, 10)
    assert atacante.atacar(objetivo) == 26
    assert objetivo.vida == 74


def test_mago_ignora_defensa():
    atacante = Mago("A", 100, 40, 0)
    objetivo = Guerrero("B", 100, 10, 30)
    assert atacante.atacar(objetivo) == 40
    assert objetivo.vida == 60


def test_arquero_duplica_danio_si_supera_defensa():
    atacante = Arquero("A", 100, 35, 0)
    objetivo = Guerrero("B", 100, 10, 15)
    assert atacante.atacar(objetivo) == 40
    assert objetivo.vida == 60


def test_arquero_no_hace_danio_si_no_supera_defensa():
    atacante = Arquero("A", 100, 15, 0)
    objetivo = Guerrero("B", 100, 10, 15)
    assert atacante.atacar(objetivo) == 0
    assert objetivo.vida == 100


def test_vida_no_puede_ser_negativa_y_danio_es_efectivo():
    objetivo = Mago("B", 10, 10, 0)
    assert objetivo.recibir_danio(50) == 10
    assert objetivo.vida == 0


def test_no_acepta_danio_negativo():
    objetivo = Mago("B", 10, 10, 0)
    with pytest.raises(ValueError):
        objetivo.recibir_danio(-1)


def test_personaje_derrotado_no_puede_atacar():
    atacante = Guerrero("A", 0, 20, 0)
    objetivo = Mago("B", 50, 10, 0)
    with pytest.raises(ValueError):
        atacante.atacar(objetivo)


def test_combate_identifica_ganador():
    atacante = Mago("A", 100, 100, 0)
    objetivo = Guerrero("B", 10, 1, 0)
    combate = Combate(atacante, objetivo)
    assert combate.iniciar() is atacante


def test_empate_tecnico_sin_danio():
    arquero1 = Arquero("A", 50, 5, 5)
    arquero2 = Arquero("B", 50, 5, 5)
    combate = Combate(arquero1, arquero2)
    assert combate.iniciar() is None
    assert combate.empate is True
