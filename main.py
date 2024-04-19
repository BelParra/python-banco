red = "\033[1;31m"
green = "\033[1;32m"
negrito = "\033[1m"
blue = "\033[1;34m"
clear = "\033[m"


def deposito(contas, cpf, valor):
    conta_selecionada = selecionar_conta(contas, cpf)
    if conta_selecionada is None:
        print("Conta não encontrada.")
        return

    while valor < 0:
        valor = float(
            input(
                """{}\nValor inválido{}. Tente novamente.
R$""".format(
                    red, clear
                )
            )
        )

    saldo_atual = conta_selecionada["saldo"]
    saldo_atual += valor
    conta_selecionada["saldo"] = saldo_atual
    conta_selecionada["transacoes"].append(("Depósito", valor))
    print("{}\nDepósito realizado.\n{}".format(green, clear))
    return saldo_atual


def saque(contas, cpf, valor):
    conta_selecionada = selecionar_conta(contas, cpf)
    if conta_selecionada is None:
        print("Conta não encontrada.")
        return

    if valor > 500:
        print(
            """\n{}O valor do saque excede o limite de R$500.{}
""".format(
                red, clear
            )
        )
        return

    numero_saques = sum(
        1 for transacao in conta_selecionada["transacoes"] if transacao[0] == "Saque"
    )

    if numero_saques >= conta_selecionada["limite_saques"]:
        print(
            """{}\nVocê atingiu o limite de saque para hoje.{}
""".format(
                red, clear
            )
        )
        return conta_selecionada["saldo"]

    saldo_atual = conta_selecionada["saldo"]
    if valor > saldo_atual:
        print("{}\nSaque não foi realizado. Saldo insuficiente.\n{}".format(red, clear))
        return saldo_atual

    while valor < 0:
        valor = float(
            input(
                """{}\nValor inválido{}. Tente novamente.
 R$ """.format(
                    red, clear
                )
            )
        )

    saldo_atual -= valor
    conta_selecionada["saldo"] = saldo_atual
    conta_selecionada["transacoes"].append(("Saque", valor))
    print("{}\nSaque realizado com sucesso.\n{}".format(green, clear))
    return saldo_atual


def extrato(contas, cpf):
    print("\n{}----{} Extrato {}----{}".format(blue, clear, blue, clear))
    for conta in contas:
        if conta["usuario"]["cpf"] == cpf:
            print(f"{'\n'}{negrito}{conta['tipo_conta']}{clear}:")
            for transacao in conta["transacoes"]:
                print(f"{transacao[0]}: R${transacao[1]}")
            print(f"{negrito}{'\n'}Saldo atual: R${conta['saldo']}{'\n'}{clear}")


def criar_usuario(usuarios):
    cpf = input(
        """\nDigite seu CPF {}(apenas números){}:
""".format(
            negrito, clear
        )
    )
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            print("Usuário já cadastrado.")
            return None
    nome = input("\nDigite seu nome:\n")
    apelido = input("\nComo gostaria de ser chamado(a)?\n")
    data_nascimento = input(
        """\nDigite sua data de nascimento ({}DD/MM/AAAA{}):
""".format(
            negrito, clear
        )
    )
    endereco = input(
        """\nDigite seu endereço ({}Logradouro, número - bairro, cidade/estado{}):
""".format(
            negrito, clear
        )
    )
    usuarios.append(
        {
            "nome": nome,
            "apelido": apelido,
            "cpf": cpf,
            "data_nascimento": data_nascimento,
            "endereco": endereco,
        }
    )
    print("\nOlá {}{}{}!\n".format(blue, apelido, clear))
    return cpf


def criar_conta(usuarios, contas, cpf):
    tipos_contas_existente = {
        conta["tipo_conta"] for conta in contas if conta["usuario"]["cpf"] == cpf
    }
    if len(tipos_contas_existente) == 3:
        print("Não é possível criar uma nova conta. Você já possui uma de cada tipo.")
        return None

    tipo_conta = int(
        input(
            """\nEscolha o tipo de conta:\n
[ 1 ] {}Conta Corrente{}
[ 2 ] {}Conta Salário{}
[ 3 ] {}Conta de Investimentos{}\n
Sua opção: """.format(
                negrito, clear, negrito, clear, negrito, clear
            )
        )
    )

    opcao_para_tipo = {
        1: "Conta Corrente",
        2: "Conta Salário",
        3: "Conta de Investimentos",
    }

    if any(
        conta["tipo_conta"] == opcao_para_tipo[tipo_conta]
        for conta in contas
        if conta["usuario"]["cpf"] == cpf
    ):
        print(
            "\n{}Você já tem uma {}{}.\n".format(
                red, opcao_para_tipo[tipo_conta], clear
            )
        )

        return None

    numero_conta = len(contas) + 1
    usuario_encontrado = None
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            usuario_encontrado = usuario
            break
    if usuario_encontrado is None:
        print("Usuário não encontrado.")
        return None

    agencia = "0001"
    if tipo_conta == 1:
        contas.append(
            {
                "agencia": agencia,
                "numero_conta": numero_conta,
                "tipo_conta": "Conta Corrente",
                "usuario": usuario_encontrado,
                "saldo": 0,
                "limite_saques": 3,
                "transacoes": [],
            }
        )
    elif tipo_conta == 2:
        contas.append(
            {
                "agencia": agencia,
                "numero_conta": numero_conta,
                "tipo_conta": "Conta Salário",
                "usuario": usuario_encontrado,
                "saldo": 0,
                "limite_saques": 3,
                "transacoes": [],
            }
        )
    elif tipo_conta == 3:
        contas.append(
            {
                "agencia": agencia,
                "numero_conta": numero_conta,
                "tipo_conta": "Conta de Investimentos",
                "usuario": usuario_encontrado,
                "saldo": 0,
                "limite_saques": 3,
                "transacoes": [],
            }
        )
    else:
        print("Opção inválida.")
        return None

    print("Conta criada com sucesso.\n")
    return numero_conta


def selecionar_conta(contas, cpf):
    contas_usuario = [conta for conta in contas if conta["usuario"]["cpf"] == cpf]
    if len(contas_usuario) == 1:
        return contas_usuario[0]

    print("\nEscolha a conta:\n")
    for i, conta in enumerate(contas_usuario, 1):
        print(f"[ {i} ] {negrito}{conta['tipo_conta']}{clear}")
    opcao = int(input("\nSua opção: "))
    return contas_usuario[opcao - 1]


saldo = 0
limite = 500
LIMITE_SAQUES = 3
numero_saques = 0
transacoes_saque = []
transacoes_deposito = []
usuarios = []
contas = []

cpf = input("{}Digite seu CPF ou 0 para sair:{}\n".format(blue, clear))
if cpf == "0":
    exit()

usuario_existente = False
for usuario in usuarios:
    if usuario["cpf"] == cpf:
        usuario_existente = True
        break

if not usuario_existente:
    opcao = int(
        input(
            """\n{}CPF não cadastrado{}. Deseja cadastrar um usuário?\n
[ 0 ] {}Não{}
[ 1 ] {}Sim{}\n
Sua opção: """.format(
                red, clear, negrito, clear, negrito, clear
            )
        )
    )
    if opcao == 1:
        cpf = criar_usuario(usuarios)
        if cpf is None:
            exit()
    else:
        exit()

criar_conta(usuarios, contas, cpf)

menu = """Deseja algo mais?\n
[ 0 ] {}Sair{}
[ 1 ] {}Depositar{}
[ 2 ] {}Sacar{}
[ 3 ] {}Extrato{}
[ 4 ] {}Criar Conta\n{}
Sua opção: """.format(
    negrito, clear, negrito, clear, negrito, clear, negrito, clear, negrito, clear
)

while True:
    opcao = int(input(menu))
    if opcao == 0:
        break
    elif opcao == 1:
        valor_deposito = float(input("\nQual valor deseja depositar?\nR$"))
        conta_selecionada = contas[0]
        saldo = deposito(contas, cpf, valor_deposito)

    elif opcao == 2:
        valor_saque = float(input("\nQual valor deseja sacar?\nR$"))
        conta_selecionada = contas[0]
        saldo = saque(contas, cpf, valor_saque)

    elif opcao == 3:
        extrato(contas, cpf)
    elif opcao == 4:
        criar_conta(usuarios, contas, cpf)
    else:
        print("{}\nOpção inválida\n{}".format(red, clear))
