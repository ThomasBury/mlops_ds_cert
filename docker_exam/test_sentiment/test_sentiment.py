import os
import time
import requests


def add_to_log(output):
    # printing to a file
    if os.environ.get('LOG') == 1:
        log_path = '/home/app/logs/api_test.log'  # Path to the log file inside the container
        host_log_path = './logs/api_test.log'  # Path to the log file on the host machine
        with open(log_path, 'a') as file:
            file.write(output)
        with open(host_log_path, 'a') as file:
            file.write(output)

    
def main():
    # Wait for the API container to become available
    #print("Waiting for the API container to start...")
    #time.sleep(10)  # Adjust the delay as needed
    
    api_address = 'sentiment_api_from_compose' # "0.0.0.0" 
    api_port = 8000

    def run_sentiment_analysis_test(username, password, api_version, sentence):
        url = f'http://{api_address}:{api_port}/{api_version}/sentiment'
        params = {
            'username': username,
            'password': password,
            'sentence': sentence
        }

        response = requests.get(url, params=params)
        sentiment_score = response.json().get('score')

        return sentiment_score

    def test_result(username, api_version, sentence, expected_sentiment, sentiment_score):
        test_status = 'POSITIVE' if sentiment_score > 0 else 'NEGATIVE'
        output = f'''
        ===============================
           Sentiment Analysis Test
        ===============================
        User: {username}
        Sentence: {sentence}
        API Version: {api_version}
        Expected Sentiment: {expected_sentiment}
        Actual Sentiment Score: {sentiment_score}
        ==> {test_status}
        '''
        add_to_log(output)
        print(output)

    # Test for user "alice" with access to both v1 and v2
    username_alice = 'alice'
    password_alice = 'wonderland'
    sentences = [
        'life is beautiful',
        'that sucks'
    ]

    for sentence in sentences:
        # Test for v1
        sentiment_score_v1 = run_sentiment_analysis_test(username_alice, password_alice, 'v1', sentence)
        test_result(username_alice, 'v1', sentence, 'POSITIVE', sentiment_score_v1)

        # Test for v2
        sentiment_score_v2 = run_sentiment_analysis_test(username_alice, password_alice, 'v2', sentence)
        test_result(username_alice, 'v2', sentence, 'NEGATIVE', sentiment_score_v2)


if __name__ == '__main__':
    main()