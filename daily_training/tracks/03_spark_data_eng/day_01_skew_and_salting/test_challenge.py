from collections import Counter
from challenge import apply_salting, replicate_dimension_table

def test_salting_distribution():
    # 1000 transacciones con la misma clave sesgada ('KEY_A')
    skewed = [{"key": "KEY_A", "amount": 100} for _ in range(1000)]
    salted = apply_salting(skewed, salt_range=5)
    
    counts = Counter(r["salted_key"] for r in salted)
    assert len(counts) == 5
    for salt_key, count in counts.items():
        # Cada bucket debería tener ~200 elementos (entre 140 y 260 por varianza aleatoria)
        assert 140 <= count <= 260, f"Distribución desbalanceada en {salt_key}: {count}"

def test_dimension_replication():
    dim = [{"key": "KEY_A", "category": "Tech"}, {"key": "KEY_B", "category": "Health"}]
    rep = replicate_dimension_table(dim, salt_range=4)
    assert len(rep) == 2 * 4
    keys = {r["salted_key"] for r in rep}
    assert "KEY_A_0" in keys and "KEY_A_3" in keys
    assert "KEY_B_0" in keys and "KEY_B_3" in keys

