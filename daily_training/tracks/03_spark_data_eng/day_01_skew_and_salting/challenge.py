import random
from typing import List, Dict

def apply_salting(skewed_records: List[Dict], salt_range: int = 5) -> List[Dict]:
    """
    Añade salt a los registros con sesgo para distribuir la carga.
    """
    salted = []
    for r in skewed_records:
        salt = random.randint(0, salt_range - 1)
        item = r.copy()
        item["salted_key"] = f"{r['key']}_{salt}"
        salted.append(item)
    return salted

def replicate_dimension_table(dimension_records: List[Dict], salt_range: int = 5) -> List[Dict]:
    """
    Replica la tabla de dimensión para cada valor posible de la sal.
    """
    replicated = []
    for r in dimension_records:
        for salt in range(salt_range):
            item = r.copy()
            item["salted_key"] = f"{r['key']}_{salt}"
            replicated.append(item)
    return replicated

