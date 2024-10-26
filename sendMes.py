import requests
import json
import asyncio
from pprint import pprint as pp

def openJson(nameJson):
    
    with open(nameJson, 'r', encoding='utf-8') as file:
        
        data_json = json.load(file)
        
    return data_json

def loginRequest(urlRequest = 'https://api-seller.rozetka.com.ua/sites', data_login = {}):
    
    response = requests.post(urlRequest, json=data_login)
    
    response.raise_for_status()
    
    responseData = json.loads(response.text)
    
    return responseData

def requestListOrders(urlRequest = 'https://api-seller.rozetka.com.ua/orders/search', headerData = {}, params = {}):
    
    response = requests.get(urlRequest, headers=headerData, params = params)
    
    response.raise_for_status()
    
    responseData = json.loads(response.text)
    
    return responseData

def changeStatusReviewRequestSend(url, headers, data):
    
    response = requests.put(url, headers=headers, json=data)
    
    response.raise_for_status()
    
    responseData = json.loads(response.text)
    
    return responseData

def searchChatID(id, header, params):
    
    response = requests.get(f'https://api-seller.rozetka.com.ua/messages/{id}/order-chat', headers=header, params = params)
    
    response.raise_for_status()
    
    responseData = json.loads(response.text)
    
    return responseData['content']

def sendMess(url, headers, data):
    
    response = requests.post(url, headers=headers, json=data)
    
    response.raise_for_status()  
    
    return response.json()

def answerCreated(returnMes, answerMes, answerTick, order_id):
    
    returnMes.append({f'{order_id}': [answerMes['success'], answerTick['success']]})
    
def format_return_mes(return_mes):
    formatted_str = ""
    for item in return_mes:
        for key, value in item.items():
            formatted_str += f"{key}: {value},\n"
            
    formatted_str += f"Всього відправлено: {len(return_mes)}"
    return formatted_str

async def startBot(nameSeller):
    seller = {
        'Party Zoo': 'seller_PartyZoo.json',
        'Rock Dog': 'seller_RockDog.json'
    }
    
    data = openJson(seller[nameSeller])

    responseDataLogin = loginRequest('https://api-seller.rozetka.com.ua/sites', data)

    token = responseDataLogin['content']['access_token']

    requestHeaderListOrder = {
        'Authorization': f"Bearer {token}",
        'Accept-Validate-Exception': '1',
        'Content-Language': 'uk',
    }

    paramsRequestHeaderListOrder = {
        'type': 2,
        'is_review_request_send': 0,
        'has_market_review': 0
    }

    responseDataListOrder =  requestListOrders('https://api-seller.rozetka.com.ua/orders/search', requestHeaderListOrder, paramsRequestHeaderListOrder)

    listOrderIsReview = responseDataListOrder['content']['orders']
    
    returnMes = []
    
    for i in listOrderIsReview:
        id = i['id']
        
        dataForChangeReviewRequestSend = {
            'Authorization': f"Bearer {token}",
            'Content-Type': "application/json",
        }

        bodyChangeReviewRequestSend = {
            'order_ids': [id],
            'types': 1
        }

        dataForChangeReviewRequestSendMes = {
            'Authorization': f"Bearer {token}",
            'Content-Type': "application/json",
        }

        user_params = searchChatID(id, {
            'Authorization': f"Bearer {token}",
        },{
            "id": id
        })

        paramsChangeReviewRequestSendMes = {
            'body': f'Будь ласка, оцініть нашу роботу. Це займе декілька хвилин та допоможе нам покращити сервіс. Перейдіть за посиланням, зайдіть під своїм логіном та паролем, залишіть оцінку або напишіть відгук https://rozetka.com.ua/cabinet/shopreviews/{id}',
            'chat_id': user_params['id'],
            'sendEmailUser': 0,
            'receiver_id': user_params['user']['id'],
            'file': None
        }

        answerMes = sendMess('https://api-seller.rozetka.com.ua/messages/create', dataForChangeReviewRequestSendMes, paramsChangeReviewRequestSendMes)
        answerTick = changeStatusReviewRequestSend('https://api-seller.rozetka.com.ua/orders/review-request-status', dataForChangeReviewRequestSend, bodyChangeReviewRequestSend)
        
        answerCreated(returnMes,answerMes , answerTick, id)
    if returnMes == []:
        returnMes = 'Все вже відправлено'
        return returnMes
        
    return format_return_mes(returnMes)


if __name__ == "__main__":
    result = asyncio.run(startBot('Rock Dog'))
    print(result)
