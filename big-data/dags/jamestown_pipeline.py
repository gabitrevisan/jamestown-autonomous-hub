import os
import pandas as pd
import requests
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.oracle.hooks.oracle import OracleHook

# caminhos absolutos no container do Docker
DATA_DIR = '/opt/airflow/dags'
TELEMETRY_FILE = os.path.join(DATA_DIR, 'telemetry_greenhouse.csv')
VISION_FILE = os.path.join(DATA_DIR, 'vision_diagnosis.json')

default_args = {
    'owner': 'Equipe_Jamestown',
    'start_date': datetime(2026, 5, 25),
    'retries': 1,
}

with DAG('jamestown_mission_pipeline', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:

    def extract_and_transform(**kwargs):
        # 1. LER ARQUIVOS LOCAIS (CSV E JSON)
        df_tel = pd.read_csv(TELEMETRY_FILE)
        df_vis = pd.read_json(VISION_FILE)
        
        # 2. LER API DA NASA (DONKI - Clima Espacial Real)
        # usando a data de quando a V1 do projeto foi criada como parâmetro
        nasa_api_url = "https://api.nasa.gov/DONKI/CME?startDate=2026-05-01&endDate=2026-05-26&api_key=DEMO_KEY"
        try:
            response = requests.get(nasa_api_url)
            nasa_data = response.json()
            # flag para avisar que há evento espacial rolando
            space_weather_alert = 1 if len(nasa_data) > 0 else 0
        except:
            space_weather_alert = 0
            
        # 3. TRATAMENTO DE DADOS
        # preenchendo pH vazio com a média
        df_tel['ph'] = df_tel['ph'].fillna(df_tel['ph'].mean())
        # preenchendo CO2 vazio com 800 (padrão)
        df_tel['co2_ppm'] = df_tel['co2_ppm'].fillna(800.0)
        
        # merge (join) da telemetria com a visão pelo módulo e timestamp aproximado
        df_tel['timestamp'] = pd.to_datetime(df_tel['timestamp'])
        df_vis['timestamp'] = pd.to_datetime(df_vis['timestamp'])
        
        # ordenando para o merge_asof funcionar
        df_tel = df_tel.sort_values('timestamp')
        df_vis = df_vis.sort_values('timestamp')
        
        # junta o diagnóstico da visão com a leitura do sensor mais próxima
        df_final = pd.merge_asof(df_tel, df_vis, on='timestamp', by='module_id', direction='nearest')
        
        # adicionando a flag da NASA
        df_final['nasa_radiation_alert'] = space_weather_alert
        
        # salvando arquivo tratado temporariamente para a próxima task
        clean_file_path = os.path.join(DATA_DIR, 'clean_data.csv')
        df_final.to_csv(clean_file_path, index=False)

    def load_to_oracle(**kwargs):
        # lê o arquivo limpo
        clean_file_path = os.path.join(DATA_DIR, 'clean_data.csv')
        df = pd.read_csv(clean_file_path)
        
        # conecta no Oracle da FIAP
        oracle_hook = OracleHook(oracle_conn_id='oracle_fiap')
        connection = oracle_hook.get_conn()
        cursor = connection.cursor()
        
        # carrega linha a linha
        for index, row in df.iterrows():
            insert_query = """
                INSERT INTO FACT_JAMESTOWN_DATA 
                (timestamp, module_id, ph, humidity, co2, temperature, radiation, predicted_class, nasa_alert)
                VALUES (TO_TIMESTAMP(:1, 'YYYY-MM-DD HH24:MI:SS'), :2, :3, :4, :5, :6, :7, :8, :9)
            """
            
            # 1. Trata a data forçando o formato exato que o Oracle entende
            data_formatada = pd.to_datetime(row['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            
            # 2. Trata valores nulos da classe prevista
            pred_class = int(row['predicted_class']) if pd.notna(row['predicted_class']) else -1
            
            cursor.execute(insert_query, (
                data_formatada, 
                str(row['module_id']), 
                float(row['ph']), 
                float(row['humidity_pct']), 
                float(row['co2_ppm']), 
                float(row['temperature_c']), 
                float(row['radiation_msv']), 
                pred_class, 
                int(row['nasa_radiation_alert'])
            ))
            
        connection.commit()
        cursor.close()
        connection.close()

    extract_transform_task = PythonOperator(task_id='extract_and_transform', python_callable=extract_and_transform)
    load_task = PythonOperator(task_id='load_to_oracle', python_callable=load_to_oracle)

    extract_transform_task >> load_task