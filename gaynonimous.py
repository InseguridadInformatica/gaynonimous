import os
import subprocess
import time

def barra_de_progreso(iteracion, total, longitud=50, llenado='█'):
    progreso = (iteracion / total)
    flecha = '>'
    espacios = ' '
    longitud_progreso = int(longitud * progreso)
    barra = llenado * longitud_progreso + flecha + espacios * (longitud - longitud_progreso)
    print(f'\r[{barra}] {int(progreso * 100)}%', end='', flush=True)

def instalar_dependencias():
    print('Instalando dependencias...')
    comando_pkg = None

    if os.environ.get('PREFIX') == '/data/data/com.termux/files/usr':
        comando_pkg = 'pkg'
    else:
        comando_pkg = 'sudo apt'

    paquetes = ['tor', 'torsocks', 'tmux']

    for paquete in paquetes:
        subprocess.run([comando_pkg, 'install', '-y', paquete], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        barra_de_progreso(paquetes.index(paquete) + 1, len(paquetes))
        time.sleep(0.2)

    print('\nDependencias instaladas.')

def iniciar_sesion_tmux():
    print('Iniciando una nueva sesión de tmux...')

    subprocess.run(['tmux', 'new-session', '-d', '-s', 'mysession'])
    subprocess.run(['tmux', 'split-window'])

    print('Sesión de tmux iniciada.')

def iniciar_torsocks():
    print('Iniciando torsocks en el primer panel...')
    subprocess.run(['tmux', 'send-keys', '-t', 'mysession:0.0', '. torsocks on', 'C-m'])
    print('Torsocks iniciado.')

def finalizar_y_adjuntar():
    print('Finalizando y adjuntando a la sesión de tmux...')
    subprocess.run(['tmux', 'select-pane', '-t', 'mysession:0.1'])
    subprocess.run(['tmux', 'attach-session', '-t', 'mysession'])

def principal():
    comando_limpiar = 'clear' if os.name == 'posix' else 'cls'
    subprocess.run(comando_limpiar, shell=True)

    instalar_dependencias()
    iniciar_sesion_tmux()
    iniciar_torsocks()
    finalizar_y_adjuntar()

if __name__ == "__main__":
    principal()
