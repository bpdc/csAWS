<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=2980B9&height=200&section=header&text=Candy%20Shop%20Cloud&fontSize=50&fontColor=fff&animation=twinkling&fontAlignY=40&desc=AWS%20|%20Docker%20|%20Flask%20|%20RDS%20|%20Lambda%20|%20API%20Gateway&descAlignY=60&descSize=18">

<p align="center">
  <i>🍰 Uma aplicação web completa para gerenciar loja de doces, implantada em nuvem AWS com arquitetura serverless e containerizada.</i>
</p>

***

### 📚 Projeto Acadêmico

<div align="center">

**Disciplina:** Serviços em Nuvem  
**Objetivo:** Implementação completa de aplicação web com Docker, AWS EC2, RDS MySQL, Lambda e API Gateway

</div>

### 🌟 Funcionalidades

<div align="center">

| Feature | Descrição |
|:---:|:---|
| 🍰 | Catálogo de Produtos (Doces e Tortas) |
| 🛒 | Sistema de Pedidos Completo |
| 📊 | Relatórios e Estatísticas via Lambda |
| 🌐 | API RESTful Completa |
| 🐳 | Containerização com Docker |
| ☁️ | Deploy AWS EC2 + RDS + Lambda |
| 🔒 | Banco de Dados MySQL Privado |
| 🛡️ | Segurança VPC e Security Groups |
| 📈 | Gerenciamento de Estoque |
| 💰 | Controle de Valores e Vendas |

</div>

### 🛠️ Tecnologias

<div align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=python,flask,docker,aws,mysql,html,css,js&theme=dark" />
  </a>
</div>

### 🏗️ Arquitetura

```
┌─────────────────┐
│   API Gateway   │ ← Endpoint público HTTPS
└────────┬────────┘
         │
    ┌────┴────────────────────┐
    │                         │
    ▼                         ▼
┌────────┐              ┌──────────┐
│  EC2   │              │  Lambda  │
│ Docker │              │  Report  │
│ Flask  │              └────┬─────┘
│ :8080  │                   │
└───┬────┘                   │
    │                        │
    │ HTTP ◄─────────────────┘
    │
    ▼
┌─────────┐
│   RDS   │
│  MySQL  │
│ Privado │
└─────────┘
```

***

### 📋 Requisitos Implementados

- ✅ API Flask completa para gerenciamento de produtos
- ✅ Sistema de pedidos com itens e totais
- ✅ Banco de dados RDS MySQL privado
- ✅ 3 tabelas relacionadas (products, orders, order_items)
- ✅ Containerização completa com Docker
- ✅ EC2 com aplicação Flask na porta 8080
- ✅ Função Lambda para relatórios estatísticos
- ✅ API Gateway integrando Lambda e EC2
- ✅ Security Groups configurados corretamente
- ✅ VPC com subnets públicas e privadas
- ✅ Variáveis de ambiente via arquivo .env
- ✅ Endpoints REST completos (GET, POST, PUT, DELETE)

***

### 🚀 Começando

#### Desenvolvimento Local

```bash
# Clone o projeto
git clone https://github.com/SEU_USUARIO/CandyShopAWS.git
cd CandyShopAWS

# Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas credenciais

# Suba os serviços localmente
docker-compose up --build

# Acesse no navegador:
# API: http://localhost:8080/products
# Health Check: http://localhost:8080/health
```

#### Deploy AWS

**1. Criar RDS MySQL:**
```bash
# Via Console AWS:
# - MySQL 8.0
# - db.t3.micro (Free Tier)
# - Acesso privado (sem IP público)
# - Nome do banco: candy_shop_db
# - Anote o endpoint do RDS
```

**2. Configurar EC2:**
```bash
# Conectar via SSH
ssh -i "candyshop-key.pem" ec2-user@SEU-IP-EC2

# Instalar Docker
sudo yum update -y
sudo yum install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user

# Clone e configure
git clone https://github.com/SEU_USUARIO/CandyShopAWS.git
cd CandyShopAWS

# Criar arquivo .env
nano .env
# Adicionar:
# DB_HOST=seu-endpoint-rds.amazonaws.com
# DB_PORT=3306
# DB_USER=admin
# DB_PASSWORD=sua-senha
# DB_NAME=candy_shop_db

# Build e run
docker build -t cs-img .
docker run -d --name tasks-api --restart unless-stopped \
  -p 8080:8080 --env-file .env cs-img
```

**3. Configurar Lambda:**
```python
# Criar função candyshop-report
# Runtime: Python 3.9
# Variável de ambiente: API_URL=http://SEU-IP-EC2:8080/api/products
# Timeout: 30 segundos
# Código: ver Guia de Implantação
```

**4. Configurar API Gateway:**
```bash
# Criar API REST: CandyShopAPI
# Recursos: /products, /orders, /report
# Métodos: GET, POST conforme necessário
# Integrar /report com Lambda
# Deploy em estágio 'prod'
```

***

### 📁 Estrutura do Projeto

```
CandyShopAWS/
├── app.py                  # Aplicação Flask principal
├── requirements.txt        # Dependências Python
├── Dockerfile             # Container Docker
├── .env.example           # Exemplo de variáveis
├── lambda_function.py     # Código da função Lambda
├── docker-compose.yml     # Desenvolvimento local
├── docs/
│   └── Guia-Implantacao-AWS.md
└── README.md
```

***

### 💾 Modelo de Dados

**Tabela: products**
```sql
- id (INT, PK, AUTO_INCREMENT)
- name (VARCHAR 200)
- category (ENUM: 'doce', 'torta')
- flavor (VARCHAR 100)
- price (DECIMAL 10,2)
- stock (INT)
- created_at, updated_at (TIMESTAMP)
```

**Tabela: orders**
```sql
- id (INT, PK, AUTO_INCREMENT)
- customer_name, customer_email, customer_phone
- total (DECIMAL 10,2)
- status (ENUM: 'pending', 'processing', 'completed', 'cancelled')
- created_at, updated_at (TIMESTAMP)
```

**Tabela: order_items**
```sql
- id (INT, PK, AUTO_INCREMENT)
- order_id (FK → orders)
- product_id (FK → products)
- product_name, quantity, unit_price, subtotal
- created_at (TIMESTAMP)
```

***

### 📊 Endpoints da API

#### EC2 Backend (Flask)

| Método | Endpoint | Descrição |
|:------:|:---------|:----------|
| GET | `/health` | Health check da aplicação |
| GET | `/products` | Lista todos os produtos (array) |
| GET | `/api/products` | Lista produtos com metadados |
| GET | `/api/products/lowstock` | Produtos com estoque baixo |
| POST | `/api/orders` | Cria novo pedido |

#### API Gateway (Público)

| Método | Endpoint | Descrição | Integração |
|:------:|:---------|:----------|:-----------|
| GET | `/products` | Lista produtos | EC2 HTTP |
| POST | `/orders` | Cria pedido | EC2 HTTP |
| GET | `/report` | Relatório estatístico | Lambda |

***

### 🔍 Exemplos de Uso

**Listar produtos:**
```bash
curl http://SEU-IP-EC2:8080/products
```

**Criar pedido:**
```bash
curl -X POST http://SEU-IP-EC2:8080/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer": {
      "name": "João Silva",
      "email": "joao@email.com",
      "phone": "(11) 98765-4321"
    },
    "items": [
      {"product_id": 1, "quantity": 5},
      {"product_id": 3, "quantity": 1}
    ]
  }'
```

**Relatório Lambda:**
```bash
curl https://xxxxxx.execute-api.us-east-1.amazonaws.com/prod/report
```

**Resposta esperada do /report:**
```json
{
  "success": true,
  "report": {
    "total_products": 8,
    "by_category": {"doce": 5, "torta": 3},
    "by_flavor": {"chocolate": 3, "coco": 2, "morango": 1},
    "low_stock_count": 2,
    "low_stock_products": [
      {"id": 4, "name": "Torta de Morango", "stock": 3},
      {"id": 7, "name": "Torta de Limão", "stock": 2}
    ],
    "total_inventory_value": 1234.50
  }
}
```

***

### ☁️ Infraestrutura AWS

**VPC e Rede:**
- VPC customizada com CIDR definido
- Subnet privada para RDS
- Subnet pública para EC2
- Internet Gateway para acesso público
- Route tables configuradas

**EC2:**
- Instância t2.micro (Free Tier)
- Amazon Linux 2
- Docker instalado
- Security Group permitindo:
  - SSH (22) - IP específico
  - HTTP (8080) - Público ou restrito

**RDS MySQL:**
- Instância db.t3.micro (Free Tier)
- MySQL 8.0
- Sem acesso público
- Security Group permitindo:
  - MySQL (3306) - Apenas do Security Group EC2

**Lambda:**
- Runtime Python 3.9
- 128 MB memória
- 30s timeout
- Variável API_URL configurada
- Permissões básicas de execução

**API Gateway:**
- API REST regional
- Integração HTTP com EC2
- Integração Lambda para /report
- CORS habilitado
- Estágio de produção (prod)

***

### 🛡️ Segurança

- ✅ RDS sem IP público (acesso apenas via EC2)
- ✅ Security Groups com regras mínimas necessárias
- ✅ Credenciais em arquivo .env (não versionado)
- ✅ SSH apenas por chave privada
- ✅ Lambda com IAM role específica
- ✅ API Gateway com throttling configurado
- ✅ Senhas fortes para RDS
- ✅ Backups automáticos do RDS habilitados

***

### 🎯 Objetivos de Aprendizado Alcançados

- [x] Containerização Docker para aplicações Python/Flask
- [x] Deploy e gerenciamento de aplicações em AWS EC2
- [x] Configuração de banco de dados RDS MySQL
- [x] Integração EC2 + RDS com Security Groups
- [x] Desenvolvimento de funções Lambda serverless
- [x] Configuração de API Gateway REST
- [x] Integração Lambda + API Gateway
- [x] Arquitetura híbrida (containers + serverless)
- [x] Gerenciamento de variáveis de ambiente
- [x] Implementação de API RESTful completa
- [x] Modelagem de dados relacional (3 tabelas)
- [x] Pipeline de deploy manual estruturado

***

### 📈 Monitoramento e Logs

**Docker Logs:**
```bash
docker logs -f tasks-api
```

**Lambda Logs (CloudWatch):**
```bash
aws logs tail /aws/lambda/candyshop-report --follow
```

**RDS Monitoring:**
- Enhanced Monitoring habilitado
- Métricas de CPU, memória, conexões
- Alarmes CloudWatch configuráveis

***

### 🔄 Atualização da Aplicação

```bash
# SSH na EC2
ssh -i "candyshop-key.pem" ec2-user@SEU-IP-EC2

# Atualizar código
cd CandyShopAWS
git pull origin main

# Reconstruir container
docker stop tasks-api
docker rm tasks-api
docker build -t cs-img .
docker run -d --name tasks-api --restart unless-stopped \
  -p 8080:8080 --env-file .env cs-img

# Verificar
docker logs tasks-api
curl http://localhost:8080/health
```

***

### 💰 Custos AWS (Free Tier)

| Serviço | Free Tier | Custo Estimado |
|:--------|:----------|:---------------|
| EC2 t2.micro | 750h/mês (12 meses) | $0 (dentro do limite) |
| RDS db.t3.micro | 750h/mês (12 meses) | $0 (dentro do limite) |
| Lambda | 1M req/mês (sempre) | $0 (baixo uso) |
| API Gateway | 1M req/mês (12 meses) | $0 (dentro do limite) |
| **Total** | - | **~$0/mês** (Free Tier) |

***

### 📖 Documentação Adicional

- [Guia Completo de Implantação AWS](docs/Guia-Implantacao-AWS.md)
- Passo a passo detalhado de toda infraestrutura
- Troubleshooting e solução de problemas
- Scripts de automação e manutenção

***

### 🚧 Melhorias Futuras

- [ ] Frontend web para visualização
- [ ] Autenticação e autorização (JWT)
- [ ] CI/CD com GitHub Actions
- [ ] Terraform para Infrastructure as Code
- [ ] Load Balancer para alta disponibilidade
- [ ] CloudWatch Dashboards personalizados
- [ ] Testes automatizados (pytest)
- [ ] Cache com Redis/ElastiCache

***

### 🐛 Solução de Problemas

**Container não inicia:**
```bash
docker logs tasks-api
# Verificar erro de conexão com RDS
# Verificar credenciais no .env
```

**Lambda timeout:**
```bash
# Verificar API_URL está correto
# Aumentar timeout para 30s
# Verificar Security Group permite acesso
```

**Erro 502 API Gateway:**
```bash
# IP público do EC2 pode ter mudado
# Atualizar URL de integração no API Gateway
# Re-deployar API
```

***

### 👤 Autor

<div align="center">
  <a href="https://github.com/SEU_USUARIO" target="_blank">
    <img src="https://skillicons.dev/icons?i=github" alt="GitHub"/>
  </a>
</div>

### 📜 Licença

Projeto sob licença MIT – veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

### 🙏 Agradecimentos

- Professores da disciplina Serviços em Nuvem
- Documentação oficial AWS
- Comunidade Docker e Flask

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=2980B9&height=120&section=footer"/>

</div>