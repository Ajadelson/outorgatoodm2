import psycopg2
import uuid

from read_kml import *

class KmlToOdm2():

    def __init__(self):
        """Conectando com o Banco ODM2"""

        self.con = psycopg2.connect(host='localhost', database='odm2',
        user='odmuser', password='odmlogin')
        self.cur = self.con.cursor()

        self.df = df

    def result_inserte(self, uuid, feaactid, retype, valid, status, sample, valuecount):
        """Insere dados na tabela ODM2.Result"""

        try:
            self.cur.execute("SELECT * FROM ODM2.Variables")
            varid = self.cur.fetchall()
            self.cur.execute("SELECT * FROM ODM2.Units")
            unid = self.cur.fetchall()
            self.cur.execute("SELECT * FROM ODM2.ProcessingLevels")
            plid = self.cur.fetchall()
            self.cur.execute("INSERT INTO ODM2.Results (resultuuid, featureactionid, resulttypecv, variableid, unitsid, processinglevelid, validdatetime, statuscv, sampledmediumcv, valuecount) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s)", (uuid, int(feaactid), retype, varid[0][0], unid[0][0], plid[0][0], valid, status, sample, valuecount))
            self.con.commit()

            #print("Dado inserido na Tabela Result")
        except:
            print("Erro ao inserir dado na tabela Result")

    def measuresul_inserte(self, id, lat, long, fuso, duracao):
        """Insere dados na tabela ODM2.MeasurementResult"""

        try:
            self.cur.execute("SELECT * FROM ODM2.Units")

            #Tratamento de dados
            unid = self.cur.fetchall()
            if fuso == '25':
                fuso = '25L'
            if duracao == '':
                duracao = '0'

            self.cur.execute("INSERT INTO ODM2.MeasurementResults (resultid, xlocation, ylocation, censorcodecv, qualitycodecv, aggregationstatisticcv, timeaggregationinterval, timeaggregationintervalunitsid) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (id, lat.replace(',','.'), long.replace(',','.'), "VAZAO", "SUPERFICIAL", fuso, (duracao.replace(',',".")), unid[0][0]))
            self.con.commit()
            #print("Dado inserido na Tabela MeasurementResult")
        except:
            print("Erro ao inserir dado na tabela MeasurementResult")

    def resultvalues_inserte(self, id, qout, duracao, fuso):
        """Insere dados na tabela ODM2.MeasurementResultValues"""

        try:
            #Tratamento de dados
            if qout == '':
                qout = '0'

            self.cur.execute("INSERT INTO ODM2.MeasurementResultValues (resultid, datavalue, valuedatetime, valuedatetimeutcoffset)VALUES (%s,%s,%s,%s)", (id, qout.replace(',','.'), duracao, int(float(fuso.replace(',','.')))))
            self.con.commit()
            #print("Dado inserido na Tabela ResultValues")
        except:
            print("Erro ao inserir dado na tabela ResultValues")

    def annotation_insert(self, anotatype, anotacode, anotatexto):
        """Insere anotações na tabela ODM2.Annotations"""
        try:
            self.cur.execute("INSERT INTO ODM2.Annotations (annotationtypecv, annotationcode, annotationtext) VALUES (%s,%s,%s)", (anotatype, anotacode, anotatexto))
            self.con.commit()
            #print("Dado inserido na Tabela Annotations")
        except:
            print("Erro ao inserir dado na tabela Annotations")

    def measuresul_anotacao(self, valueid, annotationid):
        """Cria ponte de ODM2.MeasurementResultValues para ODM2.Annotations"""
        try:
            self.cur.execute("INSERT INTO ODM2.MeasurementResultValueAnnotations ( valueid, annotationid) VALUES (%s,%s)", (int(valueid), int(annotationid)))
            self.con.commit()
            #print("Ponte MeasurementResult para Annotations criada")
        except:
            print("Erro Ponte MeasurementResult para Annotations criada")

    def resultvalues_anotacao(self, resultid, annotationid, begindatetime, enddatetime):
        """Cria ponte de ODM2.Results para ODM2.Annotations"""

        try:
            #Tratamento de dados
            if begindatetime == '':
                begindatetime = '1/1/1900'
            if enddatetime == '':
                enddatetime = '1/1/1900'

            self.cur.execute("INSERT INTO ODM2.ResultAnnotations (resultid, annotationid, begindatetime, enddatetime) VALUES (%s,%s,%s,%s)", (int(resultid), int(annotationid), begindatetime, enddatetime))
            self.con.commit()
            #print("Ponte Results para Annotations criada")
        except:
            print("Erro Ponte Results para Annotations criada")

    def unit_insert(self):
        """Insere dados na tabela Units"""
        try:
        #inserir = "INSERT INTO ODM2.Units (unitsid, unitstypecv, unitsabbreviation, unitsname) VALUES (1, %s, %s, %s);" % ("Metros_Cubicos_Por_Segundo","m³s⁻¹","Vazao")

            self.cur.execute("INSERT INTO ODM2.Units (unitstypecv, unitsabbreviation, unitsname) VALUES (%s, %s, %s)", ("Metros_Cubicos_Por_Segundo","m³s⁻¹","Vazao"))
            self.con.commit()
            #print("Unidade inserida com sucesso.")
        except:
            print("Deu problema.")

    def cvs_create(self):
        """popula o controle de vocabulario."""

        self.cur.execute("INSERT INTO ODM2.CV_UnitsType (term, name, definition, category, sourcevocabularyuri) VALUES (%s, %s, %s, %s, %s)", ("Metros_Cubicos_Por_Segundo","Metros_Cubicos_Por_Segundo","Metros_Cubicos_Por_Segundo","Metros_Cubicos_Por_Segundo","Metros_Cubicos_Por_Segundo",))
        self.cur.execute("INSERT INTO ODM2.CV_ResultType (term, name) VALUES (%s,%s)",("H2O","H2O"))
        self.cur.execute("INSERT INTO ODM2.CV_Status (term, name) VALUES (%s,%s)",("VENCIDA","VENCIDA"))
        self.cur.execute("INSERT INTO ODM2.CV_Status (term, name) VALUES (%s,%s)",("VALIDA","VALIDA"))
        self.cur.execute("INSERT INTO ODM2.CV_CensorCode (term, name) VALUES (%s,%s)", ("VAZAO","VAZAO"))
        self.cur.execute("INSERT INTO ODM2.CV_AggregationStatistic (term, name) VALUES (%s,%s)",("Sem_dado","Sem_dado"))
        self.cur.execute("INSERT INTO ODM2.CV_AggregationStatistic (term, name) VALUES (%s,%s)",("24L","24L"))
        self.cur.execute("INSERT INTO ODM2.CV_AggregationStatistic (term, name) VALUES (%s,%s)",("25L","25L"))
        self.cur.execute("INSERT INTO ODM2.CV_Qualitycode (term, name) VALUES (%s,%s)",("SUPERFICIAL","SUPERFICIAL"))
        self.cur.execute("INSERT INTO ODM2.CV_AnnotationType (term, name) VALUES (%s,%s)",("MeasurementResults","MeasurementResults"))
        self.cur.execute("INSERT INTO ODM2.CV_AnnotationType (term, name) VALUES (%s,%s)",("ResultValues","ResultValues"))
        self.cur.execute("INSERT INTO ODM2.CV_Medium (term, name) VALUES (%s,%s)",("H2O","H2O"))
        self.cur.execute("INSERT INTO ODM2.CV_MethodType (term, name) VALUES (%s, %s)", ("OUTORGA","OUTORGA"))
        self.cur.execute("INSERT INTO ODM2.CV_SamplingFeatureType (term, name) VALUES (%s, %s)", ("Vazão_Superficial", "Vazão_Superficial"))

        lista = []
        for item in self.df["FINALIDADE"]:
            if item not in lista:
                lista.append(item)
                self.cur.execute("INSERT INTO ODM2.CV_ActionType (term, name) VALUES (%s, %s)", (item,item))

        usulista = []
        for item in self.df["USUARIO"]:
            if item not in usulista:
                usulista.append(item)
                self.cur.execute("INSERT INTO ODM2.CV_OrganizationType (term, name) VALUES (%s, %s)", (item, item))

        self.cur.execute("INSERT INTO ODM2.CV_VariableName (term, name) VALUES (%s, %s)", ("VAZÃO","VAZÃO"))
        self.cur.execute("INSERT INTO ODM2.CV_VariableType (term, name) VALUES (%s, %s)", ("Q","Q"))
        self.con.commit()

    def sf_create(self):
        """Criando SamplingFeatures"""

        sfuuid = str(uuid.uuid4())
        self.cur.execute("INSERT INTO ODM2.SamplingFeatures (samplingfeatureuuid, samplingfeaturetypecv, samplingfeaturecode) VALUES (%s, %s, %s)", (sfuuid, "Vazão_Superficial", "0001"))
        self.cur.execute("SELECT * FROM ODM2.SamplingFeatures")
        sfid = self.cur.fetchall()

        #Criando variavel
        self.cur.execute("INSERT INTO ODM2.Variables (variabletypecv, variablecode, variablenamecv, nodatavalue) VALUES (%s, %s, %s, %s)", ("Q", 1, "VAZÃO", 0))
        self.cur.execute("SELECT * FROM ODM2.Variables")
        vaid = self.cur.fetchall()

        #Criando ProcessingLevels
        self.cur.execute("INSERT INTO ODM2.ProcessingLevels (processinglevelcode) VALUES (%s)", ("Q"))
        self.cur.execute("SELECT * FROM ODM2.ProcessingLevels")
        plid = self.cur.fetchall()

        usuario = []
        metcode = 1
        for item in self.df.iterrows():
            if item[1][15] not in usuario:
                usuario.append(item[1][15])
                self.cur.execute("INSERT INTO ODM2.Organizations (organizationtypecv, organizationcode, organizationname, organizationdescription) VALUES (%s, %s, %s, %s)", (item[1][15], len(usuario), item[1][15], item[1][14]))

            self.cur.execute("SELECT * FROM ODM2.Organizations")
            organid = self.cur.fetchall()
            self.cur.execute("INSERT INTO ODM2.Methods (methodtypecv, methodcode, methodname, organizationid) VALUES (%s, %s, %s, %s)", ("OUTORGA", metcode, "OUTORGA", organid[-1][0]))
            self.cur.execute("SELECT * FROM ODM2.Methods")
            metcode += 1
            metid = self.cur.fetchall()
            if item[1][21][0:1] == '':
                aux = 25
            else:
                aux = item[1][21][0:1]
            self.cur.execute("INSERT INTO ODM2.Actions (actiontypecv, methodid, begindatetime, begindatetimeutcoffset, actiondescription) VALUES (%s, %s, %s, %s, %s)",(item[1][10], metid[-1][0], item[1][5], aux, "MUNICIPIO DE "+item[1][13]))
            self.cur.execute("SELECT * FROM ODM2.Actions")
            acid = self.cur.fetchall()
            self.cur.execute("INSERT INTO ODM2.FeatureActions (featureactionid, samplingfeatureid, actionid) VALUES (%s, %s, %s)", (item[0],sfid[0][0],acid[-1][0]))
