import uuid
from odm2_main import *

class Run():

    def __init__(self):
        """Carrega o DataFrame"""
        self.dataframe = df
        self.odm = KmlToOdm2()

    def resultado(self):
        """Insere todos os dados no Banco ODM2"""

        flagbesta = 0

        pin = len(self.dataframe)
        barra = 0
        incremento = 100/pin
        for item in self.dataframe.iterrows():

            if item[1][7] == '':
                aux='01/01/1900'
            else:
                aux = item[1][7]

            #Inserindo Resultados
            resultuuid = str(uuid.uuid4())
            self.odm.result_inserte(resultuuid, item[0], "H2O", aux, item[1][8], "H2O", 1)

            #Inserindo MeasurementResult em Resultados
            self.odm.cur.execute("SELECT * FROM ODM2.Results")
            resuid = self.odm.cur.fetchall()
            if item[1][21] != '':
                self.odm.measuresul_inserte(resuid[-1][0], item[1][30], item[1][31], item[1][21], item[1][20])
            else:
                self.odm.measuresul_inserte(resuid[-1][0], item[1][30], item[1][31], 'Sem_dado', item[1][20])

            #Inserindo valores em MeasurementResult
            self.odm.cur.execute("SELECT * FROM ODM2.MeasurementResults")
            meresul = self.odm.cur.fetchall()
            self.odm.resultvalues_inserte(meresul[-1][0], item[1][17], item[1][5], item[1][6])

            #Inserindo Anotações para Resultados
            #bacia
            self.odm.annotation_insert("MeasurementResults", "Bacia", item[1][12])
            self.odm.cur.execute("SELECT * FROM ODM2.Annotations")
            anotid = self.odm.cur.fetchall()
            self.odm.resultvalues_anotacao(resuid[-1][0], anotid[-1][0], item[1][5], item[1][7])

            #notas e observações
            #try:
            if str(item[1][32]) != '':
                aux = "%s %s    %s" %(str(item[1][32]), str(item[1][33]), str(item[1][34]))
                self.odm.annotation_insert("ResultValues", "observacoes_importantes", aux)
                self.odm.cur.execute("SELECT * FROM ODM2.Annotations")
                reanoid = self.odm.cur.fetchall()
                self.odm.measuresul_anotacao(resuid[-1][0], reanoid[-1][0])
                #print("Nota Criada!")
            #except:
                #flagbesta+=1
                #print("Não foi preciso Nota")

            #Inserindo Anotações para MeasurementResult
            #Processo, Portaria e ano da portaria
            ppstring = "PROCESSO " + str(item[1][2]) + " E PORTARIA " + str(item[1][3])
            self.odm.annotation_insert("ResultValues", "Processo_Portaria", ppstring)
            self.odm.cur.execute("SELECT * FROM ODM2.Annotations")
            anotid = self.odm.cur.fetchall()
            self.odm.measuresul_anotacao(resuid[-1][0], anotid[-1][0])

            #Pleito e Finalidade
            self.odm.annotation_insert("MeasurementResults", item[1][9], item[1][10])
            self.odm.cur.execute("SELECT * FROM ODM2.Annotations")
            anotid = self.odm.cur.fetchall()
            self.odm.measuresul_anotacao(resuid[-1][0], anotid[-1][0])

            barra += incremento
            print("%.3f%%  DADO INSERIDO COMPLETAMENTE - %d de %d" %(barra, item[0]+1, pin))



#maint
teste = Run()
teste.odm.cvs_create()
teste.odm.sf_create()
teste.odm.unit_insert()
teste.resultado()
