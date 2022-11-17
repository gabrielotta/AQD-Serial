### Files ###

class File_Handler():
    def __init__(self):
        pass
    
    def save_file(self, texto, filename: str):
        try:
            with open(filename, 'w') as file:
                file.write(texto)
                filename = filename.replace('data', '')
                filename = filename.replace('/', '')
                filename = filename.replace('.txt', '')
                return 'Arquivo salvo com o nome: ' + '"' + filename + '"' + ' na pasta data.\n'
        except:
            return 1