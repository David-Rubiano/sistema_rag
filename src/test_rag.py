import os
from dotenv import load_dotenv
from database.vector_db import VectorDBManager
from rag.llm_factory import RAGPipeline

# Cargar variables de entorno (GROQ_API_KEY, LLM_PROVIDER, MEMORY_WINDOW)
load_dotenv()

if __name__ == "__main__":
    print("Iniciando pruebas del sistema RAG con LangGraph...")
    
    # 1. Conectar a la base de datos vectorial (Singleton)
    db_manager = VectorDBManager()
    
    # 2. Leer configuración del .env
    provider = os.getenv("LLM_PROVIDER", "groq")
    
    # Manejo de error por si MEMORY_WINDOW está vacío en el .env
    try:
        n_mensajes = int(os.getenv("MEMORY_WINDOW", 5))
    except ValueError:
        n_mensajes = 5
    
    # 3. Inicializar el pipeline RAG
    rag = RAGPipeline(
        vector_store=db_manager.vector_store,
        llm_provider=provider,
        memory_window=n_mensajes
    )
    
    # 4. Simulación de chat en consola
    print("\n" + "="*50)
    print("🤖 CHATBOT DAVIbank INICIADO (Escribe 'salir' para terminar)")
    print("="*50)
    
    # Simulamos un usuario específico para probar la persistencia del ID
    session_usuario = "candidato_david_001"
    
    while True:
        pregunta = input("\nTú: ")
        if pregunta.lower() == 'salir':
            print("\nCerrando el chat. ¡Éxito con la prueba!")
            break
            
        # Ejecutamos la consulta pasando el ID de sesión
        respuesta = rag.ask(pregunta, session_id=session_usuario)
        
        print(f"\n🤖 DAVIbank Bot: {respuesta['answer']}")
        
        # Opcional: Imprimir las fuentes para verificar que el RAG está buscando bien
        if respuesta['sources']:
            print("\n[🔍 Fuentes consultadas:]")
            for i, fuente in enumerate(respuesta['sources'], 1):
                # Imprimimos solo los primeros 100 caracteres de cada chunk para no saturar la consola
                print(f"  {i}. {fuente[:100]}...")