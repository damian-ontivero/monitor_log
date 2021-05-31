import os.path
import time
import logging
import subprocess
from datetime import date

log_dir = '/var/log/gestor-trackme/' + date.today().strftime('%Y%m%d') + '/'
log_file = 'GestorTrackMe_GruposConfiguracion_index_0.log'
time_out = 30
service = 'gestor-trackme'

log_date_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename = os.path.dirname(os.path.abspath(__file__)) + '/main.log', level = logging.WARNING, format = log_date_format)

def CheckLog():
    while os.path.isdir(log_dir):
        try:
            if (time.time() - os.path.getmtime(log_dir + log_file) > time_out):
                logging.warning('No hay cambios en el archivo. Es necesario iniciar o reiniciar el servicio.')
                if IsRunning(service):
                    logging.warning('Ejecutando reinicio del servicio...')
                    RestartService(service)
                else:
                    logging.warning('Ejecutando inicio del servicio...')
                    StartService(service)
            else:
                logging.info('Hay cambios en el archivo. No es necesario reiniciar el servicio.')
        except FileNotFoundError:
            logging.error('El archivo "' + log_file  + '" no existe. Es necesario iniciar o reiniciar el servicio.')
            if IsRunning(service):
                logging.warning('Ejecutando reinicio del servicio...')
                RestartService(service)
            else:
                logging.warning('Ejecutando inicio del servicio...')
                StartService(service)
        time.sleep(time_out)
    else:
        logging.error('El directorio "' + log_dir + '" no existe.')

def IsRunning(service):
    p = subprocess.Popen(['pgrep', '-f', '/' + service + '/'])
    if p.poll() == 0:
        return True
    else:
        return False

def StartService(service):
    command = 'start ' + service
    try:
        subprocess.call(command, shell = True)
    except FileNotFoundError:
        logging.error('Inicio del servicio incorrecto. Comando invalido: "' + command + '"')
    else:
        logging.warning('Inicio del servicio correcto. Comando valido: "' + command + '"')
    finally:
        logging.warning('Proceso de inicio terminado.')


def RestartService(service):
    command = 'restart ' + service
    try:
        subprocess.call(command, shell = True)
    except FileNotFoundError:
        logging.error('Reinicio del servicio incorrecto. Comando invalido: "' + command + '"')
    else:
        logging.warning('Reinicio del servicio correcto. Comando valido: "' + command + '"')
    finally:
        logging.warning('Proceso de reinicio terminado.')

if __name__ == '__main__':
    while True:
        CheckLog()