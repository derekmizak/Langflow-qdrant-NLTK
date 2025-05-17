### README.md  

# LangFlow + Qdrant Dockerized Setup

This repository provides a Dockerized environment for running LangFlow alongside Qdrant, a high-performance vector database. The setup ensures data persistence, NLP support, and efficient container orchestration.

## 📌 Features

- **LangFlow**: A tool for managing and visualizing LLM pipelines.
- **Qdrant**: A vector search database for efficient similarity search.
- **PostgreSQL**: Database for LangFlow running on non-standard port 5433 to avoid conflicts.
- **Persistent Storage**: Ensures data across container restarts.
- **Preloaded NLTK Data**: Mounted for use in NLP-related operations.

## 🚀 Getting Started

### 1️⃣ Prerequisites

Ensure you have the following installed:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### 2️⃣ Clone the Repository

```bash
git clone [<repository-url>](https://github.com/derekmizak/Langflow-qdrant-NLTK.git)
cd Langflow-qdrant-NLTK
```

### 3️⃣ Build & Start the Containers

Run the following command to build and start LangFlow and Qdrant:

```bash
docker-compose up -d --build
```

This will:
- Build the LangFlow image using `Dockerfile_langflow`
- Start LangFlow (`langflow133`) on port **7860**
- Start Qdrant (`qdrant133`) on ports **6333** and **6334**

### 4️⃣ Access the Services

- **LangFlow UI**: Open [http://localhost:7860](http://localhost:7860)  
- **Qdrant API**: Available at `http://localhost:6333/dashboard`
- **PostgreSQL**: Available at `localhost:5433` (non-standard port to avoid conflicts with existing PostgreSQL instances)
  - Username: langflow
  - Password: langflow
  - Database: langflow

## 📂 Mounted Volumes

All data is stored in local directories within the project folder:

| Directory           | Description                                     |
|--------------------|-------------------------------------------------|
| `./langflow_data`   | LangFlow application data and configurations    |
| `./postgres_data`   | PostgreSQL database files                      |
| `./file_injest`     | Directory for file processing and document input|
| `./flow_output`     | Directory for storing output from LangFlow     |
| `./qdrant_storage`  | Persistent storage for Qdrant vector database  |
| `./nltk_data`       | NLTK data storage for NLP tasks                |

## 🛑 Stopping & Cleaning Up

To stop the containers without removing volumes:
```bash
docker-compose down
```

To remove all data and start fresh:
```bash
docker-compose down -v
```

## 📝 Environment Variables

| Variable | Description |
|----------|-------------|
| `LANGFLOW_DATABASE_URL` | PostgreSQL connection string (using non-standard port 5433 externally) |
| `LANGFLOW_SAVE_DB_IN_CONFIG_DIR` | Ensures LangFlow database is saved persistently |
| `NLTK_DATA` | Specifies the path for NLTK data storage |

## 🔄 Updating the Containers

To rebuild the containers after making changes:
```bash
docker-compose up -d --build
```

## 📖 Additional Notes

- Ensure `./file_injest` and `./nltk_data` exist before starting the containers.
- Qdrant is set to persist storage under `./qdrant_storage`.
- The `depends_on` directive ensures LangFlow starts only after Qdrant is ready.

---

### 📬 Need Help?
Feel free to raise an issue or contribute to the repository.

Happy Coding! 
Would you like any modifications or enhancements? 
Please let me know.