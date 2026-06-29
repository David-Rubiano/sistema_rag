import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# ==========================================
# 1. Metaclase para el Patrón Singleton
# ==========================================
class SingletonMeta(type):
    """
    Esta metaclase asegura que solo se cree una instancia de la clase que la utilice.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            # Si no existe, creamos la instancia y la guardamos
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

# ==========================================
# 2. Gestor de la Base de Datos Vectorial
# ==========================================
class VectorDBManager(metaclass=SingletonMeta):
    def __init__(self):
        print("Inicializando VectorDBManager y cargando modelo de Embeddings...")
        # Usamos un modelo open source ligero y gratuito
        self.embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.persist_directory = os.path.join(os.getcwd(), "data", "chroma_db")
        self.vector_store = None
        
        # Si ya existe una base de datos, la cargamos inmediatamente
        if os.path.exists(self.persist_directory) and os.listdir(self.persist_directory):
            self.load_existing_db()

    def load_existing_db(self):
        """Carga la base de datos vectorial existente desde el disco."""
        self.vector_store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_model
        )
        print("Base de datos vectorial cargada exitosamente desde disco.")

    def build_and_index(self, data_dir: str, chunk_size: int = 1000, chunk_overlap: int = 200):
        """Lee los .txt, los divide en chunks y los indexa en ChromaDB."""
        print(f"Cargando documentos desde {data_dir}...")
        
        # 1. Cargar documentos
        loader = DirectoryLoader(data_dir, glob="*.txt", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
        documents = loader.load()
        
        if not documents:
            print("No se encontraron documentos de texto para indexar.")
            return

        # 2. Dividir en chunks (estrategia de partición)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        chunks = text_splitter.split_documents(documents)
        print(f"Se crearon {len(chunks)} chunks a partir de {len(documents)} documentos.")

        # 3. Indexar en ChromaDB y persistir en disco
        print("Vectorizando e indexando en ChromaDB... (esto puede tardar unos segundos)")
        self.vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embedding_model,
            persist_directory=self.persist_directory
        )
        print("¡Indexación completada y guardada en disco!")

    def search(self, query: str, k: int = 3):
        """Realiza una búsqueda de similitud en la base de datos."""
        if not self.vector_store:
            raise ValueError("La base de datos vectorial no ha sido inicializada. Llama a build_and_index() primero.")
        
        # Retorna los k fragmentos más relevantes
        return self.vector_store.similarity_search(query, k=k)