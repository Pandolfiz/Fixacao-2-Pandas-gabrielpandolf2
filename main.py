import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


print('\n--------------------------------------------------------------------')
# Lendo o DataFrame 
df = pd.read_csv('CBC data_for_meandeley_csv.csv')
print(df)

print('\n------------------------------------------------')
# Realizando uma analise sobre os dados presentes no DF e retirando alguns insights

print(df.shape)
print(df.head(10))
print(df.tail(10))
print(df.describe(include='all'))
print(df.info)
print(df.isnull().sum())
print(df.dtypes)

print('\n--------------------------------------------------------------------')

# Qual a aplicabilidade para o identificador S. No e da primeira linha(linha 0) que identifica a nomeclatura de cada coluna ? 

df= df.drop('S. No.',axis=1)
df = df.drop(0)
print(df)

print('\n------------------------------------------------')

# Quantos Not ate Number(NaN) existem no dataframe ? A presença dele interefere na analise ?

nan_count = df.isna().sum()
print(nan_count)
df.dropna(inplace=True)
print(df)

print('\n------------------------------------------------')

#Sexo e Genero se expressam analisados sobre o mesmo viés 1(H) 0(M)?

df = df.rename(columns = {'Sex  ':'Gen'})
print(df.head())

print('\n------------------------------------------------')

# Alguns atributos possuem espaços, realizaremos a retiradas desses espaços como .strip

print(df.columns)
df.columns = df.columns.str.strip()
print(df.columns)

print('\n------------------------------------------------')

#Quantos individuos são menores de 18 anos ? Como se esobça um data frame filtrado ?

def filtro_menor_18(idade):
  if idade < 18:
      return 'Menor que 18 anos '
  else:
      return 'Maior que 18 anos'

result = df['Age'].apply(filtro_menor_18)
filtered_df = df[result == 'Menor que 18 anos ']
print(filtered_df)
print('A quantidade de homens menores de 18 anos é dada por :', (filtered_df['Gen'] == 1).sum())
print('A quantidade de mulheres menores de 18 anos é dada por :',(filtered_df['Gen'] == 0).sum())

print('\n------------------------------------------------')

# Qual a media da idade dos pacientes e como se esboça a proporção de plaquetas por Litro sanguíneo ?

df['Age'].mean()
def mm3_para_litros(mm3_value):
    return float(mm3_value) * 1e-9
  
df['PLT /Litros'] = df['PLT /mm3'].apply(mm3_para_litros)
print(df)

print('\n------------------------------------------------')

# Qual o valor maximo de cada coluna e a variância dos dados em cada linha ?

df['Valor_Maximo'] = df.max(axis=1,numeric_only =True)
df['Variância'] = df.var(axis=1,numeric_only =True)
print(df)

print('\n------------------------------------------------')

# Qual a media de hemoglobina e eritrócitos na corrente sanguinea da base de dados abordada ?

df['HGB'] = pd.to_numeric(df['HGB'], errors='coerce')
media_hemoglobina = df['HGB'].mean()
print('A média de hemoglobina da amostra é dada por : ', media_hemoglobina)
df['RBC'] = pd.to_numeric(df['RBC'], errors='coerce')
media_CELVERMELHA = df['RBC'].mean()
print('A média de Hemácias da amostra é dada por : ',media_CELVERMELHA)

print('\n----------------------------------------------')

# Filtro  para a idade onde a coluna 'HGB' é menor que media_hemoglobina e o número de células vermelhas (coluna 'RBC') é menor que media_CELVERMELHA

print(df[(df['HGB'] < media_hemoglobina) & (df['RBC'] < media_CELVERMELHA)])
df['PLT /mm3'] = pd.to_numeric(df['PLT /mm3'], errors='coerce')
df['TLC'] = pd.to_numeric(df['TLC'], errors='coerce')

print('\n----------------------------------------------')

# Média da contagem de leucócitos ('TLC') para cada categoria ou grupo de valores de contagem de células vermelhas ('RBC') e como a média da contagem de leucócitos varia em relação à contagem de células vermelhas.

print(df.groupby('RBC')['TLC'].mean(numeric_only=True))

print('\n----------------------------------------------')

# Grafico Iterativo utilizando plotly.express da relação de Hemácias e Leucócitos

'''
fig  = px.scatter(df, x = 'RBC', y = 'TLC', log_x = True, width = 800)
fig.update_traces(marker = dict(size = 12, line=dict(width = 2)), selector = dict(mode = 'markers'))
fig.update_layout(title = 'Relação Celulas Vermelhas e Leucócitos')
fig.update_xaxes(title = 'RBC')
fig.update_yaxes(title = 'TLC')
fig.show()
'''

print('\n----------------------------------------------')

# Gráfico de Dispersão RBC vs. TLC

x = df['RBC']
y = df['TLC']
plt.scatter(x, y)
plt.xlabel('RBC')
plt.ylabel('TLC')
plt.title('Gráfico de Dispersão RBC vs. TLC')
plt.show()

print('\n----------------------------------------------')

# Dividindo a faixa etária dos pacientes utilizando pd.cut

intervalos = [0, 12, 18, 60, 100]  
df['Faixa Etária'] = pd.cut(df['Age'], bins=intervalos, labels=['Criança', 'Jovem', 'Adulto', 'Idoso'])
print(df)

print('\n----------------------------------------------')

# Grafico da Faixa Etária 

plt.figure(figsize=(7,7))
ax = sns.countplot(x=df['Faixa Etária'])
plt.title('Faixa Etária')
for p in ax.patches:
    plt.annotate(p.get_height(), xy=(p.get_x() + 0.25, p.get_height()), fontsize=14)
plt.show()
print('\n----------------------------------------------')

# Exportando o Arquivo para CSV

df.to_csv('Anemia_Manipulado', index=False)