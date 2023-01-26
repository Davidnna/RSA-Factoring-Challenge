#! /usr/bin/python

## CRACKING RSA WITH COMMON FACTORS METHOD      ##
## HACKING WEEK '14 : CRYPTO-4 CHALLENGE        ##
## GUZMUD                                       ##

import fractions
from collections import defaultdict

## MATHEMATICAL FUNCTIONS ##

# extended Euclide algorithm
# canonical implementation
def euclideEtendu(a, b):
	x,y,u,v =0,1,1,0
	while a!= 0:
		q = b//a
		r = b%a
		m = x-u*q
		n = y-v*q
		b,a,x,y,u,v = a,r,u,v,m,n
	return b,x,y

# get modular inverse of a in M
def get_invA(a, m):
	invA = 0
	if (fractions.gcd(a,m) == 1):
		g, x, y = euclideEtendu(a,m)
		invA = x%m
	return invA

## CRYPTO-4 CHALLENGE FUNCTION

def readstring(data,level=27):
    TRADTABLE = [' ','a','b','c','d','e','f','g','h','i','j','k','l','m',
                 'n','o','p','q','r','s','t','u','v','w','x','y','z']
    a = data
    t = 1
    temparray = []
    temp = 0
    
    while a != 0:
        t = a-level*(a//level)
        a = a//level
        temparray += TRADTABLE[int(t)]
        
    return ''.join(temparray)

def crypto4_cracking(weak_keys):
    pub = 2**16+1
    cypher = 97313723999427158707313571074505809044734576227366074775197337179596924131890323110047188776214753462110672927375882648122238543395136397500411230385539389860460250957019288356953382932530827442895828951533573302647648238521279077394005914829458808700551912957892108347414768602246507965856863930813172801853

    lcracked = []

    for i in weak_keys:
        # NB : here we consider len(weak_keys[i]) == 2
        temp = pow(cypher, get_invA(pub, (weak_keys[i][0]-1)*(weak_keys[i][1]-1)),(weak_keys[i][0]*weak_keys[i][1]))
        lcracked += [str(readstring(temp))]

    return lcracked

## CORE FUNCTIONS

# load and parse the input file
# formated for the moduli.txt from crypto4 challenge
def import_keys(filename):
    data = open(filename)
    t = data.read().split('[')[1].split(']')[0].split(',')
    for i in range(len(t)):
        t[i] = int(t[i].replace(' ','').replace('\n',''))
    return t

# look for common factors
# return a defaultdict with keys and factors
def find_weak_keys(keylist):
    weak_keys = defaultdict(list)
    
    for y in keylist:
        for i in keylist:
            if y != i:
                k = fractions.gcd(y,i)
                
                if k != 1:
                    if k not in weak_keys[y]:
                        weak_keys[y] += [k]
                    if k not in weak_keys[i]:
                        weak_keys[i] += [k]
    return weak_keys

# getting the other factor
def other_half(weak_keys):
    for i in weak_keys:
        for j in weak_keys[i]:
            if i/j not in weak_keys[i]:
                weak_keys[i] += [i/j]
    return weak_keys

print "HACKINGWEEK: CRYPTO4 : COMMON FACTORS\n"
print "Importing keys from moduli.txt ..."
keylist = import_keys("moduli.txt")
print "Finding the weak keys and associated factor ..."
weak_keys = find_weak_keys(keylist)
print "Getting the other factors ..."
weak_keys = other_half(weak_keys)
print "Cracking the crypto4 challenge ..."
lcracked = crypto4_cracking(weak_keys)
print "\nFindings :"
for i in lcracked:
    print "\t-"+str(i)
