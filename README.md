# EXTRACTOR-CNPJ

Ferramenta em Python para consulta e extração de dados de CNPJs utilizando a API da Minha Receita.  
O script realiza coleta, filtragem e exportação de informações empresariais para arquivos JSONL e CSV.

---

## 🚀 Funcionalidades

- Consulta automática de CNPJs via API
- Extração de:
  - Razão Social
  - Nome Fantasia
  - CNAE
  - Endereço
  - CEP
  - Bairro
  - Município
  - Capital Social
  - Situação Cadastral
- Filtragem de campos específicos
- Conversão de JSONL para CSV
- Comparação de CNPJs entre arquivos
- Geração automática de:
  - `output.jsonl`
  - `filtered.jsonl`
  - `finalresult.csv`
  - `unmatched.txt`

---

## 📦 Requisitos

Instale as dependências:

```bash
pip install requests
```

---

## 📁 Estrutura dos Arquivos

```bash
input.txt          # Lista de CNPJs para consulta
numbers.txt        # Lista de comparação
output.jsonl       # Resultado bruto da API
filtered.jsonl     # Resultado filtrado
finalresult.csv    # Resultado final em CSV
unmatched.txt      # CNPJs não encontrados
```

---

## ▶️ Como usar

### 1. Adicione os CNPJs no arquivo:

```bash
input.txt
```

Exemplo:

```text
12345678000199
11222333000144
```

---

### 2. Execute o script

```bash
python extractor.py
```

---

## 📄 Dados Extraídos

O script coleta os seguintes campos:

```python
[
    "uf",
    "cep",
    "cnpj",
    "porte",
    "bairro",
    "numero",
    "municipio",
    "logradouro",
    "cnae_fiscal",
    "complemento",
    "razao_social",
    "nome_fantasia",
    "capital_social",
    "cnae_fiscal_descricao",
    "descricao_situacao_cadastral",
    "descricao_tipo_de_logradouro"
]
```

---

## 📊 Exportação CSV

O resultado final é salvo automaticamente em:

```bash
finalresult.csv
```

Compatível com:

- Excel
- Google Sheets
- LibreOffice

---

## 🌐 API Utilizada

```text
https://minhareceita.org/
```

---

## ⚠️ Aviso

Este projeto possui finalidade educacional e de automação de consultas públicas de CNPJ.

Respeite os limites da API utilizada.

---

## 👨‍💻 Autor

GitHub: https://github.com/NicolasSamuel0
