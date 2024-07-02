from database.DB_connect import DBConnect


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getNodi():
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """select g.GeneID, g.Chromosome 
                from genes_small.genes g 
                where g.Chromosome > 0"""

        cursor.execute(query)

        for row in cursor:
            if row["Chromosome"] in result:
                result[row["Chromosome"]].append(row["GeneID"])
            else:
                result[row["Chromosome"]] = [row["GeneID"]]

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArco(c1, c2):
        conn = DBConnect.get_connection()

        result = 0

        cursor = conn.cursor(dictionary=True)
        query = """select g.GeneID as g1, g2.GeneID  as g2, g.Chromosome as c1, g2.Chromosome as c2, i.Expression_Corr as peso 
                from genes_small.genes g, genes_small.genes g2, genes_small.interactions i 
                where g.Chromosome > 0 and g2.Chromosome = %s and g.Chromosome = %s and g.GeneID = i.GeneID1  and g2.GeneID = i.GeneID2 
                group by g1, g2"""

        cursor.execute(query, (c2, c1))

        for row in cursor:
            result += row["peso"]

        cursor.close()
        conn.close()
        return result