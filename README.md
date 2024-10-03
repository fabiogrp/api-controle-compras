# api-controle-compras
Repositório da API do App Controle de Compras versão web
Utiliza uma base de dados SQLite.

Na versão atual existe apenas as funcionalidades de inserção e consulta dos dados

## Essa API é consumida por uma interface web que está no repositório

https://github.com/fabiogrp/gui-controle-compras

## Pra executar a API é necessário ter o uvicorn instalado
main-fastapi-compras:app
A API vai subir na porta 8000

## Obs
O peewee está como dependência porquê pretendia (ainda pretendo) utilizar esse ORM na aplicação, mas pode ser removido o import porquê atualmente não está sendo usado

