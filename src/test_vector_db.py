import os
from database.vector_db import VectorDBManager

if __name__ == "__main__":
    clean_data_dir = os.path.join(os.getcwd(), "data", "clean")
    
    # 1. Instanciamos el Singleton (la primera vez cargará el modelo)
    db_manager = VectorDBManager()
    
    # 2. Verificamos que el Singleton funcione (debería ser la misma dirección de memoria)
    db_manager_2 = VectorDBManager()
    assert db_manager is db_manager_2, "El patrón Singleton falló"
    
    # 3. Construimos el índice leyendo la carpeta "clean"
    db_manager.build_and_index(data_dir=clean_data_dir)
    
    # 4. Probamos una búsqueda (cambia la pregunta según lo que hayas scrapeado)
    pregunta = "¿Cuáles son los beneficios de la tarjeta de crédito Cencosud?"
    print(f"\nRealizando búsqueda para: '{pregunta}'")
    
    resultados = db_manager.search(pregunta, k=2)
    for i, doc in enumerate(resultados):
        print(f"\n--- Resultado {i+1} ---")
        print(doc.page_content)