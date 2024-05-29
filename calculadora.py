import math
import re

def soma(n1,n2): 
    return float(n1)+float(n2) 

def subtracao(n1,n2):
    return float(n1)-float(n2)  

def divisao(n1,n2):
    return float(n1)/float(n2)   

def multiplicao(n1,n2):
    return float(n1)*float(n2) 

def expoente(n1,n2):
    return float(n1)**float(n2)  

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

def equacao2(exp):
    a=exp[1]
    b= exp[2]+exp[3]
    c=exp[4]+exp[5]
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

calculos={
    '+':soma,
    '-':subtracao,
    '/':divisao,
    '*':multiplicao,
    '^':expoente,
    'eq1':equacao1,
    'eq2':equacao2
}
prioridades=[['^'],['*','/'],['+','-']]#lista de operaçoes prioridades
final=0.0
continuar=True

def resolucao(expressao,v):
    global continuar
    x=0#contador das prioridades
    aux2=[]# auxiliar para a expressão
    aux=[]# auxiliar para os sinais
    try:
        if '(' in expressao and ')' in expressao:
            aux3=re.findall(r'\([-+*/\^0-9\s]{0,}\)', expressao)#pega a operação entre parenteses
            cont=0
            while cont!=len(aux3):
                expressao=expressao.replace(aux3[cont],str(resolucao(' '.join(re.sub(r'[( )]','',aux3[cont])),'eq')))
                cont+=1
        aux2=expressao.split()
        aux=list(re.sub('[0-9.]|[-+]+[0-9.]|\s','',expressao))#transforma números e espaços em nada, deixando apenas os sinais
        if aux2[0]=='p':#interrope processo
            continuar=False
        elif aux2[0]=='a':
            ajuda()
        else:
            if aux2[0].startswith('eq'):#caso a expressão seja uma equação
                calculos[aux2[0]](aux2)
            else:
                if aux2[0] in ['+','-']:
                    aux2[1]=aux2[0]+aux2[1]
                    aux.pop(0)
                    aux2.pop(0)
                for op in prioridades:#vai rodando pelo loop, calculando primeiro os sinais de maior prioridade
                    while x!=len(aux):
                        if aux[x] in op:
                            resultado=calculos[aux[x]](aux2[x*2],aux2[x*2+2])
                            del(aux2[x*2:x*2+3])#exclui a operação correspondente
                            del(aux[x])#exclui o sinal correspondente
                            aux2.insert(x*2, resultado)
                            x=-1
                        x+=1
                    x=0
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
        '+ = soma;\t - = subtração;\t * = multiplicação;\t / = divisão;\t ^ = expoente\n',
        'Ex: 2 + 2 \t 2 - 2 \t\t 2 * -2 \t\t -2 / 2 \t 2 ^ 2\n',
        'eq1 no inicio = equação de primeiro grau(ex: eq1 9x - 4x + 10 = 7x - 30)\n',
        'eq2 no inicio = equação de segundo grau(ex: eq2 x^2 - x - 12 = 0 | eq2 3x^2 - 27 = 0 | eq2 5x^2 - 45x = 0)\n'
    )

ajuda()

while continuar:
    conta=input('Expresse a conta:')
    resolucao(conta,'')