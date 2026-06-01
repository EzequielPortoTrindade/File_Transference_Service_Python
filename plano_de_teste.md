# Plano de Testes – Projeto Socket File Transfer

## 1. Objetivo

Este documento descreve o plano de testes do projeto de transferência de arquivos utilizando sockets TCP em Python. O objetivo é validar o funcionamento correto das funcionalidades implementadas no sistema cliente-servidor.

---

# 2. Ferramentas Utilizadas

| Ferramenta   | Finalidade                   |
| ------------ | ---------------------------- |
| Python 3.x   | Execução do sistema          |
| Git          | Controle de versão           |
| GitHub       | Hospedagem do repositório    |
| Terminal/CMD | Execução dos processos       |
| VS Code      | Desenvolvimento e testes     |
| Socket TCP   | Comunicação cliente-servidor |

---

# 3. Configurações do Ambiente

## Sistema Operacional

* Windows 10/11
* Compatível com Linux

## Requisitos

* Python 3 instalado
* Git instalado
* Conexão localhost habilitada
* Porta TCP 5050 livre

## Estrutura de Pastas

```text
projeto/
│
├── server.py
├── client.py
├── server_files/
└── client_files/
```

---

# 4. Restrições

* O sistema utiliza apenas comunicação local (`localhost`)
* Apenas arquivos simples são suportados
* Não há autenticação de usuários
* Não há criptografia de dados
* O servidor deve ser iniciado antes dos clientes

---

# 5. Procedimentos de Teste

## 5.1 Inicialização do Projeto

### Iniciar servidor

```bash
py server.py
```

### Iniciar cliente

```bash
py client.py
```

---

# 5.2 Procedimentos de Versionamento

## Commit

```bash
git add .
git commit -m "descrição da alteração"
```

## Push

```bash
git push
```

## Pull

```bash
git pull
```

## Pull Request

1. Criar branch de desenvolvimento
2. Realizar alterações
3. Enviar branch ao GitHub
4. Abrir Pull Request
5. Revisar e aprovar alterações
6. Realizar merge na branch principal

---

# 6. Casos de Teste

| ID    | Funcionalidade           | Descrição do Teste                       | Resultado Esperado             |
| ----- | ------------------------ | ---------------------------------------- | ------------------------------ |
| CT-01 | Conexão cliente-servidor | Cliente conectar ao servidor             | Conexão estabelecida           |
| CT-02 | Upload de arquivo        | Enviar arquivo do cliente ao servidor    | Arquivo salvo no servidor      |
| CT-03 | Download de arquivo      | Baixar arquivo do servidor               | Arquivo salvo no cliente       |
| CT-04 | Listagem de arquivos     | Solicitar arquivos do servidor           | Lista exibida corretamente     |
| CT-05 | Remoção de arquivo       | Excluir arquivo do servidor              | Arquivo removido               |
| CT-06 | Arquivo inexistente      | Solicitar arquivo inválido               | Mensagem de erro               |
| CT-07 | Múltiplos clientes       | Conectar vários clientes simultaneamente | Servidor atender todos         |
| CT-08 | Encerramento de conexão  | Cliente sair do sistema                  | Conexão encerrada corretamente |

---

# 7. Matriz de Funcionalidades x Testes

| Funcionalidade | CT-01 | CT-02 | CT-03 | CT-04 | CT-05 | CT-06 | CT-07 | CT-08 |
| -------------- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| Conexão TCP    | X     |       |       |       |       |       | X     | X     |
| Upload         |       | X     |       |       |       |       | X     |       |
| Download       |       |       | X     |       | X     | X     | X     |       |
| Listagem       |       |       |       | X     |       |       | X     |       |
| Remoção        |       |       |       |       | X     |       | X     |       |
| Concorrência   |       |       |       |       |       |       | X     |       |
| Encerramento   |       |       |       |       |       |       |       | X     |

---

# 8. Critérios de Sucesso

O sistema será considerado aprovado caso:

* Todos os testes executem sem falhas críticas
* O servidor suporte múltiplos clientes
* Upload e download ocorram corretamente
* Não ocorram perdas de arquivos
* As conexões sejam encerradas corretamente

---

# 9. Possíveis Melhorias Futuras

* Autenticação de usuários
* Criptografia TLS/SSL
* Interface gráfica
* Logs de auditoria
* Transferência de diretórios
* Barra de progresso
* Compressão de arquivos

---

# 10. Responsável

Projeto desenvolvido para fins acadêmicos utilizando Python e sockets TCP.
