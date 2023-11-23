# Captura e Análise de Dados do Setor Elétrico

Este repositório do GitHub contém um projeto desenvolvido para a captação e análise de dados do setor elétrico, especificamente dos órgãos ONS (Operador Nacional do Sistema Elétrico), CCEE (Câmara de Comercialização de Energia Elétrica) e ANEEL (Agência Nacional de Energia Elétrica). Os dados capturados são cruzados e tratados de forma a facilitar o uso em análises, com o objetivo de aplicar a Ciência de Dados na exploração do conhecimento dos dados abertos relacionados à comercialização de energia elétrica.

## Organização do Repositório

O repositório está organizado da seguinte forma:

- `01_dados/`: Esta pasta contém os dados capturados dos órgãos ONS, CCEE e ANEEL. Os arquivos são organizados em subpastas de acordo com a fonte e o período de captura para após serem tratados e concatenados.

- `02_notebooks/`: Esta pasta contém notebooks Jupyter com exemplos de análises e exploração dos dados capturados.

- `03_scripts/`: Nesta pasta estão os scripts desenvolvidos para a captação, atualização e tratamento dos dados. Os scripts estão organizados da seguinte maneira:

  - `01_scrapping/`: Nessa pasta estão os scripts de captura dos dados.

- `requirements.txt`: Arquivo que lista as dependências necessárias para executar o projeto.

- `README.md`: Este arquivo, fornecendo informações sobre o projeto, sua organização e instruções para uso.

- `04_utils/`: Nesta pasta estão ferramentas diversas úteis usadas no projeto:

## Uso do Projeto

Para utilizar este projeto, siga as etapas abaixo:

1. Clone o repositório para sua máquina local usando o seguinte comando: 
```git
git clone https://github.com/2023LabBITS-Dados/dados-seb.git
```

2. Certifique-se de ter as dependências necessárias instaladas. Você pode usar o `pip` para instalar as dependências listadas no arquivo `requirements.txt`. Execute o seguinte comando para instalá-las:
```python
pip install -r requirements.txt
```

3. Baixe o chromedriver compatível com a versão  seu navegador GoogleChrome e coloque na pasta `04_utils/driver/`

4. Altere a variável ```DOWNLOAD_PATH``` para o caminho de donwload da sua máquina para seu usuário nos seguintes scripts:
  - `03_scripts/01_scrapping/00_scrapping_ons.py`
  - `03_scripts/01_scrapping/01_update_ons_data.py`
  - `03_scripts/01_scrapping/05_scrapping_ccee.py`
  - `03_scripts/01_scrapping/06_scrapping_ccee.py`

OBS: O programa leva em consideração que não existe nenhum dados dessas instituições no seu diretório de Download, certifique-se de remover todos arquivos referentes a esse tema para evitar erros.

5. Execute os scripts em ordem de pasta seguindo e ordem de script, EX:
  - `03_scripts/01_scrapping/00_scrapping_ons.py`
  - `03_scripts/01_scrapping/01_update_ons_data.py`
  - `03_scripts/01_scrapping/02_merge_ons_data.py`
  - ...


