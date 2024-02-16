import sys
import os
import time

#nb de variables = nj * ne * ne

#fonction qui calcule l'indice k d'une variable
def codage(ne, nj, j, x, y):
    return j * ne * ne + x * ne + y + 1

#k est ecrit en base ne
def decodage(k, ne):
    j = (k-1)//(ne*ne)
    x = (k-j*ne*ne-1)//ne
    y = k - 1 - j * ne * ne - x * ne
    return j, x, y

def au_moins_un_vrai(l):
    body = ""
    for i in l:
        body += str(i) +" "
    body += "0" + "\n"
    return body

#retourne le corps et le nombre de contraintes
def au_plus_un_vrai(l):
    body = ""
    for index, i in enumerate(l):
        for j in l[index+1:]:
            body += "-"+str(i)+" -"+str(j)+" 0\n"
    return body

def encoderC1(ne, nj):
    body = ""
    l1 = []
    list_equipes = range(ne)
    for j in range(nj):
        for x in list_equipes:
            for y in list_equipes:
                if (x!=y) : #car une equipe ne joue pas un match avec elle meme
                    l1.append(codage(ne, nj, j, x, y))
                    l1.append(codage(ne, nj, j, y, x))
            body += au_plus_un_vrai(l1)
            l1.clear()
    return body


'''
    on ajoute pas le cas ou y avec x directement dans une autre liste, car
    on a que x varie dans [0,..,ne-1] et y aussi, donc on aura toutes les paires
    [0,..,ne-1] * [0,...,ne-1] - [(0,0),(1,1),...,(ne-1, ne-1)]
'''
def encoderC2(ne, nj):
    l1 = []
    body = ""
    list_equipes = range(ne)
    for x in list_equipes:
        for y in list_equipes:
            if (x!=y):
                for j in range(nj):#parcours de la liste de jours
                    l1.append(codage(ne, nj, j, x, y))
                body += au_moins_un_vrai(l1)
                l1.clear()
    return body


'''
pour le calcul du nombre de contraintes que 
genere la fonction au_plus_un_vrai(l) avec l une liste de taille len, n=len-1
il suffit de calculer la valeur suivante : 
    n+(n-1)+(n-2)+(n-3)+...+(n-(n-1)) = n+n+n+..n - (0+1+2+...+n-1)
    = n**2- ((n)*(n-1)) // 2
donc on note nbCAUV(n) = n**2- ((n)*(n-1)) // 2, le nombre de clauses de que retourne 
la fonction au_plus_un_vrai(l),
donc la fonction encoderC1(ne, nj) va retourner nj * ne * nbCAUV(2*(ne-1)-1)
et pour encoderC2(ne, nj) on aura au final ne * (ne - 1) * 2 contraintes car la premiere 
boucle parcours ne equipes et la secondes ne-1, et comme la fonction au_moins_un_vrais
retourne une clause et qu'on l'appel deux fois donc au total on retourne ne*(ne-1)*2 clauses
'''

#calcul le nombre de clauses de la fonction au_plus_un_vrai
def nbCAUV(n):
    return n ** 2 - (n*(n-1)) // 2

def encoder(ne, nj, encoderCs):
    nbVar = nj * ne * ne
    nbClauseC1 = ne * nj * nbCAUV((ne-1)*2 - 1)
    nbClauseC2 = ne * (ne - 1)
    codage = ""
    for encoderC in encoderCs:
        codage += encoderC(ne, nj)
    nbTotalClauses = nbClauseC1 + nbClauseC2
    return  "p cnf " + str(nbVar) + " " + str(nbTotalClauses)+ "\n" + codage

#recuperation du nom d'une equipe
def recuperNomEquipe(f, i):
    if f is None or not os.path.exists(f):
        return str(i)
    with open(f, 'r') as file:
        for index, ligne in enumerate(file):
            if i == index :
                return ligne.replace('\n', '')
    #erreur dans le fichier equipes
    sys.exit(-1)

def lireJour(j):
    return "Dimanche("+str(j)+")" if j % 2 == 0 else "Mercredi("+str(j)+")"

#pour lire la reponse du resultat dimacs
def liteReponse(file, equipe, ne, affiche=True):
    last_line = None
    with open(file, 'r') as f:
        for ligne in f:
            last_line = ligne.strip()
    resp = last_line.split(' ')
    if (resp[1] == 'UNSATISFIABLE'):
        if (affiche): print("pas de solution !!")
        return False #unsat
    if (affiche):
        for r in resp[1:len(resp)-1]:
            r = int(r)
            if (r>=0):
                j, x, y = (decodage(r, ne))
                print(f"l'equipe {recuperNomEquipe(equipe, x)} joue contre {recuperNomEquipe(equipe, y)} le jour {lireJour(j)}")
    return True #sat

#question 4 : trouver
def optimisation(timout=10, encoderCs=[]):
    for ne in range(3, 11):
        for nj in range(ne+2, ne*10):
            if (run(['', ne, nj], timout, affiche=False, encoderCs=encoderCs)):
                print(f'le nombre de jour minimum pour {str(ne)} equipes est de {str(nj)}')
                break

#generation des sous tableau de taille k d un tableau de taille n, en sachant 
#que l'odre n'est pas important : [1,2,3] = [3,1,2] = [3,2,1] ....
def gen_sou_tableau_k(arr, k, start=0, current=[]):
    if len(current) == k:
        return [current[:]]
    
    res = []

    for i in range(start, len(arr)):
        res.extend(gen_sou_tableau_k(arr, k, i+1, current + [arr[i]]))

    return res

'''
on genere tous les sous tableau de taille n-k+1, avec n = len(l)
donc si on a que au plus une variable est vrai dans le sous tableau, et que
on fait cela pour tous les tableau, on aura bien que au plus k variables
sont vrai,  
'''
def au_plus_k(l, k):
    if (len(l)<k-1):
        print('erreur, k est trod grand')
        sys.exit(-1)
    sous_tableau = gen_sou_tableau_k(l, len(l)-k+1)
    body = ""
    for tab in sous_tableau:
        body+=au_plus_un_vrai(tab)
    return body

'''
    C4 : 'chaque equipe joue au moins Pext% match a l'exterieur le dimanche'
'''
def encoderC4(ne, nj, pext):
    body = ""
    l1 = []
    list_equipes = range(ne)
    for x in list_equipes:
        for y in list_equipes:
            if (x!=y) : #car une equipe ne joue pas un match avec elle meme
                for j in range(nj):
                    if (j%2==1):#pour les mercredi
                        l1.append(codage(ne, nj, j, y, x))#on prends que les matchs a l'exterieurs les mercredis
        #au plus (ne-1) * (1-pext) matchs a l'exterieur le mercredie, car
        #en effet pour jouer au moins k match a l'extertieur le dimance
        #il faut jouer au plus k match a l'extertieur le mercredi avec 
        #avec une proba de 1-pext, et comme
        #chaque equipe joue au max ne-1 match a l'extertieur les dimanches 
        body += au_plus_k(l1, int((ne-1) * (1-pext)))
        l1.clear()
    return body

'''
    C5 : 'chaque equipe joue au moins Pdom% match a domicile le dimanche'
'''
def encoderC5(ne, nj, pdom):
    body = ""
    l1 = []
    list_equipes = range(ne)
    for x in list_equipes:
        for y in list_equipes:
            if (x!=y) : #car une equipe ne joue pas un match avec elle meme
                for j in range(nj):
                    if (j%2==1):#pour les mercredi
                        l1.append(codage(ne, nj, j, x, y))#on prends que les matchs a domicile les mercredis
        #au plus (ne-1) * (1-pdom) matchs a domicile le mercredie, car
        #en effet pour jouer au moins k match a domicile le dimanche
        #il faut jouer au plus k match a domicile le mercredi avec 
        #avec une proba de 1-pdom, et comme
        #chaque equipe joue au max ne-1 match a domicile les dimanches 
        body += au_plus_k(l1, int((ne-1) * (1-pdom)))
        l1.clear()
    return body

'''
    C6 : 'aucune equipe ne joue plus de 2 match consecutifs a l'exterieur'
    C7 : 'aucune equipe ne joue plus de 2 match consecutifs a domicile'
'''
def encoderC6C7(ne, nj):
    body = ""
    l1, l2 = [], []
    list_equipes = range(ne)
    overlap = False
    for x in list_equipes:
        for j in range(nj):
            for y in list_equipes:
                if (x!=y) : #car une equipe ne joue pas un match avec elle meme
                    l1.append(codage(ne, nj, j, y, x))#exterieur
                    l2.append(codage(ne, nj, j, x, y))#domicile
            if (j==1 or overlap):#on alterne les jours 
                overlap = True
                body += au_plus_un_vrai(l1)
                body += au_plus_un_vrai(l2)
                l1 = l1[len(l2)//2:]#on garde le jour courant pour la prochaine iteration
                l2 = l2[len(l2)//2:]#on garde la trace du jour courant pour pouvoir le verifier apres
                
    return body

def run(args, timeout = None, affiche=True, encoderCs=[]):
    if (len(args) < 3):
        print('Erreur dans le nombre de parametres')
        print('\tIl faut le nombre d\'equipes et le nombre de jours')
        print('\t\tpython main.py ne nj')
        print('\tExemple : ')
        print('\t\tpython main.py 4 5')
        sys.exit()
    
    ne = int(args[1])
    nj = int(args[2])

    #ecriture dans un fichier du programme pl
    with open('res.pl', "w") as f:
        f.write(encoder(ne, nj, encoderCs))
    #execution de glucose
    if timeout == None:
        command = './glucose -model res.pl > model.txt'
    else:
        command = f'timeout {timeout}s ./glucose -model res.pl > model.txt'
    start_time = time.time()
    os.system(command)
    execution_time = time.time() - start_time
    if (execution_time > timeout):
        return False

    #attends l'ecriture du fichier...
    time.sleep(0.1)
    #lecture des reponses
    return liteReponse('model.txt', 'equipes.txt', ne, affiche)

if __name__ == '__main__':
    #run(sys.argv)
    optimisation(encoderCs=[encoderC1, encoderC2])