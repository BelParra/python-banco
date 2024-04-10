red = '\033[1;31m'
green = '\033[1;32m'
clear = '\033[m'

menu = '''Deseja algo mais?\n
[ 0 ] Sair
[ 1 ] Depositar
[ 2 ] Sacar
[ 3 ] Extrato\n
Sua opção: '''

saldo = 0
limite = 500
LIMITE_SAQUES = 3
numero_saques = 0
transacoes_saque = []
transacoes_deposito = []

opcao = -1

while True:
    opcao = int(input('''Olá esse é o seu primeiro acesso.\n
Deseja fazer um depósito?\n
[ 0 ] Sair
[ 1 ] Sim\n
Sua opção: '''))
    if opcao == 0:
        break
    elif opcao == 1:
        deposito = float(input('\nQual valor do depósito?\nR$'))

        while deposito < 0:
            deposito = float(
                input('''{}\nDigite um valor positivo{}.
R$'''.format(red, clear)))

        if deposito > 0:
            saldo += deposito
            transacoes_deposito.append(('Depósito', deposito))
            print('{}\nDepósito realizado.\n{}'.format(green, clear))
            break
    else:
        print('{}\nOpção inválida.\n{}'.format(red, clear))

while opcao != 0:
    opcao = int(input(menu))

    if opcao == 1:
        deposito = float(input('\nQual valor deseja depositar?\nR$'))

        while deposito < 0:
            deposito = float(input('''{}\nValor inválido{}. Tente novamente.
R$ '''.format(red, clear)))

        transacoes_deposito.append(('Depósito', deposito))
        saldo += deposito

        print('{}\nDepósito realizado.\n{}'.format(green, clear))

    elif opcao == 2:
        if numero_saques >= LIMITE_SAQUES:
            print('{}\nVocê atingiu o limite de saque para hoje.\n{}'.format(
                red, clear))
            continue

        saque = float(input('''\nQual valor deseja sacar?
R$'''))

        while saque > saldo:
            saque = float(input('''\nVocê tem {}R${}{} em sua conta.\n
{}Saque não foi realizado{}, Tente novamente.
R$'''.format(red, saldo, clear, red, clear)))

        while saque < 0:
            saque = float(input('''{}\nValor inválido{}. Tente novamente.
R$ '''.format(red, clear)))

        while saque > limite:
            saque = float(input('''{}\nLimite de R$500{}. Tente novamente.\n
R$ '''.format(red, clear)))

        transacoes_saque.append(('Saques', saque))
        saldo -= saque
        numero_saques += 1

        print('{}\nSaque realizado com sucesso\n{}'.format(green, clear))

    elif opcao == 3:
        print('---- Extrato ----')
        print('Depósitos:')
        for transacao in transacoes_deposito:
            print('{}: R${}'.format(transacao[0], transacao[1]))
        print('Saques:')
        for transacao in transacoes_saque:
            print('{}: R${}'.format(transacao[0], transacao[1]))
        print('\nSeu saldo é de {}R${}{}\n'.format(green, saldo, clear))

    elif opcao != 0 and 1 and 2 and 3:
        print('{}\nOpção inválida\n{}'.format(red, clear))
