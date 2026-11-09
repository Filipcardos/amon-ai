"""Simulações matemáticas ilustrativas, independentes de respostas da IA."""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP


def _centavos(valor: Decimal) -> Decimal:
    return valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def simular_juros_compostos(
    capital_inicial: float,
    aporte_mensal: float,
    taxa_mensal_pct: float,
    meses: int,
) -> dict:
    """Projeta juros compostos com aportes no FIM de cada mês.

    Taxa mensal em porcentagem, ex.: 1 corresponde a 1% ao mês.
    Taxas e valores são hipotéticos; sem impostos, inflação ou tarifas.
    """
    capital = Decimal(str(capital_inicial))
    aporte = Decimal(str(aporte_mensal))
    taxa_pct = Decimal(str(taxa_mensal_pct))

    if capital < 0 or aporte < 0:
        raise ValueError("Capital inicial e aporte mensal não podem ser negativos.")
    if taxa_pct < -100:
        raise ValueError("A taxa não pode ser inferior a -100% ao mês.")
    if not isinstance(meses, int) or not 1 <= meses <= 600:
        raise ValueError("O prazo deve ser entre 1 e 600 meses.")

    taxa = taxa_pct / Decimal("100")
    saldo = capital
    evolucao = [{"Mês": 0, "Saldo": float(_centavos(saldo))}]

    for mes in range(1, meses + 1):
        saldo = saldo * (1 + taxa) + aporte
        evolucao.append({"Mês": mes, "Saldo": float(_centavos(saldo))})

    total_investido = capital + aporte * meses
    return {
        "valor_final": _centavos(saldo),
        "total_investido": _centavos(total_investido),
        "rendimento": _centavos(saldo - total_investido),
        "evolucao": evolucao,
    }
