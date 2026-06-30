import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

# --- Importaciones Modernas de LangGraph ---
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from typing import Annotated, TypedDict

load_dotenv()

# ==========================================
# 1. Definición del Estado del Grafo
# ==========================================
class RAGState(TypedDict):
    # add_messages asegura que los mensajes nuevos se concatenen al historial existente
    messages: Annotated[list, add_messages]
    context: list[str]

# ==========================================
# 2. Patrón Factory para el LLM 
# ==========================================
class LLMFactory:
    @staticmethod
    def create_llm(provider_name: str, **kwargs):
        provider = provider_name.lower()
        if provider == "groq":
            api_key = os.getenv("GROQ_API_KEY")
            model_name = kwargs.get("model_name", "llama-3.3-70b-versatile")
            return ChatGroq(groq_api_key=api_key, model_name=model_name, temperature=0.1)
        elif provider == "ollama":
            model_name = kwargs.get("model_name", "llama3")
            return ChatOllama(model=model_name, temperature=0.1)
        else:
            raise ValueError(f"Proveedor no soportado: {provider}")

# ==========================================
# 3. Orquestador Moderno con LangGraph
# ==========================================
class RAGPipeline:
    def __init__(self, vector_store, llm_provider="groq", memory_window=5):
        print(f"Inicializando RAG con {llm_provider} (Arquitectura LangGraph)...")
        self.llm = LLMFactory.create_llm(llm_provider) # Strategy: Inyección de dependencias para el LLM
        self.retriever = vector_store.as_retriever(search_kwargs={"k": 4}) # Strategy: Recuperar 4 documentos relevantes
        
        # Multiplicamos por 2 porque un "intercambio" tiene pregunta (User) y respuesta (AI)
        self.memory_window = memory_window * 2 

        # --- NODO 1: Recuperación de Información ---
        def retrieve_node(state: RAGState):
            # Tomamos la última pregunta del usuario
            last_message = state["messages"][-1].content
            docs = self.retriever.invoke(last_message)
            context = [doc.page_content for doc in docs]
            return {"context": context}

        # --- NODO 2: Generación de Respuesta ---
        def generate_node(state: RAGState):
            context_text = "\n\n".join(state["context"])
            system_prompt = SystemMessage(
                content="Eres un asistente virtual del banco DAVIbank. Responde basándote "
                        "ÚNICAMENTE en el siguiente contexto. Si no lo sabes, di que no "
                        f"tienes la información.\n\nContexto:\n{context_text}"
            )
            
            # REQUISITO: "N mensajes anteriores". 
            # Recortamos la lista de mensajes en memoria antes de enviarla al LLM.
            chat_history = state["messages"][-self.memory_window:]
            
            # Invocamos al LLM con las instrucciones + el historial acotado
            response = self.llm.invoke([system_prompt] + chat_history) # Strategy llm aplicado
            
            return {"messages": [response]}

        # --- CONSTRUCCIÓN DEL GRAFO ---
        workflow = StateGraph(RAGState)
        workflow.add_node("retrieve", retrieve_node)
        workflow.add_node("generate", generate_node)
        
        workflow.add_edge(START, "retrieve")
        workflow.add_edge("retrieve", "generate")
        workflow.add_edge("generate", END)

        # El Checkpointer es el encargado moderno de persistir las sesiones (ID)
        self.checkpointer = MemorySaver() 
        self.app = workflow.compile(checkpointer=self.checkpointer)

    def ask(self, question: str, session_id: str = "default_session") -> dict:
        """Procesa la pregunta inyectándola al grafo y filtrando por thread_id."""
        if not question.strip():
            return {"answer": "Por favor, escribe una pregunta.", "sources": []}
            
        print(f"Ejecutando Grafo para la sesión: {session_id}...")
        
        # En LangGraph, el session_id se maneja a través del thread_id en la config
        config = {"configurable": {"thread_id": session_id}}
        
        # Ejecutamos el grafo con el nuevo mensaje
        result = self.app.invoke(
            {"messages": [HumanMessage(content=question)]},
            config=config
        )
        
        # Extraemos la respuesta final generada y las fuentes
        answer = result["messages"][-1].content
        sources = result.get("context", [])
        
        return {
            "answer": answer,
            "sources": sources
        }