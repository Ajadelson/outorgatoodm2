import uuid
import psycopg2
import pandas as pd
import pandas.io.sql as psql

class Selecao():

    def __init__(self):
        self.con = psycopg2.connect(host='localhost', database='odm2',
        user='odmuser', password='odmlogin')
        self.cur = self.con.cursor()

        self.df = psql.read_sql("SELECT * FROM ODM2.Annotations INNER JOIN ODM2.ResultAnnotations ON (ODM2.Annotations.annotationid = ODM2.ResultAnnotations.annotationid) WHERE annotationcode='Bacia' ORDER BY annotationtext;", self.con)

    def bacia(self, nome):
        self.ponte = psql.read_sql("SELECT * FROM ODM2.Results INNER JOIN ODM2.ResultAnnotations ON (ODM2.Results.resultid = ODM2.ResultAnnotations.resultid)", self.con)

        self.result = pd.concat([self.df, self.ponte], axis=1).reindex(self.df.index)

        self.result = self.result[self.result['annotationtext'] == nome]
