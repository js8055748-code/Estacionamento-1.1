from datetime import datetime
from database import conectar


class Movimentacao:
    VALOR_HORA = 5.0  # valor por hora

    @classmethod
    def registrar_entrada(cls, placa: str) -> None:
        if not placa:
            raise ValueError("Placa não pode ser vazia.")

        conn = None
        try:
            agora = datetime.now().isoformat(timespec="seconds")
            conn = conectar()
            cur = conn.cursor()

            # Verifica se já existe entrada aberta para a placa
            cur.execute("""
                SELECT id FROM movimentacoes
                WHERE placa = ? AND saida IS NULL
                LIMIT 1
            """, (placa.strip().upper(),))

            if cur.fetchone():
                raise Exception("Já existe uma entrada aberta para esta placa.")

            cur.execute(
                """
                INSERT INTO movimentacoes (placa, entrada)
                VALUES (?, ?)
                """,
                (placa.strip().upper(), agora)
            )

            conn.commit()

        except Exception as e:
            raise Exception(f"Erro ao registrar entrada: {e}")

        finally:
            if conn:
                conn.close()

    @classmethod
    def registrar_saida(cls, placa: str):
        if not placa:
            raise ValueError("Placa não pode ser vazia.")

        conn = None
        try:
            conn = conectar()
            cur = conn.cursor()

            cur.execute("""
                SELECT id, entrada FROM movimentacoes
                WHERE placa = ? AND saida IS NULL
                ORDER BY id DESC
                LIMIT 1
            """, (placa.strip().upper(),))

            row = cur.fetchone()
            if not row:
                return None

            mov_id, entrada_str = row
            entrada_dt = datetime.fromisoformat(entrada_str)
            saida_dt = datetime.now()

            horas = (saida_dt - entrada_dt).total_seconds() / 3600
            if horas < 1:
                horas = 1

            valor = round(horas * cls.VALOR_HORA, 2)

            cur.execute("""
                UPDATE movimentacoes
                SET saida = ?, valor = ?
                WHERE id = ?
            """, (
                saida_dt.isoformat(timespec="seconds"),
                valor,
                mov_id
            ))

            conn.commit()
            return valor

        except Exception as e:
            raise Exception(f"Erro ao registrar saída: {e}")

        finally:
            if conn:
                conn.close()