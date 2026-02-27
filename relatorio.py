from database import conectar

class Relatorio:
    @classmethod
    def clientes(cls):
        conn = conectar()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                c.id,
                c.nome,
                c.cpf,
                c.placa,
                c.tipo,
                IFNULL(m.valor, 0)
            FROM clientes c
            LEFT JOIN movimentacoes m
                ON m.placa = c.placa
            ORDER BY c.nome
        """)

        rows = cur.fetchall()
        conn.close()
        return rows