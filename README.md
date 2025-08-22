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

- [Node.js](https://nodejs.org/)  
- [Express](https://expressjs.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/) para despliegue y contenedores  

---

## 🚀 Instalación y uso

Clonar el repositorio:

```bash
git clone https://github.com/kikeGit/drombo-service.git
cd drombo-service
```

Instalar dependencias:

```bash
npm install
```

Levantar el servidor en desarrollo:

```bash
npm run dev
```

El backend quedará disponible en:  
👉 `http://localhost:3000` (puerto por defecto)

---

## 👩‍🎓 Autores

- [Mariana Bartesaghi](https://github.com/mbartesaghi)  
- [Enrique Castro](https://github.com/kikeGit)  

---

## 📚 Referencia académica

Este proyecto forma parte de la tesis:  
> *"DROMBÓ: Optimización de logística sanitaria de traslados de hasta 3Kg en drones de largo alcance para policlínicas periféricas en el departamento de Tacuarembó."*  
Universidad de la República – Facultad de Ingeniería, 2025.

