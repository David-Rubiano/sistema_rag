import os 
import json
import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from typing import Dict, Any

# ==========================================
# 1. Interfaz de la Estrategia (Strategy)
# ==========================================
class ScraperStrategy(ABC):
    @abstractmethod
    def scrape(self, url: str) -> Dict[str, Any]:
        """Debe retornar un diccionario con los datos 'raw' y 'clean'."""
        pass

# ==========================================
# 2. Estrategias Concretas
# ==========================================
class BBVAScraperStrategy(ScraperStrategy):
    def __init__(self):
        # Headers para simular un navegador real y evitar bloqueos básicos 403
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8"
        }

    def scrape(self, url: str) -> Dict[str, Any]:
        print(f"Iniciando scraping en: {url}")
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            raw_html = response.text
            
            # Limpieza con BeautifulSoup
            soup = BeautifulSoup(raw_html, 'html.parser')
            
            # Eliminar scripts, estilos y header/footers que meten ruido
            for element in soup(["script", "style", "nav", "footer", "header"]):
                element.decompose()
                
            # Extraer texto limpio
            clean_text = " ".join(soup.stripped_strings)
            
            return {
                "url": url,
                "raw_content": raw_html,
                "clean_content": clean_text,
                "status": "success"
            }
        except Exception as e:
            print(f"Error haciendo scraping a {url}: {e}")
            return {"url": url, "raw_content": None, "clean_content": None, "status": "error", "message": str(e)}

# ==========================================
# 3. Contexto (El ejecutor)
# ==========================================
class WebScraper:
    def __init__(self, strategy: ScraperStrategy):
        self._strategy = strategy
        # Crear directorios para cumplir con el requisito de almacenar datos crudos y limpios
        self.raw_dir = os.path.join(os.getcwd(), "data", "raw")
        self.clean_dir = os.path.join(os.getcwd(), "data", "clean")
        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.clean_dir, exist_ok=True)

    def set_strategy(self, strategy: ScraperStrategy):
        self._strategy = strategy

    def execute_and_save(self, urls: list[str]):
        for idx, url in enumerate(urls):
            result = self._strategy.scrape(url)
            
            if result["status"] == "success":
                # Guardar crudo (HTML)
                raw_path = os.path.join(self.raw_dir, f"page_{idx}_raw.html")
                with open(raw_path, 'w', encoding='utf-8') as f:
                    f.write(result["raw_content"])
                
                # Guardar limpio (TXT)
                clean_path = os.path.join(self.clean_dir, f"page_{idx}_clean.txt")
                with open(clean_path, 'w', encoding='utf-8') as f:
                    f.write(result["clean_content"])
                
                print(f"Datos guardados exitosamente para {url}")
            else:
                print(f"Fallo en {url}: {result.get('message')}")