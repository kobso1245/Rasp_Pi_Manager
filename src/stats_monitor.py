import subprocess


def execute_command(command):
    exec_command = subprocess.Popen(command,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
    stdout, stderr = exec_command.communicate()
    return exec_command.returncode, stdout


def retrieve_ram_usage():
    command = ['cat', '/proc/meminfo']
    ret_code, information = execute_command(command)

    if ret_code == 0:
        splitted_info = information.split('\n')
        # format
        def _clear_spaces(elem):
            splitted = elem.split(':')
            key = splitted[0]
            value = float(splitted[1].lstrip(' ').split(' ')[0]) / 1000000
            return (key, value)

        cleared_from_spaces = map(_clear_spaces, splitted_info[:-1])
        info_dct = dict(cleared_from_spaces)
        needed_info = {
            'total_ram': info_dct['MemTotal'],
            'free_ram': info_dct['MemFree'],
            'cached_ram': info_dct['Cached'],
            'swap_free': info_dct['SwapFree'],
            'swap_total': info_dct['SwapTotal']
        }
        return needed_info

    return information


def retrieve_cpu_usage():
    '''
    Return basic information:
        uptime
        cpu load
        users online
    '''

    def _parse_information(information):
        splitted_info = information.split('  ')
        try:
            uptime = splitted_info[1].replace(':', '.').strip(',')
            users = int(splitted_info[2][:-6])
            load = float(splitted_info[3][15:18].replace(',', '.'))
        except:
            print "Fail"

        percents = load / 4

        return {
            'uptime': uptime,
            'users_count': users,
            'load': percents
        }

    information = {}

    # check information about the CPU usage and uptime
    uptime_command = ["uptime"]
    ret_code, information = execute_command(uptime_command)
    if ret_code == 0:
        result = _parse_information(str(information))

    return result


def retrieve_cpu_temp():
    command = ['cat', '/sys/class/thermal/thermal_zone0/temp']
    ret_code, information = execute_command(command)
    if ret_code == 0:
        return {
            'temp': float(information) / 1000
        }

def retrieve_basic_information():
    ram_info = retrieve_ram_usage()
    cpu_info = retrieve_cpu_usage()
    temp_info = retrieve_cpu_temp()

print retrieve_cpu_temp()
