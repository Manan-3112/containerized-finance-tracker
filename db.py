cat > app/wait-for-db.py << 'EOF'
import psycopg2
import time
import os
import sys

max_retries = 30
retry_interval = 2

for i in range(max_retries):
    try:
        conn = psycopg2.connect(
            host=os.environ.get('DB_HOST', 'db'),
            database=os.environ.get('DB_NAME', 'financedb'),
            user=os.environ.get('DB_USER', 'financeuser'),
            password=os.environ.get('DB_PASSWORD', 'financepass')
        )
        conn.close()
        print("Database is ready!")
        sys.exit(0)
    except psycopg2.OperationalError:
        print(f"Waiting for database... ({i+1}/{max_retries})")
        time.sleep(retry_interval)

print("Could not connect to database!")
sys.exit(1)
EOF
