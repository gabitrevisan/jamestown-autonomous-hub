const express = require('express');
const app = express();
const port = process.env.PORT || 8080;

// Isso permite que a API receba dados em formato JSON do MQTT
app.use(express.json());

// Memória temporária da base Jamestown (começa com o dado padrão)
let statusJamestown = {
    sample_id: "JAM-GH01-SMP-0042",
    sector: "GH-01",
    timestamp: new Date().toISOString(),
    leaf_status: "saudavel", // Começa saudável
    temperature_c: 24.0,
    humidity_pct: 60.0,
    risk_score: 0.10,
    recommended_action: "nenhuma"
};

// Rota inicial
app.get('/', (req, res) => {
    res.send('Jamestown Autonomous Hub - ODS 2 e 9 - Monitoramento Ativo');
});

// Health check para o Azure
app.get('/health', (req, res) => {
    res.status(200).send('OK');
});

// O RPA do Rafa e do Du vai bater aqui (GET) para ler o status atual
app.get('/api/status', (req, res) => {
    res.json(statusJamestown);
});

// O MQTT/Maker do Breno vai bater aqui (POST) para atualizar o status
app.post('/api/status', (req, res) => {
    // Atualiza a memória com os dados novos que chegarem
    statusJamestown = { ...statusJamestown, ...req.body, timestamp: new Date().toISOString() };
    
    console.log("Novos dados recebidos via MQTT:", statusJamestown);
    res.status(200).json({ message: "Status atualizado com sucesso", data: statusJamestown });
});

app.listen(port, () => {
    console.log(`Console Jamestown rodando na porta ${port}`);
});