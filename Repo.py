import numpy as np

from Obiect import Obiect
import random
import matplotlib.pyplot as plt


class Repo:
    def __init__(self):
        self.__nrObiecte = 0
        self.__vectorObiecte = []
        self.__greutateMax = 0

    def readFromFile(self, numeFisier):  # citire din fisier
        '''
        Function that read data from file
        :param numeFisier: the name off file
        :return:
        '''
        with open(numeFisier) as reader:
            nrObiecte1 = reader.readline().strip()  # pe prima linie se afla numarul de obiecte
            self.__nrObiecte = int(nrObiecte1)
            for i in range(self.__nrObiecte):
                obj = Obiect(0,0,0)
                linie = reader.readline().strip().split(' ')
                obj.index = int(linie[0])  # indexul obiectului
                obj.valoare = int(linie[1])  # valoarea obiectului
                obj.greutate = int(linie[2])  # greutatea obiectului
                self.__vectorObiecte.append(obj)  # se adauga intr-un vector de obiecte, obiectul de pe fiecare linie
            greutateMaxx = reader.readline().strip()  # pe ultima linie se afla greutatea maxima care se poate introduce
            self.__greutateMax = int(greutateMaxx)

    # generam random un sir de biti
    def generareSir(self):
        '''
        Function that generate a random list of objects
        :return: subsir - list of object
        '''
        subsir = [0 for i in range(self.__nrObiecte)]
        for i in range(self.__nrObiecte):
            subsir[i] = random.randint(0, 1)
        return subsir

    # calculam greutatea sirului
    def greutate(self, sir):
        '''
        Function that calculate the weigth
        :param sir: list of objects
        :return: suma : the weigth that was calculate
        '''
        suma = 0
        i = 0
        for obj in self.__vectorObiecte:
            suma = suma + sir[i] * obj.greutate
            i = i + 1
        return suma

    # verificam daca e solutie
    def eSolutie(self, gr):
        '''
        Function that verify if gr is valid weigth
        :param gr: weight
        :return: true or false
        '''
        if (gr <= self.__greutateMax):
            return True
        return False

    # calculam fitness-ul solutiei
    def fitness(self, solutie):
        '''
        Function that calculate the fitness of solution
        :param solutie: a list of objects
        :return: suma: fitness
        '''
        suma = 0
        i = 0
        for obj in self.__vectorObiecte:
            suma = suma + solutie[i] * obj.valoare
            i = i + 1
        return suma

    # generez o lista de solutii
    def listaIndivizi(self, nrIndivizi):
        '''
        Function that return a list of index that are accepted by weigth
        :param nrIndivizi: number of subjects
        :return:list of index
        '''
        listaInd = []
        sir = []
        i = 0
        while i < nrIndivizi:
            gasit = 0
            while gasit == 0:  # tot generez un sir pana obtin o solutie
                sir = Repo.generareSir(self)
                greutateSir = Repo.greutate(self, sir)
                if Repo.eSolutie(self, greutateSir):
                    gasit = 1
            listaInd.append(sir)
            i = i + 1
        return listaInd

    # lista care contine pe pozitia i fitness-ul individului de pe pozitia i
    def listaFitness(self, listaInd):
        '''
        Function that calculate the fitness for listInd (subjects)
        :param listaInd: list of index
        :return: listaFitnes list of fitness
        '''
        listaFitnes = []
        for i in range(len(listaInd)):
            fitnes = Repo.fitness(self, listaInd[i])
            listaFitnes.append(fitnes)
        return listaFitnes

    # generez un k aleator si aleg k indivizi din lista si returnez individul cu cel mai bun fitness
    def turnir(self, listaInd, numarIndivizi):
        '''
        Function that generate random k and calculate k random subject  and return the best subject
        :param listaInd:list of subject
        :param numarIndivizi: number of subjects
        :return: sol: best subject
        '''
        nr = random.randint(1, numarIndivizi)
        max = 0
        sol = [0 for i in range(self.__nrObiecte)]
        for i in range(0, nr):
            j = random.randint(0, numarIndivizi - 1)
            if Repo.fitness(self, listaInd[j]) > max:
                max = Repo.fitness(self, listaInd[j])
                sol = listaInd[j][:]
        return sol

    # generez 2 descendenti prin incrucisare
    def Incrucisare(self, parinte1, parinte2):
        '''
        Function that generate two descendants by crossing
        :param parinte1: first parent
        :param parinte2:second parent
        :return: copil1, copil2: kids
        '''
        punctTaietura = random.randint(1, self.__nrObiecte - 2)
        copil1 = parinte1[:punctTaietura] + parinte2[punctTaietura:]
        copil2 = parinte2[:punctTaietura] + parinte1[punctTaietura:]
        return copil1, copil2

    # generez o lista de parinti si o lista de descendenti prin incrucisare
    def generareParinti_Descendenti(self, nrIndivizi, listaInd):
        '''
        Function that generates a list of parents and a list of descendants by cross
        :param nrIndivizi:number of subjects
        :param listaInd:subjects
        :return:listaIncrucisari : list of list of children
                 listaParinti : list of parents
        '''
        listaIncrucisari = []
        listaParinti = []
        i = 0
        while i < nrIndivizi:
            parinte1 = Repo.turnir(self, listaInd, nrIndivizi)
            parinte2 = Repo.turnir(self, listaInd, nrIndivizi)
            listaParinti.append(parinte1)
            listaParinti.append(parinte2)
            copiiValizi = False
            while copiiValizi == False:
                copil1, copil2 = Repo.Incrucisare(self, parinte1, parinte2)
                gr1 = Repo.greutate(self, copil1)
                gr2 = Repo.greutate(self, copil2)
                if Repo.eSolutie(self, gr1) == True and Repo.eSolutie(self, gr2) == True:
                    copiiValizi = True
                    listaIncrucisari.append(copil1)
                    listaIncrucisari.append(copil2)
            i = i + 1
        return listaIncrucisari, listaParinti

    # generez o mutatie a unui copil dat ca si parametru
    def mutatie(self, copil, probabilitateMutatie):
        '''
        Function that generates a mutation of a given child as a parameter
        :param copil: kid
        :param probabilitateMutatie:probability of mutation
        :return:copil:kid
        '''
        for i in range(len(copil)):
            nr = random.random()
            if nr > probabilitateMutatie:
                if copil[i] == 1:
                    copil[i] = 0
                else:
                    copil[i] = 1
        return copil

    # pentru fiecare descendent din lista, realizez o mutatie
    def generareMutatii(self, listaCopii, probabilitateMutatie):
        '''
        Function that generates a mutation for each descendant in the list
        :param listaCopii: list of kids
        :param probabilitateMutatie: probability of mutation
        :return:mutatii : list of mutant kids
        '''
        mutatii = []
        for i in range(len(listaCopii)):
            gasit = 0
            while gasit == 0:
                copilMutant = Repo.mutatie(self, listaCopii[i], probabilitateMutatie)
                greutateCopilMutant = Repo.greutate(self, copilMutant)
                if Repo.eSolutie(self, greutateCopilMutant) == True:
                    mutatii.append(copilMutant)
                    gasit = 1
        return mutatii

    # generez lista de supravietuitori
    def generareSupravietuitori(self, listaMutatii, listaParinti, nrIndivizi):
        '''
        Function that genereate survivors list
        :param listaMutatii: list og mutant kids
        :param listaParinti: list of parents
        :param nrIndivizi: number of subjects
        :return: supravietuitori: survivors
        '''
        supravietuitori = []
        listeConcatenate = listaMutatii + listaParinti  # concatenez lista de mutatii cu lista de parinti
        listeConcatenate.sort(key=self.fitness, reverse=True)
        for i in range(nrIndivizi):
            supravietuitori.append(listeConcatenate[i])
        return supravietuitori

    def algoritmEvolutiv(self, numarIndivizi, numarMaximGeneratii, probabilitateMutatie):
        '''
        evolutionary algorithm
        :param numarIndivizi: number of subjects
        :param numarMaximGeneratii: max number of generation
        :param probabilitateMutatie: probability of mutation
        :return:bestFitness :best fitness
                bestSolutie: best solution
                aveFitness: average fitness
        '''
        t = 0
        bestFitness = []  # aici o sa pun cel mai bun fitness de la fiecare generatie
        aveFitness = []  # aici o sa pun media finess-urilor de la fiecare generatie
        bestSolutie = []  # aici o sa pun cea mai buna solutie de la fiecare generatie
        indivizi = Repo.listaIndivizi(self, numarIndivizi)
        while t < numarMaximGeneratii:
            copii, parinti = Repo.generareParinti_Descendenti(self, numarIndivizi, indivizi)
            mutatii = Repo.generareMutatii(self, copii, probabilitateMutatie)
            supravietuitori = Repo.generareSupravietuitori(self, mutatii, parinti, numarIndivizi)
            fitnessSupravietuitori = Repo.listaFitness(self,
                                                       supravietuitori)  # lista de finess-uri a supravietuitorilor
            bestFitness.append(fitnessSupravietuitori[0])
            bestSolutie.append(supravietuitori[0])
            media = np.average(fitnessSupravietuitori)  # media aritmetica a finess-urilor supravietuitorilor
            aveFitness.append(media)
            t = t + 1
            indivizi = supravietuitori[:]
        return bestFitness, bestSolutie, aveFitness

    def genereazaSolutie(self, bestF, bestS):
        '''
        Function that generate a solution
        :param bestF: best fitness
        :param bestS: best solution
        :return: maxS maxim solution
                max: best fitness
        '''
        max = 0
        for i in range(len(bestF)):
            if bestF[i] > max:
                max = bestF[i]
                maxS = bestS[i][:]
        return maxS, max

    def printToFile(self, solutie, fitness, numeFisier):  # functie de scriere in fisier a celor mai bune solutii
        '''
        Function that write to file
        :param solutie: solution
        :param fitness: fitness
        :param numeFisier: name of file
        :return: none
        '''
        with open(numeFisier, "a") as printer:
            printer.write(" solutie : " + str(solutie) )
            printer.write(" fitness: " + str(fitness))
            printer.write("\n")

    def start(self):
        '''
        Start function, main function
        :return: none
        '''
        ok = True
        while ok:
            print("0. Exit")
            print("1.AE Rucsac ")
            opt = int(input("Optiunea este: "))
            if opt == 1:
                generatii =100
                #int(input("Introduceti numarul maxim de generatii: "))
                nrIndivizi =20
                #int(input("Introduceti numarul de indivizi: "))
                probabilitate =0.7
                #float(input("Introduceti probabilitatea de mutatie: "))
                file_name="int200.txt"
                #file_name="int20.txt"
                #file_name="int200.txt"
                Repo.readFromFile(self, file_name)
                bFitness, bSolutie, listaMedii = Repo.algoritmEvolutiv(self, nrIndivizi, generatii, probabilitate)
                maxSolutie, maxFitness = Repo.genereazaSolutie(self, bFitness, bSolutie)
                Repo.printToFile(self, maxSolutie, maxFitness, "rez200.txt")
                plt.plot(bFitness, 'b')
                plt.plot(listaMedii, 'r')
                plt.show()
                self.__vectorObiecte = []
            elif opt == 0:
                ok = False
















