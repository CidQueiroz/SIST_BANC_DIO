import textwrap

def menu():
	menu = """\n
	########### MENU ###########
	[D]\tDepositar
	[S]\tSacar
	[E]\tExtrato
	[NC]\tNova conta
	[LC]\tListar contatos
	[NU]\tNovo usuario
	[Q]\tSair
	=>"""

	return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato):
	if valor > 0:
		saldo += valor
		extrato += f"Deposito:\tR$ {valor:.2f}\n"
		print("\n=== Depósito realizado com sucesso! ===")
	else:
		print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
	
	return saldo, extrato

def exibir_extrato(saldo, extrato):
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")

def criar_usuario(usuarios):
	cpf = input("Informe o CPF (somente numero): ")
	usuario = filtrar_usuario(cpf, usuarios)
	
	if usuario:
		print("\n@@@ Já existe usuário com esse CPF! @@@")
		return
	
	nome = input("Informe o nome completo: ")
	data_nasc = input("Informe a data de nascimento (dd-mm-aaaa): ")
	endereco = input("Informe o endereço (logradouro, numero - Bairro - Cidade/sigla Estado): ")

	usuarios.append({"nome": nome, "data_nascimento": data_nasc, "cpf": cpf, "endereco": endereco})

	print("=== Usuario criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
	usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
	return usuarios_filtrados[0] if usuarios_filtrados else None

def sacar(saldo, valor, extrato, limite, numero_saques, limite_saques):
	excedeu_saldo = valor > saldo
	excedeu_limite = valor > limite
	excedeu_saque = numero_saques > limite_saques

	if excedeu_saldo:
		print(f"\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

	elif excedeu_limite:
		print(f"\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
	
	elif excedeu_saque:
		print(f"\n@@@ Operação falhou! Número máximo de saque excedido. @@@")
	
	if valor > 0:
		saldo -= valor
		extrato += f"\nSaque\t\tR$ {valor:.2f}\n"
		numero_saques += 1
		print("\n=== Saque realizado com sucesso! ===")

	else:
		print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

	return saldo, extrato, numero_saques

def criar_conta(AGENCIA, numero_conta, usuarios):
	cpf = input("Informe o CPF do usuario: ")
	usuario = filtrar_usuario(cpf, usuarios)

	if usuario:
		print("\n=== Conta criada com sucesso! ===")
		return {"agencia": AGENCIA, "numero_conta": numero_conta, "usuario": usuario}
	
	print("\n @@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
	return None

def listar_contas(contas):
	#BRASIL
	if not contas:
		print("\n@@@ Não existem contas cadastradas! @@@")
		return
	
	for conta in contas:
		linha = f"""\
		Agência:\t{conta["agencia"]}
		C/C:\t\t{conta["numero_conta"]}
		Titular:\t{conta["usuarios"]["nome"]}
		"""
	
	print("*" * 100)
	print(textwrap.dedent(linha))

def main():

	AGENCIA = "0001"
	LIMITE_SAQUES = 3
	saldo = 0
	limite = 500
	extrato = ""
	numero_saques = 0
	usuarios = []
	contas = []

	while True:

		opcao = menu()
	
		if opcao == "d":
			valor = float(input("Informe o valor do depósito: "))
			saldo, extrato = depositar(saldo, valor, extrato)
	
		elif opcao == "s":
			valor = float(input("Informe o valor do saque: "))
		
			saldo, extrato, numero_saques = sacar(
				saldo=saldo,
				valor=valor,
				extrato=extrato,
				limite=limite,
				numero_saques=numero_saques,
				limite_saques=LIMITE_SAQUES)
	
		elif opcao == "e":
			exibir_extrato(saldo, extrato=extrato)
	
		elif opcao == "nu":
			criar_usuario(usuarios)
		
		elif opcao == "nc":
			numero_conta = len(contas) + 1
			conta = criar_conta(AGENCIA, numero_conta, usuarios)
			
			if conta:
				contas.append(conta)

		elif opcao == "lc":
			listar_contas(contas)

		elif opcao == "q":
			break
		else:
			print("Operação inválida, por favor selecione novamente a operação desejada.")
	

main()