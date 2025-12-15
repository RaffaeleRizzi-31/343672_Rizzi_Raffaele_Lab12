from database.DB_connect import DBConnect
from model.rifugio import Rifugio as r
from model.connessione import Connessione as c

class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    # TODO
    @staticmethod
    def getAllrifugi():
        conn = DBConnect.get_connection()
        result = []
        query = """SELECT * FROM rifugio"""
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        for row in cursor:
            result.append(r(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllconnessioni_for_year(year : int):
        conn = DBConnect.get_connection()
        result = []
        query = """SELECT
                        id_rifugio1 AS id1,
                        id_rifugio2 AS id2,
                        difficolta,
                        distanza
                    FROM
                        connessione
                    WHERE
                        anno <= %s;
                    """
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query,(year,))
        for row in cursor:
            weight = 0
            if row['difficolta'] == "facile":
                weight = 1 * float(row['distanza'])
            elif row['difficolta'] == "media":
                weight = 1.5 * float(row['distanza'])
            else:
                weight = 2 * float(row['distanza'])
            result.append(c(row["id1"], row["id2"], weight))
        cursor.close()
        conn.close()
        return result