import requests

def checkIfKeyIsValid(key):
    url = "https://payhip.com/api/v1/license/verify?product_link=zpHv&license_key=" + key
    headers = {
        'payhip-api-key': '10e808d815eaecef361713f8a75e4e604b29837e'
    }
    resp = requests.get(url=url, headers=headers).json()
    print(resp)

def disableKey(key):
    url = "https://payhip.com/api/v1/license/disable"
    headers = {
        'payhip-api-key': '10e808d815eaecef361713f8a75e4e604b29837e'
    }
    resp = requests.put(url=url, headers=headers, data={"product_link": "zpHv", "license_key": "GKKAR-KCLWM-SLJ5W-Z348Y"}).json()
    print(resp)

#checkIfKeyIsValid('GKKAR-KCLWM-SLJ5W-Z348Y')
disableKey('GKKAR-KCLWM-SLJ5W-Z348Y')