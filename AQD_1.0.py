# AQD Serial - V1.0
# Aquisição de dados via porta serial
# 11/2022
# Leandro Felix / Gabriel

# imports ///////////////////////////////////////////////////////////////////////////////////////////////////
from custom_serial import Serial as serial
from fh import File_Handler as fh
import time
import PySimpleGUI as sg
import threading
import os
import datetime
import winsound
#from elevate import elevate
#elevate(show_console=False)

# variaveis globais //////////////////////////////////////////////////////////////////////////////////////////
baud_list = [9600, 19200, 38400, 57600, 115200, 128000, 230400, 256000, 460800, 921600]
baud_rate = 9600
port_list = ['COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'COM10', 'COM11', 'COM12', 'COM13', 'COM14', 'COM15']
port = '0'
ser = ()
flag_conec = False
porta_txt = ''
text_area = ''
sg.theme('Dark Gray 14')    # define o tema de cores da janela
THREAD_EVENT = '-THREAD-'   # evento do Thread
blocked = False             # bloqueia / libera a execução do Thread
cc_ended = False            # status das intruções do Thread. True = finalizadas. False = em execução
filename = ''               # string que armazena o nome do arquivo
conec_started = False
cs = serial()
fh = fh()
#////////////////////////////////////////////////////////////////////////////////////////////////////////////
def check_thread(main_window):

    starttime = time.time()     # tempo para blink do banner
    timenow = starttime         
    image_index = 1             # imagem 1 ou imagem 2 a cada 1s

    while True:
        global text_area, blocked, cc_ended, porta_txt, flag_conec, conec_started

        serial_data = cs.check_serial(text_area, blocked, porta_txt, flag_conec, conec_started)

        if len(serial_data) != 0:
            try:
                for data in serial_data:
                    if data[0] == False:
                        main_window['status_com'].Update(filename='img/conectado.png', subsample = 2)

                    if data[1] == False:
                        main_window['terminal'].Update(disabled=False)

                    if data[2] == '-THREAD-':
                        main_window.write_event_value('-THREAD-','')
                    
                    if len(data[3]) > 0:
                        text_area = data[3]

                    if data[4] != None:
                        main_window['porta'].Update(value=porta_txt)
            except:
                pass

        # sinalização através de banner piscante    
        timenow = time.time()           # obtem a contagem de tempo atual
        if flag_conec == False and timenow > starttime+0.500:
            starttime = time.time()     # atuailiza o valor referencia
            if image_index == 1:
                main_window.Element('status_com').Update(filename='img/desconec_gray.png', subsample = 2)
                image_index = 2
                winsound.Beep(700, 470)
            else:
                image_index = 1
                main_window.Element('status_com').Update(filename='img/desconec_red.png', subsample = 2)
                winsound.Beep(900, 470)

# FUNÇÕES ///////////////////////////////////////////////////////////////////////////////////////////////////
# def check_serial(main_window):

#     global text_area, blocked, cc_ended, porta_txt, flag_conec, conec_started
#     ident = "A420"              # identificador para a localização da substring
#     ident_ok = False            # flag que sinaliza que a conexão (reconexão) serial ocorreu
#     starttime = time.time()     # tempo para blink do banner
#     timenow = starttime         
#     image_index = 1             # imagem 1 ou imagem 2 a cada 1s

#     while True:

#         if blocked == False:    # esta função é bloqueada quando uma janela relativa ao Menu é aberta, pois ocorre erro - blocked == False:

#             cc_ended = False    # como não está bloqueada a função, esta var. deve ser = False
            
#             if conec_started == True and flag_conec == True:
#                 conec_started = False
#                 main_window['status_com'].Update(filename='img/conectado.png', subsample = 2)

#             try:
#                 buffer = ser.readline()
#                 string_1 = buffer.decode('utf-8')   # converte os dados do tipo byte em strin
                    
#                 if len (string_1) > 0 and ident in string_1:              # string é valida se tiver tamanho maior que zero. Tamanho zero == ocorrencia de timeout
#                     main_window.Find('terminal').Update(disabled=False)
#                     text_area = string_1
#                     main_window.write_event_value('-THREAD-','')
                
#                 flag_conec = True                   # sinaliza através da flag que a porta está aberta
                
#             except:                                 # porta não estando aberta causa erro e por consequencia o salto para o 'except'
#                 flag_conec = False
            
            

#             if flag_conec == False and porta_txt != 'Porta: ':  # informa que a porta COM está fechada
#                 # print('porta COM foi fechada\n')
#                 porta_txt = 'Porta: '
#                 main_window['porta'].Update(value=porta_txt)
#                 starttime = time.time()

#             # sinalização através de banner piscante    
#             timenow = time.time()           # obtem a contagem de tempo atual
#             if flag_conec == False and timenow > starttime+0.500:
#                 starttime = time.time()     # atuailiza o valor referencia
#                 if image_index == 1:
#                     main_window['status_com'].Update(filename='img/desconec_gray.png', subsample = 2)
#                     image_index = 2
#                     winsound.Beep(700, 470)
#                 else:
#                     main_window['status_com'].Update(filename='img/desconec_red.png', subsample = 2)
#                     image_index = 1
#                     winsound.Beep(900, 470)

#             cc_ended = True # informa que a função foi finalizada. Informação usada para abertura de janel do menu
#////////////////////////////////////////////////////////////////////////////////////////////////////////////
def show_sobre():
    sg.PopupNoTitlebar(
        """
        AQD Serial - Versão 1.0 - 2022
        Creditos: Leandro Felix - Gabriel Otta
        """
    )        
#////////////////////////////////////////////////////////////////////////////////////////////////////////////
# layout da main window /////////////////////////////////////////////////////////////////////////////////////
menu_layout = ( ["Arquivo", ["Sair"]],
                ["Ajuda", ['Como usar o AQD Serial', 'Sobre']]
                )

frame_01 = [ 
             [sg.Text('Porta:', size=(12,1), text_color='white', enable_events=True, key='porta'),
             sg.Combo(port_list, size=(7, 1), enable_events=True, key='-list_port-'),
             sg.VerticalSeparator(color='gray'),
             sg.Text('Baud rate', text_color='white'),
             sg.Combo(baud_list, default_value=9600, enable_events=True, key='baud'),
             sg.Image(filename='img/conectado.png', key='status_com', subsample = 2, tooltip='Status da comunicação')],
             [sg.HorizontalSeparator(color = 'gray')],
             [sg.Button('Abrir porta serial', key='openport', font = ('Arial', 10, 'bold'), size=(21,2),
             tooltip='Abrir a porta serial para estabelecer comunicação com a GIGA de testes'),
             sg.VerticalSeparator(color='gray'),
             sg.Button('', key='ger_dis', image_filename='img/ger_disp.png', image_size=(45,40), image_subsample=8, 
             tooltip='Abrir o gerenciador de dispositivos')] ]

frame_02 =  [ [sg.Button('Apagar mensagens', key='clear', tooltip='Limpar as mensagens da tela')] ]
                                                                                                         
layout = [
            [sg.MenuBar(menu_layout)],
            [sg.Multiline(size=(100,25), key='terminal', autoscroll=True, reroute_stdout=True, write_only=False,
            background_color='#151515', enable_events=True, border_width=3)],
            [sg.Frame('Comunicação', frame_01),
             sg.Frame('Terminal', frame_02, expand_x = True, expand_y = True, element_justification = 'center',
             vertical_alignment = 'c')] ]
#////////////////////////////////////////////////////////////////////////////////////////////////////////////

# criando a janela //////////////////////////////////////////////////////////////////////////////////////////
main_window = sg.Window('AQD Serial',layout, icon='img/aqd_serial.ico', finalize=True,
                        enable_close_attempted_event=True, location=(10,10))
main_window.finalize()  # finaliza a criação da janela. Sem este comando ocorre erro na função updatelistb()
#////////////////////////////////////////////////////////////////////////////////////////////////////////////

# abertura da porta serial //////////////////////////////////////////////////////////////////////////////////      
abertura, flag_conec, conec_started, ser = cs.openser_port(baud_rate, port)
if type(abertura) == int:
    porta_txt = 'Porta: '
    main_window['porta'].Update(value=porta_txt)
    sg.popup_error('Erro ao tentar abrir a porta serial. Conecte o cabo de comunicação na porta USB',
                    icon='img/aqd_serial.ico')

elif type(abertura) == str:
    main_window['porta'].Update(value=porta_txt)
#////////////////////////////////////////////////////////////////////////////////////////////////////////////

# ccriação do Thread relativo a comunicação serial //////////////////////////////////////////////////////////   
threading.Thread(target=check_thread, args=(main_window,), daemon=True).start()
#////////////////////////////////////////////////////////////////////////////////////////////////////////////

# delay para evitar bug na criação da main_window e ação de abrir ///////////////////////////////////////////
time.sleep(0.3)
#////////////////////////////////////////////////////////////////////////////////////////////////////////////

while True:
    # extraindo dados da tela - eventos e valores
    event, values = main_window.Read()

    # se a janela foi fechada a execução do programa deve ser encerrada
    if event in (None, sg.WIN_X_EVENT):
        break

    # botão saír do menu arquivo
    if event in (None, 'Sair'):     
        break
    
    # Sobre o AQD Serial
    if event in ('Sobre'):
        show_sobre()

    # Pdf de ajuda
    if event in ('Como usar o AQD Serial'):
        try:
            os.startfile('help\Help AQD Serial.pdf')  
        except:
            sg.popup_notify(""" O arquivo não localizado.""",
            icon='img/error.png', title='Erro', fade_in_duration=250, location=(10,10))


    # seleção de baud rate    
    if event == 'baud':             
        try:
            ser.close()
            baud_rate = values['baud']
            cs.openser_port(baud_rate, port)
        except:
            pass

    # seleção forçada de uma porta serial 
    if event == '-list_port-':                       
        try:
            port = values['-list_port-']
        except:
            pass
    
    # abrir a porta serial selecionada
    if event == 'openport':                         
        try:
            ser.close()   # fecha a atual porta serial aberta (caso haja uma)                          
        except:
            pass
        
        cs.openser_port(baud_rate, port)   # chama a função que abre a nova porta serial
    
    # limpar o texto que está no terminal
    if event == 'clear':                             
        main_window.Find('terminal').Update(disabled=False)
        main_window.Find('terminal').Update('')
        main_window.Find('terminal').Update(disabled=True)

    # abrir gerenciador de dispositivos
    if event == 'ger_dis':                  
        os.startfile('C:\Windows\System32\devmgmt.msc')

    if event == THREAD_EVENT:
        
        start_index = text_area.find(" ")   # localizador inicial
        end_index = text_area.find("p")     # localizador final 
        blocked = True                      # bloqueia as instruções do Thread
        # obtem dados de data e hora para formar o file name
        time_now = (datetime.datetime.now().strftime('%d-%m-%Y_%H-%M-%S')) 
        time_print = (datetime.datetime.now().strftime('%d/%m/%Y_%H:%M:%S'))
        # printa no terminal para sinalizar ao operador que o dado foi recebido na hora indicada
        main_window['terminal'].print("Dado recebido: " + time_print, text_color='orange') 
       
        # printa no terminal a informação contida na etiqueta impressa para conferecia do operador                            
        main_window['terminal'].print("Area em pes²: " + text_area[start_index+2:end_index-1], text_color='white')
        
        # conversão de pes² p/ m²
        texto = text_area[start_index+2:end_index-1]
        area_m2 = float(texto)      # converte a string em float
        area_m2 = area_m2 / 10.764  # conversão de pes² para m²
        area_m2 = round(area_m2, 2) # duas casas decimais
        text_area = str(area_m2)    # float para string

        # printa no terminal a informaçao em m²
        main_window['terminal'].print("Area em m²: " + text_area, text_color='white')
        
        # fomatação do nome do arquivo
        filename = 'data/' + 'Log ' + time_now + '.txt'  # cria o nome do arquivo  
        save = fh.save_file(text_area + " m²", filename)           # chama a função que salva o arquivo
        if type(save) != str:
            sg.popup_error('Erro ao tentar salvar o arquivo de Log', icon='img/aqd_serial.ico')

        # desabilita a atualização do terminal (nada pode ser escrito ou apagado do terminal pelo operador)
        main_window.Find('terminal').Update(disabled=True)
        blocked = False             # libera as instruções do Thread

# comando para fechar a janela          
main_window.close()
