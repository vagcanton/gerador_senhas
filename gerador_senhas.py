from datetime import datetime
import string
import secrets
import math

try:
    import pyperclip
    from pyperclip import PyperclipException

    CLIP_AVAILABLE = True
except ImportError:
    CLIP_AVAILABLE = False

contador = 1


# --- Monta conjunto de caracteres ---
def montar_conjunto(minusculas, maiusculas, numeros, simbolos, remover_perigosos=True):

    letras_min = string.ascii_lowercase if minusculas else ""
    letras_mai = string.ascii_uppercase if maiusculas else ""
    nums = string.digits if numeros else ""
    simb = string.punctuation if simbolos else ""

    if remover_perigosos:
        simb_proibidos = "\"'\\/:`<>,|=~"
        simb = "".join(c for c in simb if c not in simb_proibidos)

    todos = letras_min + letras_mai + nums + simb
    if not todos:
        raise ValueError("\nErro: nenhum tipo de caractere selecionado\n")
    return todos, letras_min, letras_mai, nums, simb


# --- Gera senhas ---
def gerar_senhas(qtd, tamanho, minusculas=True, maiusculas=True, numeros=True, simbolos=True):

    rng = secrets.SystemRandom()

    todos, letras_min, letras_mai, nums, simb = montar_conjunto(minusculas, maiusculas, numeros, simbolos)

    tipos = [
        (letras_min, minusculas),
        (letras_mai, maiusculas),
        (nums, numeros),
        (simb, simbolos),
    ]
    ativos = sum(1 for _, ativo in tipos if ativo)

    if tamanho < ativos:
        raise ValueError(f"\nErro: o tamanho mínimo é {ativos} para incluir todos os tipos escolhidos\n")

    if len(todos) ** tamanho < qtd:
        raise ValueError(
            f"\nErro: com {len(todos)} caracteres disponíveis, só é possível gerar até {len(todos) ** tamanho} senhas únicas\n"
        )

    senhas = set()
    while len(senhas) < qtd:
        senha = [secrets.choice(chars) for chars, ativo in tipos if ativo]
        senha += [secrets.choice(todos) for _ in range(tamanho - len(senha))]
        rng.shuffle(senha)
        senhas.add("".join(senha))
    return list(senhas)


# --- Avalia força ---
def avaliar_forca(senha, minusculas, maiusculas, numeros, simbolos):

    todos, letras_min, letras_mai, nums, simb = montar_conjunto(minusculas, maiusculas, numeros, simbolos)

    if len(senha) < 8:
        return "Fraca"
    for ativo, chars in [
        (minusculas, letras_min),
        (maiusculas, letras_mai),
        (numeros, nums),
        (simbolos, simb),
    ]:
        if ativo and not any(c in chars for c in senha):
            return "Fraca (faltam tipos exigidos)"

    entropia = len(senha) * math.log2(len(todos))
    if len(senha) >= 16 and entropia >= 90:
        return "Muito Forte"
    if len(senha) >= 12 and entropia >= 70:
        return "Forte"
    if len(senha) >= 8 and entropia >= 50:
        return "Média"
    return "Fraca"


# --- Interação ---
def perguntar_inteiro(msg, minimo=None, maximo=None):

    while True:
        try:
            valor = int(input(msg))
            if minimo is not None and valor < minimo:
                print(f"\nErro: {valor} é menor que o mínimo permitido ({minimo})\n")
                continue
            if maximo is not None and valor > maximo:
                print(f"\nErro: {valor} é maior que o máximo permitido ({maximo})\n")
                continue
            return valor
        except ValueError:
            print("\nDigite apenas números inteiros\n")


def perguntar_sim_nao(msg):

    while True:
        resp = input(msg + " (s/n): ").strip().lower()
        if resp in ("s", "n"):
            return resp == "s"
        print("\nDigite apenas 's' para sim ou 'n' para não\n")


def perguntar_opcao():

    menu = (
        "\nO que deseja fazer agora?\n"
        "  1 - Copiar para área de transferência\n"
        "  2 - Salvar em arquivo\n"
        "  3 - Cancelar\n"
        "\nSelecione uma opção (1,2,3): "
    )

    while True:
        escolha = input(menu).strip()

        if escolha in ("1", "2", "3"):
            return escolha
        print("\nDigite apenas 1, 2 ou 3")


def copiar_para_area(senhas):
    if not CLIP_AVAILABLE:
        print("Pyperclip não instalado, não é possível copiar")
        return

    try:
        pyperclip.copy("\n".join(senhas))
        print("\nSenhas copiadas para a área de transferência")
    except PyperclipException:
        print(
            "\nNão foi possível copiar as senhas.\n"
            "No Linux X11, instale 'xclip' ou 'xsel':\n"
            "  sudo apt install xclip\nou\n"
            "  sudo apt install xsel\nDepois, tente novamente"
        )


def salvar_arquivo(senhas):

    global contador
    arquivo = f"senhas_{contador}.txt"
    contador += 1

    try:
        with open(arquivo, "w", encoding="utf-8") as f:
            f.write("\n".join(senhas))
        print(f"\nSenhas salvas em '{arquivo}'")
    except OSError:
        print(f"\nErro: não foi possível salvar no arquivo '{arquivo}'")


def formatar_tipos(minusculas, maiusculas, numeros, simbolos):

    tipos = [
        nome
        for ativo, nome in [
            (minusculas, "Minúsculas"),
            (maiusculas, "Maiúsculas"),
            (numeros, "Números"),
            (simbolos, "Símbolos"),
        ]
        if ativo
    ]
    return ", ".join(tipos)


# --- Main ---
def main():

    while True:
        print("\n=== Gerador de Senhas ===\n")

        qtd = perguntar_inteiro("Quantas senhas deseja gerar? ", 1, 100)
        tamanho = perguntar_inteiro("Qual o tamanho de cada senha? ", 4, 64)

        while True:
            minusculas = perguntar_sim_nao("Incluir letras minúsculas?")
            maiusculas = perguntar_sim_nao("Incluir letras maiúsculas?")
            numeros = perguntar_sim_nao("Incluir números?")
            simbolos = perguntar_sim_nao("Incluir símbolos?")

            if any([minusculas, maiusculas, numeros, simbolos]):
                break
            print("\nErro: escolha pelo menos um tipo de caractere\n")

        try:
            senhas = gerar_senhas(qtd, tamanho, minusculas, maiusculas, numeros, simbolos)
        except ValueError as e:
            print(e)
            continue

        print(
            "\n=== Configuração escolhida ===\n"
            f"\nQuantidade: {qtd}"
            f"\nTamanho: {tamanho} caracteres"
            f"\nTipos incluídos: {formatar_tipos(minusculas, maiusculas, numeros, simbolos)}"
        )

        print("\n=== Senhas geradas ===\n")

        for s in senhas:
            print(f" {s}   [ {avaliar_forca(s, minusculas, maiusculas, numeros, simbolos)} ]")

        # Aviso de senha curta
        if tamanho < 8:
            print(
                "\nAviso: senhas com menos de 8 caracteres são menos seguras"
                "\nConsidere gerar com tamanho maior ou incluir mais tipos de caracteres"
            )

        # --- Menu de ação ---
        acoes = {
            "1": lambda: copiar_para_area(senhas),
            "2": lambda: salvar_arquivo(senhas),
            "3": lambda: print("\nNenhuma ação realizada"),
        }

        opcao = perguntar_opcao()
        acoes[opcao]()

        if not perguntar_sim_nao("\nDeseja gerar mais senhas?"):
            break

    print("\nOperação finalizada. Obrigado por utilizar o sistema")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperação interrompida pelo usuário.")
