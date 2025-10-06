import pandas as pd
import numpy as np
import os

# Dados para o dataset sintético
data = {
    'juizo': [
        '1ª Vara Cível de São Paulo', '2ª Vara Cível de São Paulo', '3ª Vara do Consumidor de Salvador', '1ª Vara Cível de Curitiba',
        '2ª Vara do Consumidor de Salvador', '1ª Vara Cível de São Paulo', '1ª Vara Cível de Curitiba', '3ª Vara do Consumidor de Salvador',
        '2ª Vara Cível de São Paulo', '1ª Vara Cível de São Paulo', '1ª Vara Cível de Curitiba', '2ª Vara do Consumidor de Salvador',
        '1ª Vara Cível de São Paulo', '3ª Vara do Consumidor de Salvador', '2ª Vara Cível de São Paulo', '1ª Vara Cível de Curitiba'
    ] * 10,
    'tese_juridica': [
        'Negativação indevida por dívida já paga', 'Produto com vício oculto não sanado no prazo legal', 'Cobrança de taxa de serviço não informada previamente', 'Falha na prestação de serviço de telefonia com cobrança indevida',
        'Atraso na entrega de produto comprado online', 'Negativação indevida por dívida já paga', 'Produto com vício oculto não sanado no prazo legal', 'Atraso na entrega de produto comprado online',
        'Falha na prestação de serviço de telefonia com cobrança indevida', 'Negativação indevida por dívida já paga', 'Cobrança de taxa de serviço não informada previamente', 'Produto com vício oculto não sanado no prazo legal',
        'Atraso na entrega de produto comprado online', 'Cobrança de taxa de serviço não informada previamente', 'Falha na prestação de serviço de telefonia com cobrança indevida', 'Negativação indevida por dívida já paga'
    ] * 10,
    'resultado': [
        'Procedente', 'Procedente', 'Improcedente', 'Procedente',
        'Procedente', 'Procedente', 'Improcedente', 'Procedente',
        'Improcedente', 'Procedente', 'Procedente', 'Procedente',
        'Improcedente', 'Procedente', 'Procedente', 'Improcedente'
    ] * 10,
    'texto_decisao': [
        'JULGO PROCEDENTE o pedido para declarar a inexigibilidade do débito e condenar a ré ao pagamento de indenização por danos morais no valor de R$ 10.000,00, uma vez que a inscrição em cadastro de inadimplentes se deu por dívida comprovadamente quitada.',
        'Acolho o pedido do autor, com base no Art. 18 do CDC, para determinar a substituição do produto por outro da mesma espécie, em perfeitas condições de uso, visto que o vício não foi sanado no prazo de 30 dias.',
        'JULGO IMPROCEDENTE o pedido, pois a taxa de serviço estava prevista em contrato de adesão, sendo de conhecimento prévio do consumidor. Não há que se falar em abusividade.',
        'É procedente o pedido de repetição de indébito em dobro, bem como a condenação por danos morais, fixados em R$ 5.000,00, dada a falha na prestação do serviço e a cobrança por serviço não contratado.',
        'Condeno a ré a indenizar o autor por danos materiais e morais, estes fixados em R$ 3.000,00, pelo atraso injustificado na entrega do produto, que ultrapassou o prazo prometido em 45 dias.',
        'Diante da comprovação do pagamento anterior à negativação, declaro a inexigibilidade da dívida e condeno a empresa ré ao pagamento de R$ 8.000,00 a título de danos morais.',
        'A preliminar de decadência é acolhida, pois o autor reclamou do vício oculto após o prazo legal. JULGO IMPROCEDENTE a demanda.',
        'O mero atraso na entrega, sem maiores consequências, configura mero aborrecimento. Pedido de danos morais improcedente. Condeno apenas à entrega do produto.',
        'Não restou comprovada a falha na prestação do serviço, sendo as cobranças devidas. JULGO IMPROCEDente o pleito autoral.',
        'A inscrição indevida do nome do consumidor nos órgãos de proteção ao crédito gera dano moral in re ipsa. Condeno a ré em R$ 12.000,00.',
        'A cobrança foi devidamente informada no momento da contratação. JULGO PROCEDENTE o pedido de devolução simples, afastando os danos morais.',
        'O fornecedor não sanou o vício no prazo legal. Conforme o Art. 18 do CDC, determino a restituição imediata da quantia paga. Danos morais procedentes, fixados em R$ 4.000,00.',
        'Apesar do atraso, o produto foi entregue e não se demonstrou prejuízo excepcional. JULGO IMPROCEDENTE o pedido de danos morais.',
        'A informação sobre a taxa foi clara e expressa no ato da contratação. Improcedente.',
        'Restou configurada a falha na prestação do serviço, com cobranças por mais de 3 meses. Condeno a ré a restituir em dobro os valores e a pagar R$ 6.000,00 por danos morais.',
        'A ré não apresentou prova da origem da dívida que gerou a negativação. Declaro a inexigibilidade do débito e condeno a ré em danos morais de R$ 7.500,00.'
    ] * 10
}

df = pd.DataFrame(data)

# Criar o diretório se não existir
if not os.path.exists('data'):
    os.makedirs('data')

# Salvar o arquivo CSV
file_path = os.path.join('data', 'jurisprudencia.csv')
df.to_csv(file_path, index=False)

print(f"Dataset sintético criado em '{file_path}' com {len(df)} registros.")
