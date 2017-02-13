import subprocess
import psutil
from time import sleep
import os
from tabulate import tabulate

def execute_command(command):
    exec_command = subprocess.Popen(command,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
    stdout, stderr = exec_command.communicate()
    return exec_command.returncode, stdout


def retrieve_ram_usage():
    memory_holder = psutil.virtual_memory()
    return {'total': memory_holder.total,
            'available': memory_holder.available
            }


def retrieve_cpu_usage():
    '''
    Return basic information:
        uptime
        cpu load
        users online
    '''
    cpu_freq = psutil.cpu_freq(percpu=True)
    result = [{'curent': core.current,
               'min': core.min,
               'max': core.max} for core in cpu_freq]

    return result


def retrieve_cpu_temp():
    sensor_temp = psutil.sensors_temperatures()
    result = [{'label': label if current_device.label == ''
              else current_device.label,
               'current': current_device.current,
               'high': current_device.high,
               'crit': current_device.critical}
              for label in sensor_temp
              for current_device in sensor_temp[label]]
    return result


def retrieve_basic_information():
    ram_info = retrieve_ram_usage()
    cpu_info = retrieve_cpu_usage()
    temp_info = retrieve_cpu_temp()


def pretty_print():
    tab_data = [['Temperatures']]
    temp_sensors = retrieve_cpu_temp()
    for sensor in temp_sensors:
        tmp_data = [sensor['label'], sensor['current'], sensor['high'],
                    sensor['crit']]
        tab_data.append(tmp_data)
    print(tabulate(tab_data, ['Label', 'Current', 'High', 'Critical'],
                   'fancy_grid'))

if __name__ == '__main__':
    while True:
        os.system('clear')
        pretty_print()
        sleep(1)
