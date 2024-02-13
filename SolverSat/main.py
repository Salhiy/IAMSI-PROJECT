#nb de variables = nj * ne * ne

#fonction qui calcule l'indice k d'une variable
def codage(nc, nj, j, x, y):
    return j * nc * nc + x * nc + y + 1

#k est ecrit en base nc
def decodage(k, nc):
    j = (k-1)//(nc*nc)
    x = (k-j*nc*nc-1)//nc
    y = k - 1 - j * nc * nc - x * nc
    return j, x, y

def au_moins_un_vrai(l):
    body = ""
    for i in l:
        body += str(i) +" "
    body += "0"
    return body

def au_plus_un_vrai(l):
    body = ""
    for index, i in enumerate(l):
        for j in l[index+1:]:
            body += "-"+str(i)+" -"+str(j)+" 0\n"

    return body

def encoderC1(ne, nj):
    body = ""
    l1, l2 = [], []
    for j in range(nj):
        for x in range(ne):
            for y in range(ne):
                if (x!=y) : #car une equipe ne joue pas un match avec elle meme
                    l1.append(codage(ne, nj, j, x, y))
                    l2.append(codage(ne, nj, j, y, x))
            body += au_plus_un_vrai(l1) # a domicile
            body += au_plus_un_vrai(l2) # a l'exterieur
            l1.clear()
            l2.clear()
    return body

def encoderC2(ne, nj):
    l1, l2 = [], []
    for x in range(ne):
        for y in range(ne):
            for j in range(nj):
                if (x!=y):
                    l1.append(codage(ne, nj, j, x, y))
                    l2.append(codage(ne, nj, j, y, x))
            body += au_moins_un_vrai(l1)
            body += au_moins_un_vrai(l2)
            l1.clear()
            l2.clear()
    return body

def encoder(ne, nj):
    return encoderC1(ne, nj) + encoderC2(ne, nj)



print(encoderC1(3,4))

'''
nc = 10
nj = 10

k = codage(nc, nj, 1, 1, 2)
print(decodage(k, nc))
'''