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
        
def run_user_authorization_test(api_address, api_port, username, password, sentence, api_version):
    url = f'http://{api_address}:{api_port}/{api_version}/sentiment'
    params = {
        'username': username,
        'password': password,
        'sentence': sentence
    }
    
    response = requests.get(url, params=params)
    
    output = f'''
    ============================
    User: {username}
        User Authorization Test
    ============================
    Password: {password}
    Sentence: {sentence}
    API Version: {api_version}
    Expected Result: 200
    Actual Result: {response.status_code}
    ==> {'SUCCESS' if response.status_code == 200 else 'FAILURE'}
    '''
    print(output)
    add_to_log(output)


def main():
    # Wait for the API container to become available
    #print("Waiting for the API container to start...")
    #time.sleep(10)  # Adjust the delay as needed
    api_address = 'sentiment_api_from_compose' # "0.0.0.0" #
    api_port = 8000
    sentence = 'This is a positive sentence.'
    # Test for user "bob" with access to v1 but not v2
    run_user_authorization_test(api_address=api_address, api_port=api_port, username='bob', password='builder', sentence=sentence, api_version='v1')
    run_user_authorization_test(api_address=api_address, api_port=api_port, username='bob', password='builder', sentence=sentence, api_version='v2')

    # Test for user "alice" with access to both v1 and v2
    run_user_authorization_test(api_address=api_address, api_port=api_port, username='alice', password='wonderland', sentence=sentence, api_version='v1')
    run_user_authorization_test(api_address=api_address, api_port=api_port, username='alice', password='wonderland', sentence=sentence, api_version='v2')
    

if __name__ == '__main__':

    main()
