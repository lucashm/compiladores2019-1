import sys

file = open(sys.argv[1], "r")
read = file.readlines()
commands = []  # Comandos de entrada
stack = []  # pilha -> M
s = 0  # Ponteiro da pilha M / stack
i = 0  # Ponteiro dos comandos de entrada / commands

registers = []  # vetor de registradores -> D

labels = {}

# Lê as linhas e guarda em -> commands
for line in read:
    commands.append(line.lstrip().replace(",", "").rstrip().split(" "))
# print(commands)

# Função de auxílio
def index_exists(ls, i):
    return (0 <= i < len(ls)) or (-len(ls) <= i < 0)


# Função de auxílio
def appendValue(value):
    global s
    if index_exists(stack, s):
        stack[s] = value
    else:
        stack.append(value)


# Função de auxílio
def appendRegisters(value, idx):
    global registers
    if index_exists(registers, int(idx)):
        registers[int(idx)] = value
    else:
        registers.append(value)


# Começa aqui
def startMEPA():
    global commands
    global stack
    global s
    global i

    global labels

    # Define as labels antes de iniciar o código
    for idx, command in enumerate(commands):
        if ":" in command[0]:
            label = command[0].strip(":")
            labels[label] = idx - 1
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
        if commands[i][0] == "INPP":  # Inicia
            s = -1
            registers.append(0)
        elif commands[i][0] == "CRCT":  # Carrega constante
            s += 1
            appendValue(commands[i][1])
        elif commands[i][0] == "LEIT":  # Lê valor de input
            s += 1
            appendValue(int(input()))
        elif commands[i][0] == "SOMA":  # Soma 2 últimos valores de stack / M
            stack[s - 1] = int(stack[s - 1]) + int(stack[s])
            s -= 1
        elif commands[i][0] == "MULT":  # Multiplica 2 últimos valores de stack / M
            stack[s - 1] = int(stack[s - 1]) * int(stack[s])
            s -= 1
        elif commands[i][0] == "SUBT":  # Subtrai 2 últimos valores de stack / M
            stack[s - 1] = int(stack[s - 1]) - int(stack[s])
            s -= 1
        elif commands[i][0] == "DIVI":  # Divide 2 últimos valores de stack / M
            stack[s - 1] = int(stack[s - 1]) / int(stack[s])
            s -= 1
        elif commands[i][0] == "INVR":  # Inverte o último valor de stack / M
            stack[s] = -stack[s]
        elif commands[i][0] == "NEGA":  # Nega o último valor de stack / M
            stack[s] = 1 - stack[s]
        elif commands[i][0] == "CONJ":
            if stack[s - 1] == 1 and int(stack[s]) == 1:
                stack[s - 1] = 1
            else:
                stack[s - 1] = 0
            s -= 1
        elif commands[i][0] == "DISJ":
            if stack[s - 1] == 1 or int(stack[s]) == 1:
                stack[s - 1] = 1
            else:
                stack[s - 1] = 0
            s -= 1
        elif commands[i][0] == "CMME":
            if stack[s - 1] < int(stack[s]):
                stack[s - 1] = 1
            else:
                stack[s - 1] = 0
            s -= 1
        elif commands[i][0] == "CMMA":
            if stack[s - 1] > int(stack[s]):
                stack[s - 1] = 1
            else:
                stack[s - 1] = 0
            s -= 1
        elif commands[i][0] == "CMIG":
            if stack[s - 1] == int(stack[s]):
                stack[s - 1] = 1
            else:
                stack[s - 1] = 0
            s -= 1
        elif commands[i][0] == "CMDG":
            if stack[s - 1] != int(stack[s]):
                stack[s - 1] = 1
            else:
                stack[s - 1] = 0
            s -= 1
        elif commands[i][0] == "CMEG":
            if int(stack[s - 1]) <= int(stack[s]):
                stack[s - 1] = 1
            else:
                stack[s - 1] = 0
            s -= 1
        elif commands[i][0] == "CMAG":
            if int(stack[s - 1]) >= int(stack[s]):
                stack[s - 1] = 1
            else:
                stack[s - 1] = 0
            s -= 1
        elif commands[i][0] == "AMEM":  # Sobe o ponteiro de stack / M
            s += int(commands[i][1])
            for x in range(0, int(commands[i][1])):
                appendValue(None)
        elif commands[i][0] == "DMEM":  # Desce o ponteiro de stack / M
            s -= int(commands[i][1])
            if s < 0:
                print("Linha {}: RunTime error. Stack underflow".format(idx))
                return
        elif commands[i][0] == "CRVL":  # Carrega valor
            s += 1
            appendValue(stack[registers[int(commands[i][1])] + int(commands[i][2])])
        elif commands[i][0] == "ARMZ":  # Armazena valor
            stack[registers[int(commands[i][1])] + int(commands[i][2])] = stack[s]
            s -= 1
        elif commands[i][0] == "DSVF":  # Desvia se falso
            if commands[i][1] in labels:
                if stack[s] == 0:
                    i = labels[commands[i][1]]
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
            else:
                print(
                    "Linha {}: RunTime error rotulo {} invalido".format(
                        idx - 2, commands[i][1]
                    )
                )
                return
        elif commands[i][0] == "ARMI":
            stack[stack[registers[commands[i][1]] + commands[i][2]]] = stack[s]
            s -= 1
        elif commands[i][0] == "CHPR":
            s+=1
            appendValue(idx + 1)
            s += 1
            appendValue(commands[i][2])
            i = labels[commands[i][1]]
        elif commands[i][0] == "CREN":
            s += 1
            stack[s] = registers[commands[i][1]] + commands[i][2]
        elif commands[i][0] == "ENRT":
            s = registers[commands[i][1]] + commands[i][2] - 1
        elif commands[i][0] == "ENPR":
            s += 1
            if(int(commands[i][1])+1 > len(registers)):
              appendValue(0)
            else:
              appendValue(registers[int(commands[i][1])])
            appendRegisters(s + 1, int(commands[i][1]))
            print("----------------")
        elif commands[i][0] == "RTPR":
            appendRegisters(stack[s], commands[i][1])
            s = s - int(commands[i][2]) + 3
            i = int(stack[s - 2])
        elif commands[i][0] == "IMPR":  # Imprime o valor no ponteiro de stack / M
            print(stack[s])
            s -= 1
        elif commands[i][0] == "PARA":  # Encerra
            return
        elif commands[i][0] == "NADA":  # Faz nada
            pass

        i += 1

        print("======================")
        print(commands[i])
        print(s)
        print(stack)
        print("======================")


startMEPA()
