from servicios.indicadores import consultar_indicador
from servicios.permisos import exigir_permiso


def calcular_pago_internacional(sesion, empleado, moneda: str) -> dict:
    """Convierte el salario base (en CLP) a la moneda del país donde se ejecuta el proyecto."""
    exigir_permiso(sesion, "calcular_pagos")
    resultado = consultar_indicador(sesion, moneda)
    indicador = resultado["indicador"]
    return {"pago": round(empleado.salario_base / indicador.valor, 2), "moneda": indicador.codigo,
            "indicador": indicador, "origen": resultado["origen"], "mensaje": resultado["mensaje"]}