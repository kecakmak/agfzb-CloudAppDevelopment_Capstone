from ibmcloudant.cloudant_v1 import AllDocsQuery, CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import requests
import sys



def main(params):
    myURL=params['COUCH_URL']
    myapikey=params['IAM_API_KEY']

    authenticator = IAMAuthenticator(myapikey) 
    client = CloudantV1(authenticator = authenticator)
    client.set_service_url(myURL)

    d_id = int(params['dealerId'])
    response = client.post_find(
        db='reviews',
        selector={'dealership': {'$eq': d_id}}
    ).get_result()

    return {
        "response": response
    }
    