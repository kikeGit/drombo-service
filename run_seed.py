import psycopg2
from app import create_app, db
from sqlalchemy import text

def run_seed():
    # 1. Crear la app y contexto
    app = create_app()
    
    with app.app_context():
        print("⚠️  Dropping all existing tables...")
        db.drop_all()
        print("✅ Tables dropped.")

        print("📦 Creating all tables...")
        db.create_all()
        print("✅ Tables created.")

    # 2. Conectar a PostgreSQL
    conn = psycopg2.connect(
        dbname="drombo_2",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    # 3. Ejecutar seed.sql
    print("📥 Inserting seed data from seed.sql...")
    with open('seed.sql', 'r', encoding='utf-8') as file:
        sql = file.read()

    try:
        cursor.execute(sql)
        conn.commit()
        print("✅ Seed data inserted successfully.")
    except Exception as e:
        conn.rollback()
        print("❌ Error while inserting seed data:", e)
    finally:
        cursor.close()
        conn.close()
        print("🔚 Connection closed.")

if __name__ == "__main__":
    run_seed()