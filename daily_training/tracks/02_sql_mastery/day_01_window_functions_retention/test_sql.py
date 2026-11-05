from pathlib import Path
import pytest

def test_sql_execution():
    try:
        import duckdb
    except ImportError:
        pytest.skip("duckdb no está instalado aún en el entorno.")

    sql_path = Path(__file__).parent / "challenge.sql"
    query = sql_path.read_text(encoding="utf-8")

    con = duckdb.connect(database=":memory:")
    con.execute("""
        CREATE TABLE monthly_revenue (
            month_date DATE,
            product_category VARCHAR,
            revenue DECIMAL(10, 2)
        );
        INSERT INTO monthly_revenue VALUES
            ('2024-01-01', 'Cloud', 1000.00),
            ('2024-02-01', 'Cloud', 1200.00),
            ('2024-03-01', 'Cloud', 1500.00),
            ('2024-01-01', 'Hardware', 500.00),
            ('2024-02-01', 'Hardware', 450.00);
    """)

    result = con.execute(query).fetchall()
    
    # Comprobar resultados para 'Cloud'
    # Enero: prev is None, growth is None
    assert result[0][1] == 'Cloud'
    assert result[0][3] is None
    assert result[0][4] is None

    # Febrero: revenue 1200, prev 1000, growth 20.00%
    assert result[1][2] == 1200.00
    assert result[1][3] == 1000.00
    assert float(result[1][4]) == 20.00

    # Marzo: revenue 1500, prev 1200, growth 25.00%
    assert result[2][2] == 1500.00
    assert result[2][3] == 1200.00
    assert float(result[2][4]) == 25.00

