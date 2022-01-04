from sseclient import SSEClient
import json
import argparse

def add_parser_args():
    parser = argparse.ArgumentParser(description='SSE CanBusHack Client')
    parser.add_argument('-u', '--url', dest='url', required=True, help='URL')
    parser.add_argument('-p', '--parameters', dest='parameters', required=False, help='Parameters')
    parser.add_argument('-d', '--delay', dest='delay', required=False, help='Parameters')
    parser.add_argument('-j', '--jsonlist', dest='json_list', required=False, help='FILE of Parameters JSON')

    parser.set_defaults(verbose=False)

    return parser.parse_args()


args = add_parser_args()
url = args.url
parameters = args.parameters
json_list_file = args.json_list
delay_str = args.delay or "0.1"
delay = float(delay_str)

if parameters is None and json_list_file is None:
    raise Exception("Need at least a parameters list or a json file")

json_parameters = None
if parameters is None:
    json_parameters = json.load(open(json_list_file, 'r'))

    parameters_list = []
    for param in json_parameters:
        for key, value in param.items():
            parameters_list.append(key)

    parameters = ','.join(parameters_list)

messages = SSEClient(
    f'http://{url}/v1/streams/stream-data/'
    f'{parameters}/'
    f'{delay}')

for msg in messages:
    msg_ = json.loads(msg.data)
    for key, value in msg_.items():
        print(f"{key}: {msg_[key]['value']:0.2f} ", end='')
    print('')
