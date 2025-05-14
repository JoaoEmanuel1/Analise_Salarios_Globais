import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# configuração do estilo dos gráficos
sns.set_theme(style="whitegrid")
sns.set_palette("viridis")

def busca_dados_salarios(records=100):
    
    # API com dados fictícios para utilizando RandomData
    url = "https://random-data-api.com/api/v2/users"
    params = {
        "size": records,
        "response_type": "json"
    }
    
    try:
        # Realiza e verifica se houve algum erro na requisição
        response = requests.get(url, params=params)
        response.raise_for_status()  
        
        data = response.json()
        
        # Verifica se a resposta é uma lista
        if not isinstance(data, list):
            raise ValueError("A API não retornou uma lista de usuários como esperado")
            
        salaries = []
        
        for user in data:
            
            if not isinstance(user, dict):
                continue
                
            try:
                # Faz o mapeamento dos dados que serão utilizados no gráfico
                salaries.append({
                    "country": user.get("address", {}).get("country", "Unknown"),
                    "salary": user.get("employment", {}).get("annual_income", 0),
                    "experience": user.get("employment", {}).get("years_of_experience", 0),
                    "education": user.get("employment", {}).get("education_level", "Unknown")
                })

            except AttributeError:
                continue
                
        return pd.DataFrame(salaries)
        
    except Exception as e:
        print(f"Erro ao buscar dados: {str(e)}")
        return pd.DataFrame()  # Retorna DataFrame vazio em caso de erro

# Carrega os dados
df = busca_dados_salarios(records=200)

# Verifica se tem dados
if df.empty:
    print("Não foi possível obter dados da API. Criando dados de exemplo...")

    # caso não tenha dados é criado alguns para exemplos
    data = {
        "country": ["USA", "Brazil", "Germany", "UK", "Japan"] * 40,
        "salary": np.random.randint(30000, 150000, 200),
        "experience": np.random.randint(0, 30, 200),
        "education": np.random.choice(["High School", "Bachelor", "Master", "PhD"], 200)
    }

    df = pd.DataFrame(data)

# Limpeza básica e remoção de salários zerados/negativos
df = df.dropna()
df = df[df["salary"] > 0]

# Gráfico 1: TOP 5 PAÍSES COM MAIORES SALÁRIOS MÉDIOS
plt.figure(figsize=(10, 5))
top_countries = df.groupby("country")["salary"].mean().nlargest(5)
top_countries.plot(kind="bar", title="Média Salarial por País (Top 5)")
plt.xlabel("País")
plt.ylabel("Salário Anual (USD)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Gráfico 2: DISTRIBUIÇÃO DE SALÁRIOS POR EXPERIÊNCIA
plt.figure(figsize=(10, 5))
sns.boxplot(x="experience", y="salary", data=df[df["experience"] <= 30])
plt.title("Salário vs Anos de Experiência")
plt.xlabel("Anos de Experiência")
plt.ylabel("Salário Anual (USD)")
plt.show()

# Gráfico 3: SALÁRIO MÉDIO POR NÍVEL DE EDUCAÇÃO
plt.figure(figsize=(10, 5))
sns.barplot(
    x="education", 
    y="salary", 
    data=df, 
    estimator=np.mean,
    errorbar=None
)

plt.title("Salário Médio por Nível de Educação")
plt.xlabel("Nível de Educação")
plt.ylabel("Salário Anual (USD)")
plt.xticks(rotation=45)
plt.show()