import random
import sys

# Paleta de cores (ANSI)
RESET = "\033[0m"
NEGRITO = "\033[1m"
VERDE = "\033[32m"
AMARELO = "\033[33m"
CINZA = "\033[90m"

def pintar(letra: str, status: str) -> str:
    """
    Retorna uma string colorida com base no status da letra.

    Args:
        letra (str): Letra a ser exibida.
        status (str): Estado da letra em relação à palavra secreta.
                      Pode ser 'correto', 'parcial' ou 'errado'.

    Returns:
        str: Representação colorida da letra dentro de colchetes.
    """
    if status == 'correto':
        return f"{NEGRITO}{VERDE}[{letra}]{RESET}"
    elif status == 'parcial':
        return f"{NEGRITO}{AMARELO}[{letra}]{RESET}"
    else:
        return f"{NEGRITO}{CINZA}[{letra}]{RESET}"

PALAVRAS = {
    5: ['limao', 'amora', 'banco', 'carta', 'dente', 'folha', 'grade', 'honra', 'carne', 'feira', 'limpo', 'manga', 'noite', 'livro', 'pedra', 'tinta', 'roupa', 'sabor', 'tampa', 'praia', 'velho', 'vinho', 'sonho', 'lenda', 'manto'],
    6: ['banana', 'jardim', 'retina', 'correr', 'lanche', 'seguro', 'motivo', 'direto', 'janela', 'chance', 'origem', 'batata', 'viagem', 'alface', 'contra', 'truque', 'temido', 'formal', 'objeto', 'acento', 'isento', 'prazer', 'sempre', 'rotina'],  
    7: ['marisco', 'pantano', 'empatia', 'cultura', 'virtude', 'desenho', 'pintura', 'mercado', 'sucesso', 'alegria', 'orgulho', 'saudade', 'coragem', 'modesto', 'parcial', 'vigente', 'piedade', 'sentido', 'bizarro', 'intenso', 'ousadia', 'desafio', 'palavra', 'intuito', 'cuidado']
}

def exibir_regras():
    """
    Exibe as regras do jogo para o jogador no terminal.
    """
    print("=======================================================")
    print("=====       Bem-vindo ao clone do Term.ooo!       =====")
    print("=======================================================\n")
    print("Regras do jogo:")
    print("1. Escolha a dificuldade: palavras de 5, 6 ou 7 letras.")
    print("2. Você terá um número de tentativas igual ao comprimento da palavra.")
    print("3. Após cada tentativa, você verá as dicas por cor:")
    print(f"   - {pintar('A','correto')} letra correta no lugar certo.")
    print(f"   - {pintar('A','parcial')} letra existe na palavra mas em outro lugar.")
    print(f"   - {pintar('A','errado')} letra não existe na palavra.")
    print("4. As palavras não possuem acentos e a avaliação ignora maiúsculas/minúsculas.\n")

def obter_dificuldade() -> int:
    """
    Solicita ao jogador que escolha a dificuldade (5, 6 ou 7).

    Returns:
        int: O tamanho da palavra escolhida pelo jogador.
    """
    while True:
        dificuldade = input("Escolha a dificuldade (5, 6 ou 7): ").strip()
        if dificuldade in ['5', '6', '7']:
            return int(dificuldade)
        else:
            print("Entrada inválida. Por favor, digite 5, 6 ou 7.")

def sortear_palavra(tamanho: int) -> str:
    """
    Seleciona aleatoriamente uma palavra de acordo com o tamanho escolhido.

    Args:
        tamanho (int): Número de letras da palavra.

    Returns:
        str: Palavra secreta sorteada.
    """
    return random.choice(PALAVRAS[tamanho]).lower()

def obter_palpite(tamanho: int) -> str:
    """
    Solicita ao jogador um palpite de palavra com o tamanho correto.

    Args:
        tamanho (int): Número de letras que a palavra deve ter.

    Returns:
        str: Palpite válido do jogador (em minúsculas).
    """
    while True:
        palpite = input(f"Digite sua tentativa de {tamanho} letras: ").strip().lower()
        if len(palpite) != tamanho:
            print(f"Por favor, digite exatamente {tamanho} letras.")
        elif not palpite.isalpha():
            print("Entrada inválida. Use apenas letras.")
        else:
            return palpite

def avaliar_palpite(palpite: str, palavra_secreta: str):
    """
    Avalia o palpite comparando com a palavra secreta.

    Args:
        palpite (str): Palavra tentada pelo jogador.
        palavra_secreta (str): Palavra correta que deve ser descoberta.

    Returns:
        list[tuple[str, str]]: Lista de pares (LETRA, status), onde:
            - status = 'correto' se letra está na posição certa.
            - status = 'parcial' se letra está na palavra mas em outra posição.
            - status = 'errado' se letra não está na palavra.
    """
    n = len(palpite)
    status = ['errado'] * n
    letras_restantes = list(palavra_secreta)

    # 1º passe: acertos na posição
    for i in range(n):
        if palpite[i] == palavra_secreta[i]:
            status[i] = 'correto'
            letras_restantes[i] = None  # consome essa letra

    # 2º passe: letras corretas em posições erradas
    for i in range(n):
        if status[i] == 'correto':
            continue
        ch = palpite[i]
        if ch in letras_restantes:
            status[i] = 'parcial'
            letras_restantes[letras_restantes.index(ch)] = None  # consome uma ocorrência

    return [(palpite[i].upper(), status[i]) for i in range(n)]

def imprimir_dicas(dicas: list[tuple[str, str]]):
    """
    Exibe no terminal as dicas coloridas da tentativa.

    Args:
        dicas (list[tuple[str, str]]): Lista de pares (LETRA, status).
    """
    pintados = [pintar(letra, st) for letra, st in dicas]
    print("Dicas:", " ".join(pintados))

def jogar_rodada():
    """
    Executa uma rodada do jogo:
    - Mostra regras
    - Sorteia palavra
    - Controla as tentativas
    - Exibe dicas coloridas
    - Declara vitória ou derrota
    """
    exibir_regras()
    tamanho = obter_dificuldade()
    palavra_secreta = sortear_palavra(tamanho)
    max_tentativas = tamanho
    tentativas = 0

    while tentativas < max_tentativas:
        palpite = obter_palpite(tamanho)
        tentativas += 1

        if palpite == palavra_secreta:
            # Mostra a palavra toda verde
            palavra_colorida = " ".join([pintar(ch.upper(), 'correto') for ch in palavra_secreta])
            print("\n" + palavra_colorida)
            print(f"\n Parabéns! Você acertou a palavra '{palavra_secreta.upper()}' em {tentativas} tentativa(s)!")
            return

        dicas = avaliar_palpite(palpite, palavra_secreta)
        imprimir_dicas(dicas)

    print(f"\nFim de jogo! A palavra correta era: {NEGRITO}{palavra_secreta.upper()}{RESET}")

def jogar():
    """
    Controla o fluxo contínuo do jogo.
    Permite jogar várias rodadas até que o usuário decida parar.
    """
    try:
        while True:
            jogar_rodada()
            novamente = input("\nDeseja jogar novamente? (s/n): ").strip().lower()
            if novamente != 's':
                print("Obrigado por jogar! Até a próxima.")
                break
    except (KeyboardInterrupt, EOFError):
        print("\nSaindo... Obrigado por jogar!")
        sys.exit(0)

if __name__ == "__main__":
    jogar()
