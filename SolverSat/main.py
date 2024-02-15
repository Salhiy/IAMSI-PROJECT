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
    l1, l2 = [], []
    list_equipes = range(ne)
    for j in range(nj):
        for x in list_equipes:
            for y in list_equipes:
                if (x!=y) : #car une equipe ne joue pas un match avec elle meme
                    l1.append(codage(ne, nj, j, x, y))
                    l2.append(codage(ne, nj, j, y, x))
            body += au_plus_un_vrai(l2)
            body += au_plus_un_vrai(l1)
            l1.clear()
            l2.clear()
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
donc la fonction encoderC1(ne, nj) va retourner nj * ne * nbCAUV(ne-2) * 2
et pour encoderC2(ne, nj) on aura au final ne * (ne - 1) * 2 contraintes car la premiere 
boucle parcours ne equipes et la secondes ne-1, et comme la fonction au_moins_un_vrais
retourne une clause et qu'on l'appel deux fois donc au total on retourne ne*(ne-1)*2 clauses
'''

#calcul le nombre de clauses de la fonction au_plus_un_vrai
def nbCAUV(n):
    return n ** 2 - (n*(n-1)) // 2

def encoder(ne, nj):
    nbVar = nj * ne * ne
    nbClauseC1 = ne * nj * nbCAUV(ne-2) * 2
    nbClauseC2 = ne * (ne - 1)
    nbTotalClauses = nbClauseC1 + nbClauseC2
    codage = encoderC1(ne, nj) + encoderC2(ne, nj)
    return  "p cnf " + str(nbVar) + " " + str(nbTotalClauses)+ "\n" + codage

if __name__ == '__main__':
    with open('res.pl', 'w') as f:
        f.write(encoder(3, 4))