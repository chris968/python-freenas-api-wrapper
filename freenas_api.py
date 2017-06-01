#/usr/bin/python

import requests
import re
import json
import os
import io
import urllib

class FreenasAPI:
    def __init__(self, method, host, port, user, password):
        self.method = method
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def request(self, type, url, *payload):
        if type == 'GET':
            req = requests.get(
            '' + self.method + '://' + self.host + ':' + self.port + '/api/v1.0/'+ url + '/',
            headers={'Content-Type': 'application/json'},
            auth=( self.user, self.password ),
            verify=False,
            params='limit=100000',
            )

        if type == 'POST':
            req = requests.post(
            '' + self.method + '://' + self.host + ':' + self.port + '/api/v1.0/'+ url + '/',
            headers={'Content-Type': 'application/json'},
            auth=( self.user, self.password ),
            verify=False,
            data=payload[0],
            )

        if type == 'DELETE':
            req = requests.delete(
            '' + self.method + '://' + self.host + ':' + self.port + '/api/v1.0/'+ url + '/',
            headers={'Content-Type': 'application/json'},
            auth=( self.user, self.password ),
            verify=False,
            params='limit=100000',
            )

        return req.status_code, req.text


    def listusers(self):
        status, content = self.request('GET', 'account/users')

        data = {}
        data['status'] = str(status)
        data['data'] = json.loads(content)

        return json.dumps(data)


    def listalldatasets(self, volume_name):
        status, content = self.request('GET', 'storage/volume/' + urllib.parse.quote(volume_name) + '/datasets')

        data = {}
        if str(status) == '200':
            data['status'] = 'ok'
            content = json.loads(content)
            data['data'] = content
        else:
            data['status'] = 'error'
            data['data'] = 'Volume do not exist'

        return json.dumps(data)


    def listdatasets(self, volume_name, *dataset_name):
        status, content = self.request('GET', 'storage/volume/' + urllib.parse.quote(volume_name) + '/datasets')

        data = {}
        if str(status) == '200':
            data['status'] = 'ok'
            content = json.loads(content)

            if dataset_name:
                datasets = []
                dataset_index = 0
                for dataset in content:
                    if re.search(r'^' + re.escape(dataset_name[0]) + r'/.+$', dataset['name']):
                        datasets.append({})
                        datasets[dataset_index] = dataset
                        dataset_index += 1

                    data['data'] = datasets
                    if datasets == []:
                        data['data'] = 'No dataset(s) found'
            else:
                data['data'] = content

        else:
            data['status'] = 'error'
            data['data'] = 'Volume do not exist'

        return json.dumps(data)


    def createdataset(self, volume_name, dataset_name):
        payload = '{ "name": "' + dataset_name + '" }'
        status, content = self.request('POST', 'storage/volume/' + urllib.parse.quote(volume_name) + '/datasets', payload)
        content = json.loads(content)

        data = {}
        if str(status) == '201':
            data['status'] = 'ok'
            data['data'] = content
        else:
            data['status'] = 'error'
            data['data'] = content['__all__']

        return json.dumps(data)


    def deletedataset(self, volume_name, dataset_name):
        status, content = self.request('DELETE', 'storage/volume/' + urllib.parse.quote(volume_name) + '/datasets/' + urllib.parse.quote(dataset_name))

        data = {}
        if str(status) == '204':
            data['status'] = 'ok'
            data['data'] = content
        else:
            data['status'] = 'error'
            data['data'] = content

        return json.dumps(data)


    def listsnapshots(self, *dataset_name):
        status, content = self.request('GET', 'storage/snapshot')

        data = {}
        if str(status) == '200':
            data['status'] = 'ok'
            content = json.loads(content)

            if dataset_name:
                snapshots = []
                snapshot_index = 0
                for snapshot in content:
                    if snapshot['filesystem'] == dataset_name[0]:
                        snapshots.append({})
                        snapshots[snapshot_index] = snapshot
                        snapshot_index += 1

                    data['data'] = snapshots

                    if snapshots == []:
                        data['data'] = 'No snapshot(s) found'

            else:
                data['data'] = content

        else:
            data['status'] = 'error'
            data['data'] = 'unknown error'



        return json.dumps(data)


    def createsnapshot(self, dataset, name, recursive ):
        payload = '{ "dataset": "' + dataset + '", "name": "' + name + '", "recursive": ' + recursive + ' }'

        status, content = self.request('POST', 'storage/snapshot', payload)

        content = json.loads(content)

        data = {}
        if str(status) == '201':
            data['status'] = 'ok'
            data['data'] = content
        else:
            data['status'] = 'error'
            data['data'] = content['error']

        return json.dumps(data)


    def deletesnapshot(self, dataset, name ):
        status, content = self.request('DELETE', 'storage/snapshot/' + urllib.parse.quote(dataset) + '@' + urllib.parse.quote(name))

        data = {}
        if str(status) == '204':
            data['status'] = 'ok'
            data['data'] = content
        else:
            data['status'] = 'error'
            content = json.loads(content)
            data['data'] = content['error']

        return json.dumps(data)


    def clonesnapshot(self, name, destination):
        payload = '{ "name": "' + destination + '" }'

        status, content = self.request('POST', 'storage/snapshot/' + name + '/clone', payload)

        data = {}
        if str(status):
            data['status'] = 'ok'
            data['data'] = content
        else:
            data['status'] = 'error'
            data['data'] = content

        return json.dumps(data)
        

    def listnfsshares(self):
        status, content = self.request('GET', 'sharing/nfs')

        data = {}
        if str(status) == '200':
            data['status'] = 'ok'
            content = json.loads(content)
            data['data'] = content
        else:
            data['status'] = 'error'
            data['data'] = content

        return json.dumps(data)
