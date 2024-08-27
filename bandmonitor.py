from flask import Flask
import psutil, time, sys, json

app = Flask(__name__)

dados  = 'consumo.json'
dados_consumo = []

def byte2mega(bytes):
    # Converte os bytes para mega
    return bytes / 1024 / 1024


def monitoramento(intervalo = 1):
    
    print(f"{'Hora':<10}{'Download':<15}{'Upload':<15}")
    print('-' * 42)
    
    dados_iniciais = psutil.net_io_counters()
    
    while True:
        time.sleep(intervalo)
        
        dados_atual = psutil.net_io_counters()
        
        #calculo da diferenca de donwload e upload
        upload = dados_atual.bytes_sent - dados_iniciais.bytes_sent
        download = dados_atual.bytes_recv - dados_iniciais.bytes_recv
        
        #convertendo a diferança para mb bytes
        
        mb_upload = byte2mega(upload)
        mb_download = byte2mega(download)
        
        dados_iniciais = dados_atual
    
        dados_format = f"{time.strftime('%H:%M:%S'):>10} | {mb_download:<15.2f} | {mb_upload:<15.2f}" 

        dados_consumo = {
            'Hora': time.strftime('%d-%m-%Y %H:%M:%S'),
            "Download (MB)": round(mb_download, 2),
            "Upload (MB)": round(mb_upload, 2)
        }
        
        sys.stdout.write('\r' + dados_format)
        sys.stdout.flush()

        # salvando no historico
        with open('consumo.json', 'a') as file:
            json.dump(dados_consumo, file)
            file.write('\n')

        
if __name__ == "__main__":
    monitoramento();