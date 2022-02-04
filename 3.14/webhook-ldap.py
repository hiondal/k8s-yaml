from flask import Flask, request, jsonify
import pprint
import requests
import ldap
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

@app.route('/', methods=['POST'])

def auth():
    # User가 kubernetes API Server에 인증 요청
    # Kubernetes API Server가 사전에 정의된 Webhook Server로 REST 요청보낸것을 받아오는 코드
    tokenReview = request.json
    print("\n")
    print("\n")
    pprint.pprint('---return result---')
    pprint.pprint(tokenReview)

    print("\n")

    # Webhook Server에 연동되어있는 인증 서버에서 인증 결과 받아옴
    tokenReview['status'] = external_auth_LDAP(tokenReview)
    pprint.pprint('---return result---')
    pprint.pprint(tokenReview)
    
    # Webhook Server에서 Kubernetes API Server로 인증결과 보냄
    return jsonify(tokenReview)

# 외부 인증 시스템
def external_auth_LDAP(tokenReview):
    try:
        user, pw = tokenReview['spec']['token'].split (':')

        # 예제에서 생성했던 도메인 정보 (/etc/hosts 에 localhost로 명시했음)
        ldap_address = "ldap://myldap.io:389"

        ldap_object = initialize_ldap(ldap_address)
        ldap_result = authenticate(ldap_object, ldap_address, user, pw)

        print('result: %s'%(ldap_result))

        if ldap_result == True:
            status = {}
            status['authenticated'] = True
            status['user'] = {
                'username': user,
                'uid': user,
                #'groups': ['system:masters'] # 주석 해제하면 관리자 권한 부여
            }
        else :
            status = {}
            status['authenticated'] = False
    except:
        status = {}
        status['authenticated'] = False
    return status

def authenticate(ldap_object, ldap_address, user_name, password):
    try:
        ldap_object.simple_bind_s(user_name, password)
    except ldap.INVALID_CREDENTIALS:
        ldap_object.unbind()
        return False
    except Exception as e:
        print(e)
        return False
    return True

def initialize_ldap(ldap_address):
    ldap_object = ldap.initialize(ldap_address)
    return ldap_object

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=6000, debug=True)
