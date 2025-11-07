from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Inicialização da aplicação Flask
app = Flask(__name__)

# Habilita CORS para permitir requisições do frontend
# Necessário para comunicação entre containers Docker
CORS(app)

# Configuração do banco de dados RDS
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'database': os.getenv('DB_NAME', 'candy_shop_db'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', '')
}

# Função para conectar ao banco de dados
def get_db_connection():
    """Estabelece conexão com o banco de dados MySQL"""
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None


@app.route('/health')
def health_check():
    """Endpoint de verificação de saúde"""
    conn = get_db_connection()
    db_status = "connected" if conn else "disconnected"
    if conn:
        conn.close()
    
    return jsonify({
        "status": "healthy",
        "service": "Candy Shop API",
        "database": db_status,
        "timestamp": datetime.now().isoformat()
    })


@app.route('/products')
def get_products():
    """Rota direta: SELECT * FROM products"""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        
        # Converter Decimal para float
        for p in products:
            p['price'] = float(p['price'])
        
        cursor.close()
        conn.close()
        
        return jsonify(products)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/products')
def get_all_products():
    """Retorna todos os produtos disponíveis do banco de dados"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Erro na conexão com o banco de dados"}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        
        # Converter Decimal para float para JSON
        for product in products:
            product['price'] = float(product['price'])
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "products": products,
            "total": len(products)
        })
    except Error as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/products/lowstock')
def get_lowstock_products():
    """Retorna produtos com estoque baixo"""
    threshold = int(request.args.get('threshold', 10))
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Erro na conexão com o banco de dados"}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products WHERE stock <= %s", (threshold,))
        products = cursor.fetchall()
        
        # Converter Decimal para float
        for product in products:
            product['price'] = float(product['price'])
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "products": products,
            "count": len(products),
            "threshold": threshold
        })
    except Error as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/orders', methods=['POST'])
def create_order():
    """Cria um novo pedido no banco de dados"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Erro na conexão com o banco de dados"}), 500
    
    try:
        data = request.get_json()
        
        if not data or 'items' not in data:
            conn.close()
            return jsonify({"error": "Items são obrigatórios"}), 400
            
        items = data['items']
        customer = data.get('customer', {})
        
        cursor = conn.cursor(dictionary=True)
        
        # Validar items e calcular total
        order_items = []
        total = 0
        
        for item in items:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 1)
            
            # Encontrar produto no banco
            cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            product = cursor.fetchone()
            
            if not product:
                cursor.close()
                conn.close()
                return jsonify({"error": f"Produto {product_id} não encontrado"}), 404
                
            # Verificar estoque
            if product['stock'] < quantity:
                cursor.close()
                conn.close()
                return jsonify({"error": f"Estoque insuficiente para {product['name']}"}), 400
            
            # Calcular subtotal
            price = float(product['price'])
            subtotal = price * quantity
            total += subtotal
            
            order_items.append({
                "product_id": product_id,
                "product_name": product['name'],
                "quantity": quantity,
                "unit_price": price,
                "subtotal": subtotal
            })
            
            # Reduzir estoque no banco
            cursor.execute(
                "UPDATE products SET stock = stock - %s WHERE id = %s",
                (quantity, product_id)
            )
        
        # Criar pedido no banco
        cursor.execute(
            """INSERT INTO orders (customer_name, customer_email, customer_phone, total, status) 
               VALUES (%s, %s, %s, %s, 'pending')""",
            (customer.get('name'), customer.get('email'), customer.get('phone'), total)
        )
        order_id = cursor.lastrowid
        
        # Inserir itens do pedido
        for item in order_items:
            cursor.execute(
                """INSERT INTO order_items (order_id, product_id, product_name, quantity, unit_price, subtotal)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (order_id, item['product_id'], item['product_name'], 
                 item['quantity'], item['unit_price'], item['subtotal'])
            )
        
        # Commit das transações
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            "success": True,
            "order": {
                "id": order_id,
                "customer": customer,
                "items": order_items,
                "total": round(total, 2),
                "created_at": datetime.now().isoformat()
            }
        })
        
    except Error as e:
        if conn:
            conn.rollback()
            conn.close()
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("Iniciando API da Loja de Doces")
    print(f"Conectando ao banco: {db_config['host']}/{db_config['database']}")
    print("Rodando na porta 8080")
    app.run(host='0.0.0.0', port=8080, debug=True)
