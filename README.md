# 🏊 SwimFlow

Sistema web para gerenciamento de treinos de natação desenvolvido com Python, Flask e MySQL.

O SwimFlow permite registrar, acompanhar e organizar treinos de natação, além de fornecer métricas e histórico individual para cada atleta.

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

### 📊 Dashboard

* Total de treinos realizados
* Distância total nadada
* Tempo total de treino
* Histórico detalhado

### 📅 Calendário

* Visualização dos treinos programados
* Organização semanal dos treinos

### 📱 Aplicativo Instalável

O SwimFlow pode ser instalado em dispositivos móveis e computadores através da tecnologia PWA (Progressive Web App).

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
natacao-app/
│
├── app.py
├── database/
├── modelos/
├── static/
├── templates/
├── manifest.json
└── service-worker.js
```

---

## 🚀 Como Executar

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
pip install flask mysql-connector-python werkzeug
```

### 4. Configurar o banco de dados

Criar um banco MySQL e ajustar as configurações de conexão no arquivo:

```text
database/connection.py
```

### 5. Executar

```bash
python app.py
```

---

## 🎯 Próximas Melhorias

* Cálculo estimado de calorias gastas
* Cálculo de IMC
* Evolução de peso do atleta
* Relatórios de desempenho
* Estatísticas avançadas

---

## 👨‍💻 Autor

Desenvolvido por Silas Simião.

Projeto criado com foco em aprendizado, organização de treinos e evolução contínua do desenvolvimento de software.
