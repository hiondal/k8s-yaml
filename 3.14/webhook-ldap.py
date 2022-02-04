from flask import Flask, request, jsonify
import pprint
import requests
import ldap
import base64
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

@app.route('/', methods=['POST'])

def auth():
    # Get request authentication data
    tokenReview = request.json
    print("\n")
    print("\n")

    # Display requested data
    pprint.pprint('---requested data---')
    pprint.pprint(tokenReview)

    print("\n")

    # Call authenticate user
    tokenReview['status'] = external_auth_LDAP(tokenReview)

    # Display authentication result
    pprint.pprint('-- Authentication result---')
    pprint.pprint(tokenReview)

    # Return data to Kubernetes API Server
    return jsonify(tokenReview)  

# Authentication system: LDAP
def external_auth_LDAP(tokenReview):
    try:
        # Get userid and password
        token = tokenReview['spec']['token'].decode('ascii')
        user, pw = token.split(':')
        #user, pw = tokenReview['spec']['token'].split (':')

        # Connect LDAP
        ldap_address = "ldap://169.56.70.201:389"
        ldap_object = initialize_ldap(ldap_address)

        # Authenticate user
        ldap_result = authenticate(ldap_object, ldap_address, user, pw)

        print('result: %s'%(ldap_result))

        # If success, update status field
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

# Authenticate user
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

# Connect LDAP
def initialize_ldap(ldap_address):
    ldap_object = ldap.initialize(ldap_address)
    return ldap_object

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=6000, debug=True)