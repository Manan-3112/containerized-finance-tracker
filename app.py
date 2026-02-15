cat > app/app.py << 'EOF'
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import os
from datetime import datetime

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'db'),
        database=os.environ.get('DB_NAME', 'financedb'),
        user=os.environ.get('DB_USER', 'financeuser'),
        password=os.environ.get('DB_PASSWORD', 'financepass')
    )
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id SERIAL PRIMARY KEY,
            date DATE NOT NULL,
            category VARCHAR(100) NOT NULL,
            description TEXT,
            amount DECIMAL(10, 2) NOT NULL,
            type VARCHAR(10) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM transactions ORDER BY date DESC, created_at DESC')
    transactions = cur.fetchall()
    
    cur.execute("SELECT SUM(amount) FROM transactions WHERE type='income'")
    total_income = cur.fetchone()[0] or 0
    
    cur.execute("SELECT SUM(amount) FROM transactions WHERE type='expense'")
    total_expense = cur.fetchone()[0] or 0
    
    balance = total_income - total_expense
    
    cur.close()
    conn.close()
    
    return render_template('index.html', 
                         transactions=transactions,
                         total_income=total_income,
                         total_expense=total_expense,
                         balance=balance)

@app.route('/add', methods=['POST'])
def add_transaction():
    date = request.form['date']
    category = request.form['category']
    description = request.form['description']
    amount = float(request.form['amount'])
    trans_type = request.form['type']
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO transactions (date, category, description, amount, type) VALUES (%s, %s, %s, %s, %s)',
        (date, category, description, amount, trans_type)
    )
    conn.commit()
    cur.close()
    conn.close()
    
    flash('Transaction added successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_transaction(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM transactions WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    
    flash('Transaction deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
EOF
