from datetime import datetime,timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

#define a function to run daily
def greet(ti):
  first_name = ti.xcom_pull(task_ids='get_name',key='first_name')
  last_name = ti.xcom_pull(task_ids='get_name',key='last_name')
  age = ti.xcom_pull(task_ids='get_name',key='age')
  print(f'hello airflow, my name is {first_name} {last_name},'
        f'and I am {age} years old!')

  
def get_name(ti):
  ti.xcom_push(key='first_name',value='xyz')
  ti.xcom_push(key='last_name',value='abc')

def get_age(ti):
  ti.xcom_push(key='age',value=18)
#default parameters
default_args = {
  'owner':'saint',
  'retries':5,
  'retry_delay':timedelta(minutes=5)
}


#create an instance of a dag
with DAG(
       default_args = default_args,
       dag_id = 'Our_dag_with_python_operator_v7',
       description ='Our first dag using python operator',
       start_date = datetime(2021,7,4,6),
       schedule_interval = '@daily'
) as dag:
      task1 = PythonOperator(
          task_id='greet',
          python_callable=greet
          # op_kwargs={'age':22}
      )
      
      task2 = PythonOperator(
          task_id = 'get_name',
          python_callable = get_name
      )

      task3 = PythonOperator(
          task_id='get_age',
          python_callable = get_age
      )

      [task2, task3] >> task1