from typing import List


class Produto:
    def __init__(self, produto_id, nome, ingredientes, preco, estoque):
        self.produto_id = produto_id
        self.nome = nome
        self.ingredientes = ingredientes
        self.preco = preco
        self.estoque = estoque

    def __str__(self):
        return f"{self.nome} - R${self.preco:.2f}"

    def exibir_detalhes(self):
        """Exibe todos os detalhes do produto"""
        print(f"\nID: {self.produto_id} | {self.nome} - R${self.preco:.2f}")
        print(f"   Ingredientes: {self.ingredientes}")
        print(f"   Estoque: {self.estoque} unidades")


class Cliente:
    def __init__(self, cliente_id, nome, email, telefone):
        self.cliente_id = cliente_id
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.pontos = 0

    def exibir_detalhes(self):
        """Exibe todos os detalhes do cliente"""
        print(f"\nCliente: {self.nome} (ID: {self.cliente_id})")
        print(f"   Email: {self.email} | Telefone: {self.telefone}")
        print(f"   Pontos acumulados: {self.pontos}")
        if self.historico_pedidos:
            print(f"   Total de pedidos: {len(self.historico_pedidos)}")
        else:
            print("   Nenhum pedido realizado")

    def adicionar_pontos(self, valor: int):
        """Adiciona pontos ao cliente baseado no valor da compra"""
        pontos_ganhos = int(valor)
        self.pontos += pontos_ganhos
        return pontos_ganhos


class Pedido:
    def __init__(self, pedido_id, cliente_id, itens, total):
        self.pedido_id = pedido_id
        self.cliente_id = cliente_id
        self.itens = itens  # Lista de tuplas (produto_id, quantidade)
        self.total = total


class SistemaCafeteria:
    def __init__(self):
        self.produtos: List[Produto] = []
        self.clientes: List[Cliente] = []
        self.pedidos: List[Pedido] = []
        self.id_pedido = 1
        self.id_cliente = 1
        self.inicializar_dados()

    def inicializar_dados(self):
        # Produtos iniciais
        self.produtos.append(Produto(1, "Café Expresso", "Café", 5.0, 10))
        self.id_pedido += 1
        self.produtos.append(Produto(2, "Cappuccino", "Café, leite, chocolate", 7.5, 15))
        self.id_pedido += 1

        # Cliente inicial
        self.clientes.append(Cliente(1, "Maria Souza", "maria@email.com", "11999999999"))
        self.id_cliente += 1

    def menu_principal(self):
        while True:
            print("\n--- Coffee Shop Tia Rosa ---")
            print("1. Registrar Cliente")
            print("2. Ver Cardápio")
            print("3. Fazer Pedido")
            print("4. Ver Pedidos")
            print("5. Ver Clientes")
            print("6. Sair")
            opcao = input("Escolha uma opção: ")
            if opcao == '1':
                self.registrar_cliente()
            elif opcao == '2':
                self.mostrar_cardapio()
            elif opcao == '3':
                self.fazer_pedido()
            elif opcao == '4':
                self.ver_pedidos()
            elif opcao == '5':
                self.ver_clientes()
            elif opcao == '6':
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida.")

    def registrar_cliente(self):
        """Registra um novo cliente no sistema"""
        print("\n" + "=" * 50)
        print("            REGISTRAR NOVO CLIENTE            ")
        print("=" * 50)

        nome = input("\nNome completo: ")
        while not nome:
            print("Nome não pode ser vazio.")
            nome = input("Nome completo: ")

        email = input("Email: ")
        while not email or "@" not in email:
            print("Email inválido.")
            email = input("Email: ")

        telefone = input("Telefone: ")
        while not telefone:
            print("Telefone não pode ser vazio.")
            telefone = input("Telefone: ")

        # Verificar se email já está cadastrado
        for cliente in self.clientes:
            if cliente.email == email:
                print("\nJá existe um cliente cadastrado com este email!")
                input("Pressione ENTER para continuar...")
                return

        novo_cliente = Cliente(self.id_cliente, nome, email, telefone)
        self.clientes.append(novo_cliente)
        self.id_cliente += 1
        print("Cliente Registrado!\n")
        novo_cliente.exibir_detalhes()

    def mostrar_cardapio(self):
        """Exibe o cardápio completo"""
        print("\n--- Cardápio ---")
        for produto in self.produtos:
            produto.exibir_detalhes()

    def fazer_pedido(self):
        try:
            cliente_id = int(input("ID do cliente: "))
        except ValueError:
            print("ID inválido.")
            return
        cliente = next((c for c in self.clientes if c.cliente_id == cliente_id), None)
        if not cliente:
            print("Cliente não encontrado.")
            return

        itens = []
        total = 0
        while True:
            self.mostrar_cardapio()
            entrada = input("ID do produto (ou 'sair'): ")
            if entrada.lower() == 'sair':
                break
            try:
                produto_id = int(entrada)
                produto = next((p for p in self.produtos if p.produto_id == produto_id), None)
                if not produto:
                    print("Produto não encontrado.")
                    continue
                quantidade = int(input("Quantidade: "))
                if quantidade > produto.estoque or quantidade <= 0:
                    print(f"Estoque insuficiente. Disponível: {produto.estoque}")
                    continue
                itens.append((produto_id, quantidade))
                total += produto.preco * quantidade
                produto.estoque -= quantidade
            except ValueError:
                print("Entrada inválida.")
                continue

        if not itens:
            print("Pedido cancelado.")
            return

        novo_pedido = Pedido(self.id_pedido, cliente_id, itens, total)
        self.pedidos.append(novo_pedido)
        cliente.adicionar_pontos(total)
        print(f"Pedido {self.id_pedido} finalizado. Total: R${total:.2f}")
        self.id_pedido += 1

    def ver_pedidos(self):
        print("\n--- Pedidos ---")
        for pedido in self.pedidos:
            print(f"Pedido {pedido.pedido_id} (Cliente {pedido.cliente_id}):")
            for item in pedido.itens:
                produto_id, qtd = item
                produto = next(p for p in self.produtos if p.produto_id == produto_id)
                print(f"  {produto.nome} x{qtd}: R${produto.preco * qtd:.2f}")
            print(f"Total: R${pedido.total:.2f}")

    def ver_clientes(self):
        print("\n--- Clientes ---")
        for cliente in self.clientes:
            print(f"ID: {cliente.cliente_id} | Nome: {cliente.nome}")
            print(f"Pontos: {cliente.pontos}")


if __name__ == "__main__":
    sistema = SistemaCafeteria()
    sistema.menu_principal()
