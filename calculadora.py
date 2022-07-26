import math
import re

def soma(n1,n2):
    resultado=float(n1)+float(n2)   
    return resultado

def subtracao(n1,n2):
    resultado=float(n1)-float(n2)   
    return resultado

def divisao(n1,n2):
    resultado=float(n1)/float(n2)   
    return resultado

def multiplicao(n1,n2):
    resultado=float(n1)*float(n2)  
    return resultado

def expoente(n1,n2):
    resultado=float(n1)**float(n2)  
    return resultado

def equacao1(exp):
    exp.pop(0)
    sinais={
        '+':'-',
        '-':'+'
    }
    aux_eq1=' '.join(exp)
    print(aux_eq1)
    antes_igual=aux_eq1.split('=')[0]
    depois_igual=aux_eq1.split('=')[1]
    if 'x' in depois_igual.split()[0] and not '-' in depois_igual.split()[0]:#se o x for o primeiro numero e for positivo
        depois_igual='+'+depois_igual
    if not 'x' in antes_igual.split()[0] and not '-' in antes_igual.split()[0]:#se o x for o primeiro numero e for positivo
        antes_igual='+ '+antes_igual
    
    antes_igual_sem_x=re.sub(r'x|[0-9]x|[+-] [0-9]x', '', antes_igual)
    antes_igual_x=re.findall(r'x|[0-9]x|[+-] [0-9]x', antes_igual)

    depois_igual_sem_x=re.sub(r'x|[0-9]x|[+-] [0-9]x','',depois_igual)
    depois_igual_x=re.findall(r'x|[0-9]x|[+-] [0-9]x',depois_igual)
    i=0
    antes_igual_sem_x=antes_igual_sem_x.split()#o sinal vai ficar separado
    for i in range(0,len(depois_igual_x)):
        if '+' in depois_igual_x[i] or '-' in depois_igual_x[i]:
            sinal=re.sub('[\w\s]','',depois_igual_x[i])
            depois_igual_x[i]=depois_igual_x[i].replace(sinal,sinais[sinal])
    for i in range(0,len(antes_igual_sem_x)):
        if '+' in antes_igual_sem_x[i] or '-' in antes_igual_sem_x[i]:
            sinal=re.sub('[\w\s]','',antes_igual_sem_x[i])
            antes_igual_sem_x[i]=antes_igual_sem_x[i].replace(sinal,sinais[sinal])

    antes_igual_x =' ' + ' '.join(antes_igual_x+depois_igual_x)#precisa do primeiro espaço pra hora da resoluçao
    depois_igual_sem_x+=' ' + ' '.join(antes_igual_sem_x)

    print(antes_igual_x,' = ',depois_igual_sem_x)
    depois_igual=resolucao(depois_igual_sem_x,'eq')

    if antes_igual_x==' x':
        print(antes_igual_x,'=',depois_igual)
    else:
        antes_igual=str(resolucao(antes_igual_x.replace(' -x ',' -1 ').replace(' x ',' 1 ').replace('x',''),'eq'))+'x'
        if antes_igual=='1.0x':
            print(antes_igual.replace('1.0x','x'),'=',depois_igual)
        else:
            y=antes_igual.replace('x','')
            depois_igual=float(depois_igual)/float(y)
            print(antes_igual.replace(y,''),'=',depois_igual)

def equacao2(a,b,c):
    eq2_item=[a,b,c]
    print(eq2_item)
    for i in range(0,3):#tira o x das variaveis
        eq2_item[i]=re.sub(r'x|\^2|\+|=','',eq2_item[i])
        if eq2_item[i]=='' or eq2_item[i]=='-':
            eq2_item[i]=eq2_item[i] + '1'
    eq2_num=[float(item) for item in eq2_item]
    if 'x' in b:
        if c=='=0':#tipo ax^2 + bx = 0
            x=(eq2_num[1]*-1)/eq2_num[0]
            print('x1=0')
            print('x2=',x)
        else:#tipo completa ax^2 + b + c = 0  
            delta=eq2_num[1]**2-4*eq2_num[0]*eq2_num[2]
            print('Delta=',delta)
            if delta>=0:
                x=lambda a, b, c: calculos[c](-b,math.sqrt(delta))/(2*a)
                print('x1=',x(eq2_num[0],eq2_num[1],'+'))
                print('x2=',x(eq2_num[0],eq2_num[1],'-'))
            else:
                print('raiz negativa, não existe nos numeros Reais')
    else:#tipo ax^2 + c = 0
        x=(eq2_num[1]*-1)/eq2_num[0]
        if x>=0:
            x=math.sqrt(x)
            print('x1=',x)
            print('x2=',x*-1)
        else:
            print('raiz negativa, não existe nos numeros Reais')

def prioridade(list, op):
    x=0
    resultado=0
    global aux2
    global aux
    while x!=len(list):
        if list[x]==op:
            resultado=calculos[op](aux2[x*2],aux2[x*2+2])
            del(aux2[x*2:x*2+3])
            del(aux[x])
            aux2.insert(x*2, resultado)
            x=-1
        x+=1
    return resultado

calculos={
    '+':soma,
    '-':subtracao,
    '/':divisao,
    '*':multiplicao,
    '^':expoente,
    'eq1':equacao1,
    'eq2':equacao2
}

final=0.0
i=1

def resolucao(expressao,v):
    c=0
    global i
    global aux2
    global aux
    try:
        if '(' in expressao and ')' in expressao:
            aux3=re.findall(r'\([-+*/\^0-9\s]{0,}\)', expressao)
            a=0
            b=0.0
            while a!=len(aux3):
                b=resolucao(' '.join(re.sub(r'[( )]','',aux3[a])),'eq')
                expressao=expressao.replace(aux3[a],str(b))
                a+=1
        aux2=expressao.split()
        aux=list(re.sub('[0-9.]|[-+]+[0-9.]|\s','',expressao))#transforma números e espaços em nada
        if aux2[0]=='p':#interrope processo
            i=0
        elif aux2[0]=='a':
            ajuda()
        else:
            if 'eq1' in aux2:
                calculos['eq1'](aux2)
            elif 'eq2' in aux2:
                calculos['eq2'](aux2[1], aux2[2]+aux2[3], aux2[4]+aux2[5])
            else:
                if len(aux)>0:#verifica se existe ao menos 1 operação
                    if aux2[0] in ['+','-']:
                        aux2[1]=aux2[0]+aux2[1]
                        aux.pop(0)
                        aux2.pop(0)
                    if '^' in aux:
                        final=prioridade(aux,'^')
                    if '*' in aux:
                        final=prioridade(aux,'*')
                    if '/' in aux:
                        final=prioridade(aux,'/')
                    while c!=len(aux):
                        calculo=calculos[aux[0+c]]
                        final=calculo(aux2[0],aux2[2])
                        del(aux2[0:2])
                        aux2[0]=final
                        c+=1
                else:
                    final=aux2[0]
                if v=='eq':
                    return final
                else:
                    print('resultado final:',final)
    except:
        print('Erro!! Verifique a expressão:',conta)
            
def ajuda():
        print(
        '\nRegras da calculadora:\n',
        'Separe as operaçôes com espaço; se for um numero negativo, o sinal fica junto ao numero\n',
        'ex: 4 + 5 * -2; 8 + -2 / 6; 2 ^ 2\n',
        '\nOperaçôes:\n',
        'p = pausar/sair; a = ajuda\n',
        '+ = soma; - = subtração; * = multiplicação; / = divisão; ^ = expoente\n',
        'Ex: 2 + 2 | 2 - 2 | 2 * -2 | -2 / 2 | 2 ^ 2\n',
        'eq1 no inicio = equação de primeiro grau(ex: eq1 9x - 4x + 10 = 7x - 30)\n',
        'eq2 no inicio = equação de segundo grau(ex: eq2 x^2 - x - 12 = 0 | eq2 3x^2 - 27 = 0 | eq2 5x^2 - 45x = 0)\n'
    )

ajuda()

while i==1:
    conta=input('Expresse a conta:')
    resolucao(conta,'')