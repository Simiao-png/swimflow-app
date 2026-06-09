# 🏊 SwimFlow

Sistema web para gerenciamento e acompanhamento de treinos de natação desenvolvido com Python, Flask e MySQL.

O SwimFlow nasceu de uma necessidade real durante os treinos de natação. Diferentemente da corrida e do ciclismo, onde o GPS registra automaticamente as atividades, o ambiente da piscina dificulta a coleta precisa dos dados pelo relógio esportivo. Além disso, encontrar aplicativos simples e eficientes para registrar a evolução dos treinos de natação mostrou-se uma tarefa difícil.

Diante desse problema, surgiu a ideia de desenvolver uma plataforma própria para registrar, organizar e acompanhar treinos de natação, permitindo ao atleta manter um histórico detalhado de sua evolução e exportar os treinos para plataformas esportivas compatíveis.

---

## 🌐 Demonstração Online

Acesse a versão publicada do projeto:

**https://swimflow.pythonanywhere.com**

> Aplicação disponível para testes diretamente pelo navegador, sem necessidade de instalação.

---

## 🚀 Destaques

* Sistema completo de autenticação de usuários
* Dashboard com métricas de desempenho
* Calendário para planejamento de treinos
* Histórico completo de atividades
* Exportação de treinos em formato TCX
* Compatível com Garmin Connect
* Aplicativo instalável via PWA
* Interface responsiva para desktop e dispositivos móveis
* Banco de dados MySQL

---

## 📷 Capturas de Tela

### 🏠 Tela Inicial

![Tela Inicial](docs/tela_inicial.png)

### 📅 Calendário de Treinos

![Calendário](docs/calendario.png)

### 👤 Perfil do Usuário

![Perfil](docs/perfil.png)

### 📊 Dashboard e Histórico

![Home](docs/home.png)

---

## ✨ Funcionalidades

### 👤 Usuários

* Cadastro de usuários
* Login seguro com senha criptografada
* Recuperação de senha
* Perfil personalizado
* Nome de exibição
* Registro de idade, peso e altura

### 🏊 Treinos

* Cadastro de treinos
* Edição de treinos
* Exclusão de treinos
* Histórico completo
* Programação de treinos futuros
* Treinos modelo reutilizáveis
* Marcação de treinos realizados
* Cálculo automático de distância
* Cálculo automático de pace

### 📅 Calendário

* Visualização mensal dos treinos
* Planejamento de sessões futuras
* Reagendamento de treinos
* Organização visual dos treinos programados

### 📊 Dashboard

* Total de treinos realizados
* Distância total nadada
* Tempo total de treino
* Histórico detalhado de atividades

### 📤 Exportação

* Exportação em formato TCX
* Compatível com Garmin Connect e outras plataformas esportivas

### 📱 Progressive Web App (PWA)

* Instalação em celulares Android
* Instalação em computadores
* Experiência semelhante a aplicativo nativo

---

## 🛠️ Tecnologias Utilizadas

* Python
* Flask
* MySQL
* HTML5
* CSS3
* JavaScript
* Progressive Web App (PWA)

---

## 📂 Estrutura do Projeto

```text
swimflow-app/
│
├── app.py
├── database/
├── modelos/
├── static/
├── templates/
├── docs/
├── requirements.txt
├── manifest.json
└── service-worker.js
```

---

## 🚀 Como Executar Localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/Simiao-png/swimflow-app.git
```

### 2. Acessar a pasta

```bash
cd swimflow-app
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar o banco de dados

Crie um banco MySQL e ajuste as configurações de conexão em:

```text
database/connection.py
```

### 5. Executar a aplicação

```bash
python app.py
```

---

## 🎯 Próximas Melhorias

* Cálculo estimado de calorias gastas
* Cálculo de IMC
* Evolução de peso do atleta
* Relatórios avançados
* Dashboard com gráficos
* Estatísticas por período
* Integração direta com dispositivos esportivos

---

## 📌 Objetivo do Projeto

O objetivo do SwimFlow é fornecer uma ferramenta simples e eficiente para que nadadores possam registrar, organizar e acompanhar sua evolução nos treinos, especialmente em situações onde dispositivos GPS e aplicativos convencionais não atendem adequadamente às necessidades da modalidade.

Além da utilização prática, o projeto também representa a aplicação de conhecimentos em Python, Flask, Banco de Dados MySQL, desenvolvimento web e Progressive Web Apps (PWA).

---

## 👨‍💻 Autor

**Silas Simião**

Professor de Matemática, triatleta e desenvolvedor em formação, utilizando tecnologia para solucionar problemas reais encontrados no esporte e na educação.
