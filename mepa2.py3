import sys

file = open(sys.argv[1], "r")
read = file.readlines()
commands = []  # Comandos de entrada
M = [0] * 256000  # pilha -> M
s = 0  # Ponteiro da pilha M / stack
i = 0  # Ponteiro dos comandos de entrada / commands

D = [0] * 256000  # vetor de registradores -> D

labels = {}

# Lê as linhas e guarda em -> commands
for line in read:
    commands.append(line.lstrip().replace(",", "").rstrip().split(" "))
# print(commands)

# Função de auxílio


def index_exists(ls, i):
    return (0 <= i < len(ls)) or (-len(ls) <= i < 0)


# Começa aqui
def startMEPA():
    global commands
    global M
    global s
    global i

    global labels

    # Define as labels antes de iniciar o código
    for idx, command in enumerate(commands):
        if ":" in command[0]:
            label = command[0].strip(":")
            labels[label] = idx
            commands[idx] = commands[idx][1:]
            # print(commands[idx])
    # A estrutura de commands é uma lista
    # Cada elemento dessa lista também é uma lista de 1 a 3 valores
    # No caso de INPP, por exemplo, temos ['INPP'] -> Apenas um elemento
    # Para CRCT, temos ['CRCT', 2], então, para acessar, temos:
    # commands[i][0] -> 'CRCT' // Nome do comando
    # commands[i][1] -> 2 // Primeiro argumento
    #
    # E o mesmo se repete para 3 valores, exemplo: ['CRVL', 0, 1]
    # commands[i][0] -> 'CRVL'
    # commands[i][1] -> 0
    # commands[i][2] -> 1

    # LINK DA DESCRIÇÃO MEPA:
    # http://www.ic.unicamp.br/~tomasz/ilp/ilp.pdf
    # página 181

    while commands[i][0] != "PARA":
        # print(">>> Line ", i+1, "=", commands[i], "s =", s, "stack =", M[0:s + 1])

        if commands[i][0] == "INPP":  # Inicia
            s = -1
        elif commands[i][0] == "CRCT":  # Carrega constante
            s += 1
            M[s] = commands[i][1]
            # appendValue(commands[i][1])
        elif commands[i][0] == "LEIT":  # Lê valor de input
            s += 1
            M[s] = int(input())
            # appendValue(int(input()))
        elif commands[i][0] == "SOMA":  # Soma 2 últimos valores de stack / M
            M[s - 1] = int(M[s - 1]) + int(M[s])
            s -= 1
        elif commands[i][0] == "MULT":  # Multiplica 2 últimos valores de stack / M
            M[s - 1] = int(M[s - 1]) * int(M[s])
            s -= 1
        elif commands[i][0] == "SUBT":  # Subtrai 2 últimos valores de stack / M
            M[s - 1] = int(M[s - 1]) - int(M[s])
            s -= 1
        elif commands[i][0] == "DIVI":  # Divide 2 últimos valores de stack / M
            M[s - 1] = int(M[s - 1]) // int(M[s])
            s -= 1
        elif commands[i][0] == "INVR":  # Inverte o último valor de stack / M
            M[s] = -M[s]
        elif commands[i][0] == "NEGA":  # Nega o último valor de stack / M
            M[s] = 1 - M[s]
        elif commands[i][0] == "CONJ":
            if M[s - 1] == 1 and int(M[s]) == 1:
                M[s - 1] = 1
            else:
                M[s - 1] = 0
            s -= 1
        elif commands[i][0] == "DISJ":
            if M[s - 1] == 1 or int(M[s]) == 1:
                M[s - 1] = 1
            else:
                M[s - 1] = 0
            s -= 1
        elif commands[i][0] == "CMME":
            if M[s - 1] < int(M[s]):
                M[s - 1] = 1
            else:
                M[s - 1] = 0
            s -= 1
        elif commands[i][0] == "CMMA":
            if M[s - 1] > int(M[s]):
                M[s - 1] = 1
            else:
                M[s - 1] = 0
            s -= 1
        elif commands[i][0] == "CMIG":
            if M[s - 1] == int(M[s]):
                M[s - 1] = 1
            else:
                M[s - 1] = 0
            s -= 1
        elif commands[i][0] == "CMDG":
            if M[s - 1] != int(M[s]):
                M[s - 1] = 1
            else:
                M[s - 1] = 0
            s -= 1
        elif commands[i][0] == "CMEG":
            if int(M[s - 1]) <= int(M[s]):
                M[s - 1] = 1
            else:
                M[s - 1] = 0
            s -= 1
        elif commands[i][0] == "CMAG":
            if int(M[s - 1]) >= int(M[s]):
                M[s - 1] = 1
            else:
                M[s - 1] = 0
            s -= 1
        elif commands[i][0] == "AMEM":  # Sobe o ponteiro de stack / M
            s += int(commands[i][1])
        elif commands[i][0] == "DMEM":  # Desce o ponteiro de stack / M
            s -= int(commands[i][1])
            if s < -1:
                print("Linha {}: RunTime error. Stack underflow".format(idx))
                return
        elif commands[i][0] == "CRVL":  # Carrega valor
            s += 1
            M[s] = M[int(D[int(commands[i][1])]) + int(commands[i][2])]
        elif commands[i][0] == "ARMZ":  # Armazena valor
            M[int(D[int(commands[i][1])]) + int(commands[i][2])] = M[s]
            s -= 1
        elif commands[i][0] == "DSVF":  # Desvia se falso
            if commands[i][1] in labels:
                if M[s] == 0:
                    i = int(labels[commands[i][1]])
                else:
                    i = i+1
                s -= 1
                continue
            else:
                print(
                    "Linha {}: RunTime error rotulo {} invalido".format(
                        idx - 2, commands[i][1]
                    )
                )
                return
        elif commands[i][0] == "DSVS":
            if commands[i][1] in labels:
                i = labels[commands[i][1]]
                continue
            else:
                print(
                    "Linha {}: RunTime error rotulo {} invalido".format(
                        idx - 2, commands[i][1]
                    )
                )
                return
        elif commands[i][0] == "ARMI":
            M[M[D[commands[i][1]] + commands[i][2]]] = M[s]
            s -= 1
        elif commands[i][0] == "CHPR":
            M[s+1] = i + 1
            M[s+2] = commands[i][2]
            s += 2
            i = labels[commands[i][1]]
            continue
        elif commands[i][0] == "CREN":
            s += 1
            M[s] = D[commands[i][1]] + commands[i][2]
        elif commands[i][0] == "ENRT":
            s = D[commands[i][1]] + commands[i][2] - 1
        elif commands[i][0] == "ENPR":
            s += 1
            M[s] = D[int(commands[i][1])]
            D[int(commands[i][1])] = s + 1
        elif commands[i][0] == "RTPR":
            old_i = i
            D[int(commands[i][1])] = M[s]
            i = int(M[s - 2])
            s = s - (int(commands[old_i][2]) + 3)
            continue
        elif commands[i][0] == "IMPR":  # Imprime o valor no ponteiro de stack / M
            print(M[s])
            s -= 1
        elif commands[i][0] == "PARA":  # Encerra
            return
        elif commands[i][0] == "NADA":  # Faz nada
            pass

        if(commands[i][0] != 'PARA'):
            i += 1


startMEPA()
