# 🚗 PRF Acidentes - Engenharia de Dados

Projeto de Engenharia de Dados desenvolvido com dados públicos de acidentes rodoviários da Polícia Rodoviária Federal (PRF).

O projeto utiliza dados de ocorrências entre **2022 e 2026**, realizando etapas de extração, transformação, validação, armazenamento, análise com SQL e visualização em dashboard.

> ⚠️ Os dados de 2026 são parciais e não representam o ano completo.

---

## 🎯 Objetivo

O objetivo do projeto é construir um pipeline de dados capaz de:

- consolidar arquivos anuais da PRF;
- transformar os dados para um formato mais eficiente;
- validar a qualidade dos registros;
- armazenar os dados em um banco analítico;
- executar consultas SQL;
- gerar uma camada analítica;
- visualizar indicadores em um dashboard interativo.

---

## 🏗️ Arquitetura do projeto

O fluxo utilizado no projeto é:

```text
Arquivos CSV da PRF
        ↓
      Pandas
        ↓
Parquet consolidado
        ↓
 Transformação
        ↓
 Parquet limpo
        ↓
     DuckDB
        ↓
       SQL
        ↓
Camada Analytics
        ↓
    Streamlit
        ↓
Dashboard interativo