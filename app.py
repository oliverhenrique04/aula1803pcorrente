import multiprocessing
import time
import os

def somar_bloco(bloco_de_linhas):
    """
    Função que recebe uma lista de linhas (strings), 
    converte para número e retorna a soma do bloco.
    """
    soma_parcial = 0
    for linha in bloco_de_linhas:
        linha = linha.strip()
        if linha:  # Ignora linhas vazias
            try:
                soma_parcial += float(linha) 
            except ValueError:
                pass # Ignora linhas que não são números válidos
    return soma_parcial

def somar_arquivo_multiprocessing(nome_arquivo, num_processos, tamanho_bloco=100000):
    """
    Lê o arquivo em partes e distribui a soma usando a quantidade de processos escolhida.
    """
    print(f"\nIniciando processamento com {num_processos} processos...")

    # Cria o Pool de processos com a quantidade definida pelo usuário
    pool = multiprocessing.Pool(processes=num_processos)
    resultados_assincronos = []

    with open(nome_arquivo, 'r') as arquivo:
        bloco = []
        for linha in arquivo:
            bloco.append(linha)
            
            # Quando o bloco atinge o tamanho definido, envia para um processo
            if len(bloco) >= tamanho_bloco:
                resultado = pool.apply_async(somar_bloco, (bloco,))
                resultados_assincronos.append(resultado)
                bloco = [] # Esvazia o bloco para preencher novamente
        
        # Envia o último bloco restante (se houver)
        if bloco:
            resultado = pool.apply_async(somar_bloco, (bloco,))
            resultados_assincronos.append(resultado)

    # Fecha o pool para novos envios e aguarda os processos finalizarem
    pool.close()
    pool.join()

    # Coleta todas as somas parciais e soma tudo
    soma_total = sum(res.get() for res in resultados_assincronos)
    
    return soma_total

if __name__ == '__main__':
    nome_do_seu_arquivo = 'numerogigante.txt'
    
    # Descobre o número máximo de núcleos do computador
    max_cores = multiprocessing.cpu_count()
    
    print("-" * 40)
    print(f"Seu processador possui {max_cores} núcleos disponíveis.")
    print("-" * 40)
    
    # Loop para garantir que o usuário digite um número válido
    while True:
        try:
            escolha = input(f"Quantos processos você deseja usar? (Recomendado: 1 a {max_cores}): ")
            qtd_processos = int(escolha)
            
            if qtd_processos > 0:
                break
            else:
                print("Por favor, digite um número maior que zero.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")
    
    try:
        print(f"\nLendo o arquivo: {nome_do_seu_arquivo}")
        tempo_inicio = time.time() # Inicia o cronômetro
        
        # Executa a função principal passando a quantidade de processos escolhida
        soma = somar_arquivo_multiprocessing(nome_do_seu_arquivo, qtd_processos)
        tempo_fim = time.time() # Para o cronômetro
        
        print("-" * 40)
        print(f"** A soma total é: {soma} **")
        print(f"Tempo de execução: {tempo_fim - tempo_inicio:.2f} segundos")
        print("-" * 40)
        
    except FileNotFoundError:
        print(f"\nERRO: O arquivo '{nome_do_seu_arquivo}' não foi encontrado.")
        print("Verifique se o arquivo está salvo na exata mesma pasta que este script Python.")