import json

class JamestownAssistant:
    def __init__(self):
        print(f"\n🤖 Assistente Jamestown Online (Modo Autônomo).")

    def load_current_status(self):
        """Lê o diagnóstico da estufa."""
        try:
            with open('../big-data/dags/vision_diagnosis.json', 'r') as f:
                return json.load(f)
        except:
            return None

    def get_action_protocol(self, status):
        """Lógica de decisão local blindada contra erros de tipo"""
        diagnostico = str(status.get('predicted_class', ''))

        if 'fungo' in diagnostico.lower():
            return "ALERTA: Fungo patógeno detectado. Protocolo: Isolar bandeja afetada, aplicar fungicida biológico e aumentar ventilação."
        elif 'estresse' in diagnostico.lower():
            return "ALERTA: Estresse hídrico. Protocolo: Verificar sistema de irrigação e ajustar níveis de umidade do solo."
        else:
            return f"STATUS: {diagnostico}. Protocolo: Manter monitoramento padrão."

    def ask_counselor(self, question):
        status = self.load_current_status()
        if not status:
            return "Não consegui ler os dados da estufa."
        
        protocolo = self.get_action_protocol(status)
        return f"RELATÓRIO: {status}\n\nRECOMENDAÇÃO: {protocolo}"

if __name__ == "__main__":
    ai = JamestownAssistant()
    pergunta = input("Comandante, qual é a sua dúvida?: ")
    print(f"\n🚀 RESPOSTA:\n{ai.ask_counselor(pergunta)}")