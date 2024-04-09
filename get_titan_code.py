import requests

def send_get_request(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error sending GET request: {e}")
        return None

if __name__ == '__main__':
    url = 'https://api-test1.container1.titannet.io/api/v2/generate/code'
    
    # Validate number of requests input
    while True:
        try:
            num_requests = int(input("Enter the number of requests: "))
            if num_requests > 0:
                break
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Please enter a valid integer.")

    jwt_token = input("Enter the JWT Authorization token: ")

    headers = {
        'Host': 'api-test1.container1.titannet.io',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,ru;q=0.7,en;q=0.6',
        'Cache-Control': 'no-cache',
        'Lang': 'cn',
        'Origin': 'https://test1.titannet.io',
        'Pragma': 'no-cache',
        'Referer': 'https://test1.titannet.io/',
        'Sec-Ch-Ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Jwtauthorization': jwt_token
    }

    with open('hashes.txt', 'w') as file:
        for i in range(num_requests):
            response = send_get_request(url, headers)
            if response:
                try:
                    data = response.json()
                    code = data.get('data', {}).get('code', 'N/A')
                    print(f"Request {i+1}: Status Code - {response.status_code}")
                    print(f"Response Code: {code}")
                    file.write(f"{code}\n")
                except ValueError:
                    print(f"Request {i+1}: Invalid JSON response")
            else:
                print(f"Request {i+1}: No response received")

