#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#


from ibmcloudant.cloudant_v1 import AllDocsQuery, CloudantV1, Document
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import requests
import sys



def main(params):
    myURL=params['COUCH_URL']
    myapikey=params['IAM_API_KEY']

    authenticator = IAMAuthenticator(myapikey) 
    client = CloudantV1(authenticator = authenticator)
    client.set_service_url(myURL)
#    service=client.new_instance()
    response="yes"
    
    new_document = Document(
        name = params['name'],
        dealership = int(params['dealership']),
        review = params['review'],
        purchase = bool(params['purchase']),
        purchase_date = params['purchase_date'],
        car_make = params['car_make'],
        car_model = params['car_model'],
        car_year = int(params['car_year'])
    )

    response = client.post_document(
        db='reviews',
        document=new_document
    ).get_result()

    return {
        "response" : response,
    }