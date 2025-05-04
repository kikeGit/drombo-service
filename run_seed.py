import psycopg2

def run_seed():

    from app import create_app, db

    # Create a Flask application
    app = create_app()

    # Create all the tables
    with app.app_context():
        db.create_all()

    print("Tables created successfully!")

    conn = psycopg2.connect(
        dbname="drombo", user="postgres", password="postgres", host="localhost", port="5432"
    )
    cursor = conn.cursor()

    with open('seed.sql', 'r') as file:
        sql = file.read()
    
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    run_seed()