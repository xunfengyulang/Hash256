import os
import re
import pandas as pd

H=[0x6A09E667F, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19]
K_path='./K.csv'

def encrypt(textpath):
    if not os.path.exists(textpath):
       assert False, "please put the file in %s" %textpath
    with open(textpath, 'rb') as f:
        data=f.read()
    data_length=len(data)
    data+=b'\x80'
    if data_length>=pow(2,64):
        assert False, "the size of file must be less than 2^64"
    if len(data)%64!=56:
        data+=b'\x00'*((56-len(data)+64)%64)
    data+=data_length.to_bytes(8, byteorder='big')
    K=K_get(K_path)
    for i in range(len(data)//64):
        text=data[i*64:i*64+64]
        W=[0]*64
        for j in range(16):
            W[j]=int.from_bytes(text[j*4:j*4+4], byteorder='big')
        for j in range(16,64):
            W[j]=W[j-16]+sig0(W[j-15])+W[j-7]+sig1(W[j-2])
            W[j]=W[j]&0xFFFFFFFF
        for j in range(64):
            t1=sigma1(H[4])+ch(H[4],H[5],H[6])+H[7]+W[j]+K[j]
            t1=t1&0xFFFFFFFF
            t2=sigma0(H[0])+maj(H[0],H[1],H[2])
            t2=t2&0xFFFFFFFF
            H[0]=(t1+t2)&0xFFFFFFFF
            H[1]=H[0]
            H[2]=H[1]
            H[3]=H[2]
            H[4]=(H[3]+t1)&0xFFFFFFFF
            H[5]=H[4]
            H[6]=H[5]
            H[7]=H[6]
    res=b''
    for num in H:
        res+=num.to_bytes(4, byteorder='big')
    return res

def K_get(path):
    K=[]
    data=pd.read_csv(path, header=None, dtype=str)
    data=data.iloc[:,1].values.tolist()
    for r in data:
        r=re.sub(r'[^0-9A-F]','',str(r))
        r=int(r,16)
        K.append(r)
    return K

def rotr(x,n):
    return (x>>n)|(x<<(32-n))

def shr(x,n):
    return x>>n

def ch(e,f,g):
    return (e&f)^(~e&g)

def maj(a,b,c):
    return (a&b)|(a&c)|(b&c)

def sigma0(x):
    return rotr(x,2)^rotr(x,13)^rotr(x,22)

def sigma1(x):
    return rotr(x,6)^rotr(x,11)^rotr(x,25)

def sig0(x):
    return rotr(x,7)^rotr(x,18)^shr(x,3)

def sig1(x):
    return rotr(x,17)^rotr(x,19)^shr(x,10)

if __name__=='__main__':
    textpath='./hash_test.txt'
    print(encrypt(textpath))