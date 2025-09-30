# utils_local.py
# Versión simple con modelo: carga al importar y funciones cortas.

import joblib
import pandas as pd

# Carga el modelo una vez
MODEL = joblib.load("modelo_credito.joblib")

# Tasa fija mensual (ejemplo: 5% mensual)
TASA_MENSUAL = 0.05

# Bandas por probabilidad de "mal pagador" (clase 1)
BANDAS_RIESGO = [
    ("Bajo",  0.00, 0.20),
    ("Medio", 0.20, 0.50),
    ("Alto",  0.50, 1.01),
]

def prob_riesgo(model, salario: float, monto: float, plazo: int) -> float:
    """
    IMPORTANTE: el pipeline del modelo espera las columnas:
    ['salario', 'monto', 'plazo']
    """
    X = pd.DataFrame({"salario": [salario], "monto": [monto], "plazo": [plazo]})
    p = model.predict_proba(X)[0, 1]
    return float(p)

def banda_riesgo(p: float) -> str:
    for nombre, lo, hi in BANDAS_RIESGO:
        if lo <= p < hi:
            return nombre
    return "N/A"

def cuota_frances(monto: float, n_cuotas: int, tasa: float = TASA_MENSUAL) -> float:
    """Cuota fija del sistema francés."""
    return monto * (tasa * (1 + tasa) ** n_cuotas) / ((1 + tasa) ** n_cuotas - 1)

def cronograma_frances(monto: float, n_cuotas: int, tasa: float = TASA_MENSUAL):
    """Tabla simple de amortización (francés) con tasa fija mensual (DataFrame)."""
    import pandas as pd
    cuota = cuota_frances(monto, n_cuotas, tasa)
    filas, saldo = [], monto
    for mes in range(1, n_cuotas + 1):
        interes = saldo * tasa
        amort   = cuota - interes
        saldo   = saldo * (1 + tasa) - cuota
        if saldo < 0: saldo = 0.0
        filas.append({
            "mes": mes,
            "interes": round(interes, 2),
            "amortizacion": round(amort, 2),
            "cuota": round(cuota, 2),
            "saldo_fin": round(saldo, 2),
        })
    return pd.DataFrame(filas)
