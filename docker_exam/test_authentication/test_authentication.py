import os
import time
import requests

def add_to_log(output):
    # printing to a file
    if os.environ.get('LOG') == 1:
        log_path = '/home/app/logs/api_test.log'  # Path to the log file inside the container
        host_log_path = '../logs/api_test.log'  # Path to the log file on the host machine
        with open(log_path, 'a') as file:
            file.write(output)
        with open(host_log_path, 'a') as file:
            file.write(output)


def main():
    # Wait for the API container to become available
    #print("Waiting for the API container to start...")
    #time.sleep(10)  # Adjust the delay as needed
    api_address = 'sentiment_api_from_compose' # "0.0.0.0" #
    api_port = 8000

    username = 'alice'
    password = 'wonderland'

    url = f'http://{api_address}:{api_port}/permissions'
    params = {
        'username': username,
        'password': password
    }

    response = requests.get(url, params=params)

    output = f'''
    ============================
        Authentication test
    ============================
    Route: /permissions 
    Request URL: {url}
    Username: {username}
    Password: {password}
    Expected Result: 200
    Actual Result: {response.status_code}
    ==> {'SUCCESS' if response.status_code == 200 else 'FAILURE'}
    '''

    print(output)

    add_to_log(output)


if __name__ == '__main__':
    main()