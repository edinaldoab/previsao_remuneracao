import pendulum
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from function import get_job_info

with DAG(
            'scrapping_glassdoor', #nomeia o dag
            start_date=pendulum.datetime(2023, 4, 3, tz='UTC'), #configura a data de início
            schedule_interval='0 9 * * 1' # agenda a execução para todas as segundas-feiras à 09:00
) as dag:
    
    #pasta de destinação dos datasets gerados
    path_base = '/home/edinaldo/Documents/previsao_remuneracao/previsao_remuneracao/airflow_script/datasets'
    
    #cria uma tarefa do Bash para gerar o dataset da semana
    task_1 = BashOperator(
        task_id = 'cria_pasta_de_cada_dataset'
        bash_command = f'mkdir -p "{path_base}/semana={{data_interval_end.strftime("%Y-%m-%d")}}"'
    )
    
    #seta o caminho da pasta criada pelo BashOperator()
    path = f'{path_base}/semana={{data_interval_end.strftime("%Y-%m-%d")}}'
    
    #executa o script de raspagem dos dados
    task_2 = PythonOperator(
        task_id = 'raspa_dados'
        python_callable=get_job_info('Data Engineer', 'United States', 15, path)
    )
    
    task_1 >> task_2
