import os
import time
import base64
import asyncio
import requests

from io import BytesIO
from PIL import Image
from capmonstercloudclient import ClientOptions, CapMonsterClient
from capmonstercloudclient.requests import ImageToTextRequest

def find_between(s, start, end):
    try:
        return (s.split(start))[1].split(end)[0]
    except:
        return None

async def saldo():
    task = await cap_monster_client.get_balance()
    return task

async def solve_captcha_sync(num_requests):
    return [await cap_monster_client.solve_captcha(image_request) for _ in range(num_requests)]

if __name__ == '__main__':
    client_options = ClientOptions(api_key='7655a98f5843913c3340c9b3678eb31b')
    cap_monster_client = CapMonsterClient(options=client_options)
    response = asyncio.run(saldo())
    saldo = response['balance']
    if saldo > 0:

        response = requests.get("https://www.chebanca.it/public/conto-premier/aprilo-subito#")
        base64str = find_between(response.text, 'data:image/png;base64,', '"')
        if base64str != None:
            image_bytes = base64.b64decode(base64str)
            
            image_request = ImageToTextRequest(image_bytes=image_bytes, threshold=50, module_name='amazon', case=True, numeric=1, math=False)
            nums = 3

            sync_start = time.time()
            sync_responses = asyncio.run(solve_captcha_sync(nums))
            tempo = f'{1/((time.time()-sync_start)/nums):0.2f} '
            solucaoCaptcha = sync_responses[0]['text']
            # imagem_io = BytesIO(image_bytes)
            # imagem_pil = Image.open(imagem_io)
            # imagem_pil.show() 
            resultado = f'Captcha: {solucaoCaptcha} - Tempo: {tempo} - Saldo: {saldo}'
            print(resultado)
        else:
            print("Erro ao obter imagem")
    else:
        print(f"Sem saldo: {saldo}")

# pip install Pillow