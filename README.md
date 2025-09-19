# Gerador de Senhas

Um gerador de senhas em Python, simples e seguro, utilizando `secrets` para aleatoriedade criptográfica.

## Funcionalidades

- Gera senhas aleatórias personalizadas.
- Permite incluir letras minúsculas, maiúsculas, números e símbolos.
- Avalia a força da senha (Fraca, Média, Forte, Muito Forte).
- Copia senhas para a área de transferência (se `pyperclip` estiver instalado).
- Salva senhas em arquivo (`senhas_1.txt`, `senhas_2.txt`, ...).

## Instalação

1. Tenha o Python 3 instalado.
2. Instale dependências opcionais:

```bash
pip install pyperclip
```

## Uso

Execute o programa:

```bash
python3 gerador_senhas.py
```

Responda às perguntas no terminal e escolha o que deseja fazer com as senhas geradas.

## Exemplo de saída

```text
=== Gerador de Senhas ===

Quantas senhas deseja gerar? 3
Qual o tamanho de cada senha? 12
Incluir letras minúsculas? (s/n): s
Incluir letras maiúsculas? (s/n): s
Incluir números? (s/n): s
Incluir símbolos? (s/n): s

=== Configuração escolhida ===

Quantidade: 3
Tamanho: 12 caracteres
Tipos incluídos: Minúsculas, Maiúsculas, Números, Símbolos

=== Senhas geradas ===

 Ab3$kT7!dQpL   [ Forte ]
 Gt8&hL2@wZmX   [ Forte ]
 Px9!rA4^tJbN   [ Forte ]

O que deseja fazer agora?
  1 - Copiar para área de transferência
  2 - Salvar em arquivo
  3 - Cancelar

Selecione uma opção (1,2,3):
```

---

## Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
