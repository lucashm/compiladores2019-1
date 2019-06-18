import sys

file = open(sys.argv[1], "r")
read = file.readlines()
commands = []  # Comandos de entrada
stack = []  # pilha -> M
s = 0  # Ponteiro da pilha M / stack
i = 0  # Ponteiro dos comandos de entrada / commands

registers = []  # vetor de registradores -> D

labels = {}


for line in read:
    commands.append(line.lstrip().replace(",", "").rstrip().split(" "))
# print(commands)


def index_exists(ls, i):
    return (0 <= i < len(ls)) or (-len(ls) <= i < 0)


def appendValue(value):
    global s
    if index_exists(stack, s):
        stack[s] = value
    else:
        stack.append(value)


def startMEPA():
    global commands
    global stack
    global s
    global i

    global labels

    # Defining labels
    for idx, command in enumerate(commands):
        if ":" in command[0]:  # Cria labels
            label = command[0].strip(":")
            labels[label] = idx

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
            if stack[s - 1] == 1 and stack[s] == 1:
                stack[s - 1] = 1
            else:
                stack[s - 1] = 0
            s -= 1
        elif commands[i][0] == "DISJ":
            if stack[s - 1] == 1 or stack[s] == 1:
                stack[s - 1] = 1
            else:
                stack[s - 1] = 0
            s -= 1
        elif commands[i][0] == "CMME":
            if stack[s - 1] < stack[s]:
                stack[s - 1] = 1
            else:
                stack[s - 1] = 0
            s -= 1
        elif commands[i][0] == "CMMA":
            if stack[s - 1] > stack[s]:
                stack[s - 1] = 1
            else:
                stack[s - 1] = 0
            s -= 1
        elif commands[i][0] == "CMIG":
            if stack[s - 1] == stack[s]:
                stack[s - 1] = 1
            else:
                stack[s - 1] = 0
            s -= 1
        elif commands[i][0] == "CMDG":
            if stack[s - 1] != stack[s]:
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
            s -= s
        elif commands[i][0] == "DSVF":  # Desvia se falso
            if stack[s] == 0:
                if commands[i][1] in labels:
                  i = labels[commands[i][1]]
                else:
                  print("Linha {}: RunTime error. rotulo {} invalido".format(idx, commands[i][1]))
                  return
        elif commands[i][0] == "DSVS":
            if commands[i][1] in labels:
              i = labels[commands[i][1]]
            else:
              print("Linha {}: RunTime error. rotulo {} invalido".format(idx, commands[i][1]))
              return
        elif commands[i][0] == "IMPR":  # Imprime o valor no ponteiro de stack / M
            print(stack[s])
            s -= 1
        elif commands[i][0] == "PARA":  # Encerra
            return

        i += 1


startMEPA()
