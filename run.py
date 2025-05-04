from app import create_app, db
from app import models  # <-- Use absolute import instead of relative

app = create_app()

# Crear tablas si no existen
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)