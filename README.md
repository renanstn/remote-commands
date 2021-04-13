# remote-commands

## Descrição

Este app sobe um pequeno servidor Flask na sua máquina, e fica ouvindo por requisições vindas da rede local.

Essas requisições podem ativar algum atalho de teclado na sua máquina, ou executar algum comando shell previamente cadastrado.

Eu utilizo este app em conjunto com o app [HTTP Request Shortcuts](https://play.google.com/store/apps/details?id=ch.rmy.android.http_shortcuts&hl=en_US&gl=US) instalado em um celular. A partir dele envio as requests, e o celular funciona como um "controle remoto" que executa comandos no meu PC.

## Setup

- Clone o repositório
- Instale as dependência utilizando o `pipenv`
```sh
pipenv install
```
- Inicie o app com o comando
```sh
pipenv run python server/main.py
```
ou
```
./run.sh
```

## Cadastrando comandos

Em seu navegador, acesse `http://localhost:5000/admin` para ir a área de cadastro de comandos.

![Flask-admin](images/admin_print.png)

Cadastre quantos comandos quiser.

## Executando

### Executando atalhos

Para executar um atalho, envie uma requisição POST com o seguinte body JSON, a partir de qualquer dispositivo de sua rede local para:
- `http://<IP_da_sua_máquina>/shortcut`
```json
{
	"command": "<nome_do_atalho>"
}
```

### Executando comandos

Para executar os comandos, envie uma requisição GET de qualquer dispositivo de sua rede local para:
- `http://<IP_da_sua_máquina>/command/<index_do_comando>`
