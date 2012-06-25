from django.http import HttpResponse
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt

import hashlib
import random
from datetime import datetime

from fs.alerts.models import User
from fs.alerts.models import Node
from fs.alerts.models import Alert
from fs.alerts.models import Contact

def validate(request):
    if 'd' in request.POST and request.POST['d']:
       try:
            obs = simplejson.loads(request.POST['d'])
            return True
       except simplejson.JSONDecodeError:
            return False
    else:
        return False

def set_error(msg):
    return {"error":True, "msg":msg}

def set_contact(uid,ctype,value):
    if ctype == "email":
        cont = Contact(user_id=uid,ctype="E",value=value)
    elif ctype == "sms":
        cont = Contact(user_id=uid,ctype="S",value=value)
    else:
        return False
    cont.save()
    return True

def set_user(ob):
    tag = hashlib.sha224(''.join([str(random.randint(1, 10000)),'KJHKJH*&^*&^*&^'])).hexdigest()[0:30]
    usr = User(user_tag=tag)
    usr.save()
    return usr

@csrf_exempt
def init_user(request):
    
    res = {}
    if validate(request):
        obs = simplejson.loads(request.POST['d'])

        ## Add the user
        usr = set_user(obs)

        ## Add any contact values.
        for key in obs["contact"].iterkeys():
            set_contact(usr.id, key, obs["contact"][key])

        res = {"usr":usr.user_tag};
    else:
        res = set_error("Validation Failed");

    return HttpResponse(simplejson.dumps(res), content_type='application/json')

@csrf_exempt
def handle_alert(request, user_tag):
    res = {}
    if validate(request):
        obs = simplejson.loads(request.POST['d'])
        usr = User.objects.get(user_tag=user_tag)
        
        if (usr == None):
            res = set_error("Invalid User");

        ## Add all the alerts.
        for nid in obs:
            for key in nid.iterkeys():
                try:
                    node = Node.objects.get(node_tag=key,user_id=usr.id)
                except Node.DoesNotExist:
                    node = Node(user_id=usr.id,high=0,low=10,node_tag=key)
                    node.save()

                # Then save the data for this node
                for alert in nid[key]:
                    alert = Alert(node_id=node.id,value=alert["v"],key=alert["k"])
                    alert.save()

        res = {"usr":usr.user_tag};
    else:
        res = set_error("Validation Failed");

    return HttpResponse(simplejson.dumps(res), content_type='application/json')

