# Drombo Backend

Backend del proyecto **Drombo**, una propuesta académica orientada a la planificación y gestión de traslados médicos mediante drones.  
Forma parte de la tesis de grado desarrollada en la Facultad de Ingeniería de la Universidad de la República (UdelaR).

---

## 📖 Descripción

El backend provee la **lógica de negocio** y las **APIs REST** necesarias para gestionar el sistema de traslados médicos con drones.  
Incluye los algoritmos de optimización y la heurística encargadas de calcular rutas eficientes para la distribución de insumos médicos.

Se comunica con el **frontend** [drombo-front](https://github.com/mbartesaghi/drombo-front) para entregar información procesada y coordinar las simulaciones.

---

## ✨ Características

- 🛠️ **API RESTful** para gestión de solicitudes de traslados y rutas.  
- 📊 **Algoritmos de optimización** aplicados al problema de ruteo de vehículos (VRP).  
- 🔄 Comunicación directa con el frontend para visualización de resultados.  
- 🧩 Arquitectura modular para facilitar mantenimiento y escalabilidad.  
- 🗄️ Persistencia de datos con base de datos relacional.  

---

## 🛠️ Tecnologías utilizadas

- [Python 3](https://www.python.org/)  
- [Flask](https://flask.palletsprojects.com/)  
- [PostgreSQL](https://www.postgresql.org/)  
- [PgAdmin4](https://www.pgadmin.org/)  
- [Docker](https://www.docker.com/) + [Docker Compose](https://docs.docker.com/compose/) 

1. **Clonar el repositorio**

```bash
git clone git@github.com:kikeGit/drombo-service.git
cd drombo-service
```

2. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

3. **Levantar base de datos con Docker**

```bash
docker-compose up -d
```

Esto descargará e inicializará las imágenes `postgres:15` y `dpage/pgadmin4`.  

4. **Conectarse a PgAdmin**  
   - Ir a: [http://localhost:5050](http://localhost:5050)  
   - Usuario: `admin@admin.com`  
   - Password: `admin`  

5. **Crear base de datos**  
   - Crear una nueva base de datos llamada `drombo` (configuración por defecto).  
   - Quedará accesible en `localhost:5432`.

6. **Configurar variables de entorno**  
   Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:  

```env
DATABASE_URL=postgresql://username:password@localhost:5432/drombo
```

*(Reemplazar `username` y `password` por tus credenciales de PostgreSQL)*

7. **Ejecutar la aplicación**

```bash
python run.py
```

El backend quedará disponible en:  
👉 `http://localhost:5000`

---

## 👩‍🎓 Autores

- [Mariana Bartesaghi](https://github.com/mbartesaghi)  
- [Enrique Castro](https://github.com/kikeGit)  

---

## 📚 Referencia académica

Este proyecto forma parte de la tesis:  
> *"DROMBÓ: Optimización de logística sanitaria de traslados de hasta 3Kg en drones de largo alcance para policlínicas periféricas en el departamento de Tacuarembó."*  
Universidad de la República – Facultad de Ingeniería, 2025.

