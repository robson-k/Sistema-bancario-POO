from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf: str, nome: str, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._cliente = cliente
        self.numero = numero
        self.agencia = "0001"
        self.historico = Historico()

    @property
    def saldo(self) -> float:
        return self._saldo

    @classmethod
    def nova_conta(cls, cliente, numero: int):
        return cls(numero, cliente)

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor: float) -> bool:
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("Valor de saque maior do que o que está na conta bancária.")
        elif valor > 0:
            self._saldo -= valor
            print(f"Saque de R${valor:.2f} realizado com sucesso!")
            return True

        else:
            print("Valor inferior a R$0! Tente novamente.")

        return False

    def depositar(self, valor: float) -> bool:
        saldo = self.saldo

        if valor > 0:
            self._saldo += valor
            print(f"Depósito de R${valor:.2f}ealizado com sucesso!")
            return True
        else:
            print("Valor de depósito inválido! Tente novamente.")

        return False


class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500, limite_saques=3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saque = limite_saques

        def sacar(self, valor):
            nro_saques = len(
                [
                    transacao
                    for transacao in self.historico.transacoes
                    if transacao["tipo"] == "Saque"
                ]
            )

            excedeu_limite = valor > self.limite
            excedeu_saques = nro_saques >= self.limite_saques

            if excedeu_saques:
                print("Operação falhou, você excedeu o limite diário de saques.")
            elif excedeu_limite:
                print(
                    f"Operação falhou, R${valor:.2f} maior do que o limite de saque R${limite:.2f} ."
                )
            else:
                return super().sacar(valor)

            return False

        def __str__(self):
            return f"""\
                Agência:\t{self.agencia}
                C/C:\t\t{self.numero}
                Titular:\t{self.cliente.nome}
            """


class Historico:
    def __init__(self, transacoes):
        self.transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self.transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
