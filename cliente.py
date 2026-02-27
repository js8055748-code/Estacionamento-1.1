from database import conectar


class Clientes:
    @classmethod
    def cadastrar(cls, nome: str, cpf: str, placa: str, tipo: str) -> None:
        # Validação básica
        if not nome or not cpf or not placa or not tipo:
            raise ValueError("Todos os campos devem ser preenchidos.")

        conn = None
        try:
            conn = conectar()
            cur = conn.cursor()

            cur.execute(
                """
                INSERT INTO clientes (nome, cpf, placa, tipo)
                VALUES (?, ?, ?, ?)
                """,
                (nome.strip(), cpf.strip(), placa.strip(), tipo.strip())
            )

            conn.commit()

        except Exception as e:
            # Repassa o erro para a interface tratar
            raise Exception(f"Erro ao cadastrar cliente: {e}")

        finally:
            if conn:
                conn.close()