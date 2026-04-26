<div align="center">
<img src="src/nutri_app/static/images/logo_readme.png" alt="NutriCheck" width="100">

<h1>NutriCheck</h1>

<p>
    Sistema web responsivo voltado ao registro alimentar, que permite ao usuário acompanhar sua alimentação diária, ingestão de água e evolução de peso por meio de gráficos e indicadores nutricionais.
</p>
</div>

<br>

## ⚙️ Funcionalidades

- Cadastro e autenticação de usuários  
- Registro de refeições diárias  
- Cálculo automático de calorias e macronutrientes  
- Registro de ingestão de água  
- Acompanhamento de progresso de peso com gráfico  
- Integração com API de alimentos (busca por nome)  
- Recuperação de senha via e-mail *(limitada a ambiente de teste, devido à ausência de domínio próprio configurado)* 
- Edição de perfil do usuário  

## 🧱 Tecnologias utilizadas

### 🔹 Backend
- **Python** → linguagem principal da aplicação  
- **Flask** → criação de rotas, controle da aplicação e estrutura do backend  
- **JavaScript** → interatividade no frontend e comunicação assíncrona com o backend (AJAX)  

### 🔹 Frontend
- **HTML** → estrutura das páginas  
- **CSS** → estilização e responsividade  
- **Bootstrap** → layout responsivo e componentes visuais  

### 🔹 Banco de dados
- **MySQL** → armazenamento de usuários, refeições e registros  

## 🔧 Bibliotecas e ferramentas

### Backend / Dados
- **Flask-SQLAlchemy** → ORM para manipulação do banco de dados  
- **Flask-WTF** → criação e validação de formulários  
- **Flask-Login** → autenticação e gerenciamento de sessão  
- **Flask-Bcrypt / bcrypt** → criptografia de senhas  
- **itsdangerous** → geração de tokens seguros (reset de senha)  
- **python-dotenv** → gerenciamento de variáveis de ambiente  
- **PyMySQL** → conexão com banco MySQL  
- **email-validator** → validação de e-mails  
- **requests** → consumo de API externa  
- **Resend** → envio de e-mails transacionais *(limitado a ambiente de testes, pois não há domínio próprio configurado)*    

### Frontend / UX
- **Chart.js** → geração do gráfico de evolução de peso  
- **Flatpickr** → seleção de datas com calendário customizado  
- **Lucide Icons** → ícones na interface  
- **Fetch API (AJAX)** → requisições assíncronas sem recarregar a página  

### DevOps / Infraestrutura
- **Git** → versionamento de código  
- **Poetry** → gerenciamento de dependências e ambiente virtual  
- **Render** → deploy da aplicação  
- **Clever Cloud** → hospedagem do banco de dados MySQL  

## 🔌 Integrações externas

- **OpenFoodFacts API** → busca de alimentos e dados nutricionais  

## 🧠 Como cada tecnologia foi aplicada (resumo)

- **Flask** → estrutura da aplicação e gerenciamento de rotas  
- **SQLAlchemy** → persistência e manipulação de dados  
- **Bcrypt** → segurança no armazenamento de senhas  
- **Flask-Login** → controle de autenticação de usuários  
- **Resend** → envio de e-mails (recuperação de senha)  
- **Fetch/AJAX** → atualização dinâmica da interface sem reload  
- **Chart.js** → visualização gráfica da evolução de peso  
- **Flatpickr** → melhoria na entrada de datas  
- **Bootstrap** → padronização visual e responsividade  

## 📊 Diferenciais do projeto

- Interface totalmente responsiva  
- Integração com API externa de alimentos  
- Cálculo automático de calorias e macronutrientes  
- Envio de e-mail para recuperação de senha (limitado a ambiente de testes, pois não há domínio próprio configurado)  
- Atualização de dados sem reload (AJAX)  
- Visualização gráfica de evolução de peso  
- Estrutura modular organizada (boas práticas com Flask)  
- Uso de variáveis de ambiente para segurança  
- Deploy em ambiente real (Render + banco externo)  

## 📁 Estrutura do projeto

Estrutura baseada em arquitetura modular utilizando Flask (Blueprints), separando responsabilidades entre rotas, templates e regras de negócio.

```bash
NutriCheck/
├── src/
│   └── nutri_app/
│       ├── routes/              # Rotas da aplicação (controllers)
│       │   ├── login_routes.py
│       │   ├── auth_routes.py
│       │   ├── home_routes.py
│       │   ├── perfil_routes.py
│       │   ├── alimentos_routes.py
│       │   ├── refeicoes_routes.py
│       │   ├── agua_routes.py
│       │   └── progressao_routes.py
│       │
│       ├── templates/           # Templates HTML (Jinja2)
│       │   ├── pages/           # Páginas principais
│       │   ├── includes/        # Componentes reutilizáveis 
│       │   ├── modals/          # Modais da aplicação
│       │   └── emails/          # Templates de e-mail
│       │
│       ├── static/              # Arquivos estáticos
│       │   ├── css/
│       │   │   ├── pages/       # CSS específico por página
│       │   │   ├── base.css
│       │   │   ├── layout.css
│       │   │   ├── components.css
│       │   │   └── utils.css
│       │   ├── js/              # Scripts JavaScript (fetch/AJAX)
│       │   ├── images/          # Imagens do sistema
│       │   └── icons/           # Favicons e ícones
│       │
│       ├── forms/               # Formulários (Flask-WTF)
│       │
│       ├── utils/               # Regras de negócio e utilidades
│       │   ├── email_service.py     # Envio de e-mails
│       │   ├── macros.py            # Cálculo de calorias/macronutrientes
│       │   ├── api_openfoodfacts.py # Integração com API externa
│       │   ├── token.py             # Geração de tokens (reset senha)
│       │   ├── static_utils.py      # Versionamento de arquivos estáticos
│       │   ├── hash.py              # Criptografia de senha
│       │   └── decorators.py        # Decoradores personalizados
│       │
│       ├── database.py          # Configuração do banco de dados
│       ├── user_login.py        # Lógica de autenticação do usuário
│       └── __init__.py          # Factory do Flask (create_app)
│
└── run.py                       # Ponto de entrada da aplicação
```

## 🌐 Acessar a aplicação em produção

👉 https://nutri-check-nw20.onrender.com

## 💻 Como rodar a aplicação localmente

```bash
# clonar o repositório
git clone https://github.com/ProjetosDevVviniciws/NutriCheck.git

# acessar a pasta
cd NutriCheck

# instalar dependências
poetry install

# criar arquivo de ambiente
cp .env.example .env   # Linux / Mac / Git Bash
# ou
copy .env.example .env # Windows (CMD)
# ou
Copy-Item .env.example .env # Windows (PowerShell)

# configurar variáveis de ambiente
# (edite o arquivo .env com suas credenciais antes de rodar)

# ativar ambiente virtual
poetry shell

# rodar aplicação
python run.py
```

## 🚀 Considerações finais

O **NutriCheck** foi desenvolvido com foco em aprendizado prático e aplicação de conceitos modernos de desenvolvimento web, integrando backend, frontend, banco de dados e serviços externos em um único sistema funcional.

Este projeto demonstra habilidades em:

- Desenvolvimento full stack  
- Integração com API externa  
- Boas práticas de organização de código  
- Deploy e configuração de ambiente de produção