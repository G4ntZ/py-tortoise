import pysvn
import time
import requests
from requests.auth import HTTPBasicAuth
import json
class Svn:
    def __init__(self, user, password):
        self.user = user
        self.password = password

    def review(self, path, version):
        #print(version)
        #print(path)
        status = False
        client = pysvn.Client()
        client.callback_get_login = self.get_login
        rev = pysvn.Revision(pysvn.opt_revision_kind.number, version)
        try:
            
            logs = client.log(path, revision_start=rev, peg_revision=rev, limit=25)
            for ci in logs:
                #print(str(version) +" == " +str(ci.revision.number))
                if int(ci.revision.number) == int(version):
                    
                    status = True
                #print(path +" "+ str(ci.revision.number) +" "+ str(ci.author))
        except Exception as e:
            #status = False
            print(f"version no encontrada: {e}")
        return status

    def reviewPauta(self, paths):
        client = pysvn.Client()
        client.callback_get_login = self.get_login
        for pauta in paths:
            #print(pauta[0])
            rev = pysvn.Revision(pysvn.opt_revision_kind.number, pauta[1])
            s_version = self.check_version(pauta[0], rev, client, pauta[1])
            #print(s_version)

    def check_version(self, path, rev, client, version):
        try:
            logs = client.log(path, revision_start=rev, peg_revision=rev, discover_changed_paths=True, limit=25)
            for ci in logs:
                status = False
                if int(ci.revision.number) == int(version):
                    status = True
                #print(path +" "+ str(ci.revision.number) +" "+ str(ci.author))
        except:
            print("version no encontrada")
        return status

    def get_login(self, *args):
        return True, self.user, self.password, True

    def log_path(self, path):
        client = pysvn.Client()
        client.callback_get_login = self.get_login
        start=pysvn.Revision(pysvn.opt_revision_kind.head)
        try:
            logs = client.log(path, revision_start=start, limit=25, discover_changed_paths=True)
            response = ""
            for ci in logs:
                number = ci.revision.number
                author = ci.author
                fdate = ci.date
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(fdate))
                message = ci.message
                message = message.replace('\n','')
                actions = ci.changed_paths
                action = ""
                for a in actions:
                    action = action + a.action
                #print(f"{number} {action} {author} {date} {message}")
                response = response+',{ "number": '+ str(number) +', "action": "' +action+'", "author": "'+author+'", "date": "'+date+'", "message": "'+message+'"}'
            response = '['+ response[1:] +']'
            return response
        except Exception as e:
            print(f"Version no encontrada {e}")

    def get_version(self,path,version):
        url = f"{path}?r={version}"
        r = requests.get(url, auth=HTTPBasicAuth(self.user, self.password))
        data = {
            "body": r.text
        }
        return data