from decimal import Decimal

import pytest

from services.calculos import simular_juros_compostos


def test_sem_juros():
    r = simular_juros_compostos(1000, 100, 0, 12)
    assert r["valor_final"] == Decimal("2200.00")
    assert r["rendimento"] == Decimal("0.00")


def test_juros_compostos_sem_aportes():
    r = simular_juros_compostos(1000, 0, 10, 2)
    assert r["valor_final"] == Decimal("1210.00")
    assert r["rendimento"] == Decimal("210.00")


def test_aporte_ocorre_no_fim_do_mes():
    r = simular_juros_compostos(1000, 100, 10, 1)
    assert r["valor_final"] == Decimal("1200.00")
    assert r["total_investido"] == Decimal("1100.00")


def test_taxa_negativa():
    r = simular_juros_compostos(1000, 0, -10, 1)
    assert r["valor_final"] == Decimal("900.00")


@pytest.mark.parametrize("args", [(-1, 0, 1, 12), (0, -1, 1, 12), (0, 0, -101, 12), (0, 0, 1, 0), (0, 0, 1, 601)])
def test_valores_invalidos(args):
    with pytest.raises(ValueError):
        simular_juros_compostos(*args)
