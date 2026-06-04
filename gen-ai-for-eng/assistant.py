import os
import json
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

# carrega as variáveis de ambiente do ficheiro .env para o sistema
load_dotenv()

class JamestownAssistant:
    def __init__(self):
        # coleta a chave do .env
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            raise ValueError("ERRO: A chave GEMINI_API_KEY não foi encontrada no ficheiro .env!")
            
        genai.configure(api_key=api_key)
        
        # configurando o modelo de IA
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')

    def load_current_status(self):
        """Lê os dados reais gerados pelo Airflow e Visão Computacional"""
        try:
            # lê o JSON gerado pelo código de Visão Computacional (big-data folder)
            caminho_json = '../big-data/dags/vision_diagnosis.json'
            
            with open(caminho_json, 'r') as f:
                vision_data = json.load(f)
            
            status_text = f"Módulo: {vision_data['module_id']} | Diagnóstico da Planta (Classe): {vision_data['predicted_class']} | Confiança: {vision_data['confidence']}"
            return status_text
        except FileNotFoundError:
            return "Aviso: O ficheiro de sensores não foi encontrado. Execute o modelo de Visão Computacional primeiro."
        except Exception as e:
            return f"Erro ao ler sensores: {e}"

    def ask_counselor(self, user_question):
        """Envia o contexto da estufa + a pergunta do utilizador para o Gemini"""
        estufa_status = self.load_current_status()
        
        prompt = f"""
        És a IA Conselheira da base espacial lunar Jamestown.
        STATUS ATUAL DA ESTUFA: {estufa_status}
        (Lembrete das Classes: 0=Saudável, 1=Estresse Hídrico/Nutricional, 2=Fungo Patógeno).
        
        O Comandante da base faz a seguinte pergunta: {user_question}
        
        Responde de forma científica, direta e sugere ações de contenção ou manutenção para a equipa ou para o braço robótico (Maker Lab).
        """
        
        print("\n[A consultar os bancos de dados da base Jamestown...]")
        response = self.model.generate_content(prompt)
        return response.text

if __name__ == "__main__":
    # teste interativo no terminal
    try:
        ai = JamestownAssistant()
        print("🤖 Assistente Jamestown Online.")
        pergunta = input("Comandante, qual é a sua dúvida em relação à estufa? ")
        
        resposta = ai.ask_counselor(pergunta)
        print(f"\n🚀 RESPOSTA DA IA:\n{resposta}")
        
    except Exception as erro:
        print(f"Erro na inicialização: {erro}")