import requests
import json
from unidecode import unidecode


Bearer ="Bearer eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwicGNrIjoxLCJhbGciOiJkaXIiLCJ0diI6Miwia2lkIjoiYTdxIn0..Jn908J-yYgcKMNJnBlhrJg.J15niJBubgAPK5cSeKL6g78C1yBxirQW9HKZ0k1usVdsFOWY392OlR_qUazosk6EiCW2ge-4ahSUo5x-qooNPNz7bb2hWAXmj4MY81oF3oLMHi6JcAPzjYsVHlZQsAYEKjyUCFR7h8h4WHNSukDgidJ6fqumOHflRWCex_eODLYGlJl-B5ksgMByssOZCOFNX-l8ylDscykKpj79steWwPI_mscsEszAbihjXIliQNw7ysEp0Xyxypcc3YCshYIbVpWNcvA1gvmXPeeC4BB0EhwMbtkPdKHAPohnH-Y0y2xJfqQJ64-sG_k_vIIryQTrzQS_cBDldnvbHWWjR1DdJ0B4bFlQz4ciiIt0j7TH6jJPdWPUzII5mKweoNNrSxtkiR0U5ZHPsOuh9dMB7dlaYJQEDm9f4bm8RGoVyLN4NHBhAGL2LAkwCQ7osIVxEvP5nfeP9qZsZTCzQGzvT-a0V8MycVPxAbP1Nem9BV4oY9SbtVaTCwZv948gYOnNEAGW.ysGRHpe2a1rWDtGh30nRdw"

url = "http://api.devexhacks.com/credit-offers/products"
response=requests.request("GET", url, headers={'Authorization': Bearer})
result = response.json()

cc_info ={}
cc_rewards={}
for temp_url in result['products']:
    new_url ='http://api.devexhacks.com'+ temp_url['_links']['self']['href'][34:]

    new_response = requests.request("GET", new_url, headers={'Authorization': Bearer})
    new_result = new_response.json()
    cc_info[unidecode(temp_url['productDisplayName'])]=(new_result['annualMembershipFee'],new_result['rewards'])
    for k,val in cc_info.iteritems():
        try:
            cc_rewards[k]=(val[0],unidecode(val[1][0]['rewardsTiers'][0]['type']),val[1][0]['rewardsTiers'][0]['value'])
        except:
            #print val[1][0]['rewardsTiers']
            pass

    for k,val in cc_info.iteritems():
        try:
            #print val
            for items in val[1][0]['rewardsTiers']:
                if ('every pur' in unidecode(items['terms'])) or ('other purchase' in unidecode(items['terms'])):
                    #print "items",items
                    cc_rewards[k]=(unidecode(val[0]),unidecode(items['type']),(str(items['value'])+"x points"))
                    #print "dict",cc_rewards[k]
        except:
            pass

final_ar=[]
max_points =0
for k,v in cc_rewards.iteritems():
    if v[2]>=max_points:
        max_points = v[2]
for k,v in cc_rewards.iteritems():
    if v[2]==max_points:
        final_ar.append((k,v))

for card in final_ar:
    print card
