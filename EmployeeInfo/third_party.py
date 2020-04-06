import requests
import json
import time
BASE_URL='http://127.0.0.1:8000/'
ENDPOINT='api/'

print('Get Gequest')
def get_resources(id=None):
    data={ }
    if id is not None:
        data={
            'id':id
        }
    resp=requests.get(BASE_URL+ENDPOINT,data=json.dumps(data))
    print(resp.status_code) 
    print(resp.json())
get_resources(9)
time.sleep(5)
print('create request')
def create_resource():
    new_emp={
           'Emp_no':1000,
        'Emp_name':'kuheli',
        'Emp_sal':58030,
        'Emp_addr':'kolkata',

    }
    r=requests.post(BASE_URL+ENDPOINT,data=json.dumps(new_emp))
    print(r.status_code)
    print(r.json())
create_resource()
time.sleep(5)
######## this code use for the send the our requermant chache to drf application
print('update request')
def update_resource(id):
    new_data={
        'id':id,
        'Emp_name':'Shimran',
        'Emp_sal':10000,
    }
    r=requests.put(BASE_URL+ENDPOINT,data=json.dumps(new_data))# this line send the json file through url
    print(r.status_code)
    print(r.json())
update_resource(8)

time.sleep(5)
print("delete request")
def delete_resource(id):
    data={
        'id':id,
    }
    r=requests.delete(BASE_URL+ENDPOINT,data=json.dumps(data))
    print(r.status_code)
    print(r.json())
delete_resource(1)
