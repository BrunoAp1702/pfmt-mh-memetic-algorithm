import os
import random
import math

def gerar_instancia(caminho_pasta, n_pessoas=50, m_projetos=5, f_habilidades=5, fracoes_tempo=[0.5, 1.0], taxa_harmonia=0.5):
	os.makedirs(caminho_pasta, exist_ok=True)

	# GERAR D.txt (Frações de Tempo)
	t_tamanho = len(fracoes_tempo)
	alfa = fracoes_tempo[0]
	with open(os.path.join(caminho_pasta, 'D.txt'), 'w') as f:
		f.write(f"{t_tamanho}\n")
		f.write(" ".join(map(str, fracoes_tempo)) + "\n")

	# GERAR K.txt (Matriz de Habilidades)
	K = []
	for i in range(n_pessoas):
		qtd_habilidades = random.randint(1, min(3, f_habilidades))
		habilidades_pessoa = [0] * f_habilidades
		indices_hab = random.sample(range(f_habilidades), qtd_habilidades)
		for idx in indices_hab:
			habilidades_pessoa[idx] = 1
		K.append(habilidades_pessoa)

	with open(os.path.join(caminho_pasta, 'K.txt'), 'w') as f:
		f.write(f"{f_habilidades}\n")
		for linha in K:
			f.write(" ".join(map(str, linha)) + "\n")

	# GERAR S.txt (Matriz Sociométrica - Harmonia)
	S = []
	for i in range(n_pessoas):
		linha_S = []
		for j in range(n_pessoas):
			if i == j:
				linha_S.append(1)
			else:
				r = random.random()
				if r < taxa_harmonia:
					linha_S.append(1)
				elif r < taxa_harmonia + ((1 - taxa_harmonia) / 2):
					linha_S.append(0)
				else:
					linha_S.append(-1)
		S.append(linha_S)

	with open(os.path.join(caminho_pasta, 'S.txt'), 'w') as f:
		f.write(f"{n_pessoas}\n")
		for linha in S:
			f.write(" ".join(map(str, linha)) + "\n")

	# GERAR R.txt (Demandas dos Projetos)
	capacidade_por_habilidade = [sum(K[i][j] for i in range(n_pessoas)) for j in range(f_habilidades)]
# GERAR R.txt (Demandas dos Projetos)
	capacidade_por_habilidade = [sum(K[i][j] for i in range(n_pessoas)) for j in range(f_habilidades)]
	R = []
	for i in range(m_projetos):
		linha_R = []
		for j in range(f_habilidades):
			max_demanda_possivel = (capacidade_por_habilidade[j] / m_projetos) * 0.7 
			limite_superior = math.floor(max_demanda_possivel / alfa)
			
			# Garante que sorteie pelo menos 0, mas vamos forçar um valor mínimo abaixo
			demanda_sorteada = random.randint(0, max(1, limite_superior)) * alfa
			linha_R.append(demanda_sorteada)
		
		# BLINDAGEM: Se a linha inteira deu zero, força a primeira habilidade a pedir 1 pessoa
		if sum(linha_R) == 0:
			linha_R[0] = 1.0 * alfa
			
		R.append(linha_R)
			
	print(f"Instância gerada com sucesso em: {caminho_pasta}")

if __name__ == "__main__":
    # Parametros baseados no TCC de Viana (2018)
    categorias = [("Categoria A", 0.3), ("Categoria B", 0.5), ("Categoria C", 0.7)]
    classes = [
        ("Classe2", 5, 50, 5, [0.0, 1.0]),                   # m=5, n=50, f=5, tempo integral
        ("Classe4", 5, 50, 5, [0.0, 0.5, 1.0]),              # m=5, n=50, f=5, meio período
        ("Classe6", 5, 50, 5, [0.0, 0.25, 0.5, 0.75, 1.0])   # m=5, n=50, f=5, fracionado
    ]
    
    for nome_cat, taxa in categorias:
        for nome_cl, m, n, f, tempos in classes:
            # Removendo o 0.0 da lista de sorteio para o gerador nao bugar
            tempos_validos = [t for t in tempos if t > 0]
            
            for i in range(1, 16): # 15 instâncias por classe para totalizar 45 por categoria
                caminho = f"./instancias/{nome_cat}/{nome_cl}/Grupo_{i}"
                gerar_instancia(
                    caminho_pasta=caminho,
                    n_pessoas=n, 
                    m_projetos=m, 
                    f_habilidades=f, 
                    fracoes_tempo=tempos_validos,
                    taxa_harmonia=taxa 
                )
    print(">>> 135 INSTÂNCIAS GERADAS COM SUCESSO!")