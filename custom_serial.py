#### Serial #####
# imports ///////////////////////////////////////////////////////////////////////////////////////////////////
import serial
import serial.tools.list_ports
import time
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
blocked = False             # bloqueia / libera a execução do Thread
cc_ended = False            # status das intruções do Thread. True = finalizadas. False = em execução
filename = ''               # string que armazena o nome do arquivo
conec_started = False
#////////////////////////////////////////////////////////////////////////////////////////////////////////////
# FUNÇÕES ///////////////////////////////////////////////////////////////////////////////////////////////////
class Serial():
    def __init__(self):
        pass
    # abertura da porta serial
    def openser_port(self, baud_rate, porta):
        global ser, porta_txt, flag_conec, conec_started
        try:
            if porta == '0':             # port = zero significa que a seleção de porta de ser automatica
                ports = serial.tools.list_ports.comports(include_links=False)
                sub_str = 'Bluetooth'   # sub strings de exclusão para porta serial
                sub_str2 = 'bluetooth'  # portas virtuais relacionadas ao bluetooth do note
                sub_str3 = 'COM1 '      # porta fisica deve ser ignorada também
                sub_str4 = 'COM1'       # por algum motivo a porta do meu pc não tem o espaço no final
                
                for port in ports :
                    str1 = ''.join(port) # transforma a lista em string
                    if sub_str in str1 or sub_str2 in str1 or sub_str3 in str1 or sub_str4 in str1: # se for uma porta relacionada ao bluetooth...
                        pass
                    else:           # se não é uma porta bluetooth ou fisica, então o endereço na variavel             
                        port_saved = port
                        
                ser = serial.Serial(port_saved.device)    
                   
                if ser.isOpen():    # caso a porta esteja aberta...
                    ser.close()     # fecha a porta

                port_used = port_saved.device
            else:                   # quando maior que 0 significa que a abertura de porta está sendo forçada pelo usuario
                port_used = porta

            ser = serial.Serial(port_used, baud_rate, timeout=1, write_timeout=1)
            ser.flushInput()    # limpa o bufer de entrada
            ser.flushOutput()   # limpa o buffer de saída
            porta_txt = 'Porta: ' + port_used
            flag_conec = True
            conec_started = True
            # print('porta ' + port_used + ' foi aberta\n')
            return porta_txt, flag_conec, conec_started, ser
            
        except:
            #### cria a popup de erro, entao deve retornar um código de erro
            return 0, flag_conec, conec_started, ser
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////
    def check_serial(self, text_area, blocked, porta_txt, flag_conec, conec_started):

        retorno = []

        ident = "A420"              # identificador para a localização da substring
        ident_ok = False            # flag que sinaliza que a conexão (reconexão) serial ocorreu

        if blocked == False:    # esta função é bloqueada quando uma janela relativa ao Menu é aberta, pois ocorre erro - blocked == False:
            
            if conec_started == True and flag_conec == True:
                conec_started = False
                retorno.append(conec_started)

            try:
                buffer = ser.readline()
                string_1 = buffer.decode('utf-8')   # converte os dados do tipo byte em string
                    
                if len (string_1) > 0 and ident in string_1:              # string é valida se tiver tamanho maior que zero. Tamanho zero == ocorrencia de timeout
                    retorno.append(False)
                    text_area = string_1
                    retorno.append('-THREAD-')
                    retorno.append(text_area)
                
                flag_conec = True                   # sinaliza através da flag que a porta está aberta
                
            except:                                 # porta não estando aberta causa erro e por consequencia o salto para o 'except'
                flag_conec = False
            
            

            if flag_conec == False and porta_txt != 'Porta: ':  # informa que a porta COM está fechada
                # print('porta COM foi fechada\n')
                porta_txt = 'Porta: '
                retorno.append(porta_txt)
                starttime = time.time()

            return retorno
        return retorno
