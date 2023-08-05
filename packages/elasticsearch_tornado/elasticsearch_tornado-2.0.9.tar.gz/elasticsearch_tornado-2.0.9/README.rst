Tornado Elasticsearch Client
----------------------------
Tornado HTTP client for Elasticsearch. Its goal is to provide common
ground for all Elasticsearch-related code in tornado and provide a
similar api to the official elasticsearch python client (elasticsearch-py).
However, this client only works for HTTP (no thrift or memcache) and doesn't
support connection pooling at this time (one client per instance). This
allows for you to design your own pooling/handling of callbacks.


Elasticsearch Compatibility
---------------------------
The library is compatible with Elasticsearch 2.X


Installation
------------
.. code-block:: bash

    pip install elasticsearch_tornado


Documentation
-------------
http://elasticsearch-tornado.readthedocs.org/en/latest/


CLI
---
Elasticsearch Tornado also provides a handy cli for interacting with
Elasticsearch clusters. Here are a few handy commands:

.. code-block:: bash
    
    # indexing

    $ cat data.json
    { "index" : { "_index" : "test", "_type" : "type1", "_id" : "1" } }
    { "user" : "foo", "age": 100 }
    { "index" : { "_index" : "test", "_type" : "type1", "_id" : "2" } }
    { "user" : "bar", "age": 99 }

    $ cat data.json | et index
    {"took":19,"errors":false,"items":[{"index":{"_index":"test","_type":"type1","_id":"1","_version":8,"_shards":{"total":2,"successful":1,"failed":0},"status":200}}]}

    # searching

    $ et search -q 'age:99'
    {"took":5,"timed_out":false,"_shards":{"total":8,"successful":8,"failed":0},"hits":{"total":2,"max_score":1.5108256,"hits":[{"_index":"test","_type":"type1","_id":"2","_score":1.5108256},{"_index":"test","_type":"test_type","_id":"2","_score":1.5108256,"_source":{ "user" : "bar", "age": 99 }}]}}

    # cat API

    $ et cat master
    127.0.0.1 127.0.0.1 8 20 0.05 d * Randall Shire

    $ et cat nodes
    127.0.0.1 127.0.0.1 8 20 0.05 d * Randall Shire

    $ et cat shards
    index    2 p STARTED    0  131b 127.0.0.1 Randall Shire
    index    2 r UNASSIGNED
    index    4 p STARTED    1 3.7kb 127.0.0.1 Randall Shire
    index    4 r UNASSIGNED
    index    3 p STARTED    0  131b 127.0.0.1 Randall Shire
    index    3 r UNASSIGNED
    index    1 p STARTED    0  131b 127.0.0.1 Randall Shire
    index    1 r UNASSIGNED
    index    0 p STARTED    0  131b 127.0.0.1 Randall Shire
    index    0 r UNASSIGNED
    test     0 p STARTED    0  159b 127.0.0.1 Randall Shire
    test     0 r UNASSIGNED
    .scripts 0 p STARTED    1 2.7kb 127.0.0.1 Randall Shire


Example use
-----------
Simple use-case:

.. code-block:: python

    from __future__            import print_function
    from elasticsearch_tornado import EsClient, serialize
    from functools             import partial
    from tornado               import ioloop, gen
    import json


    c = EsClient()


    @gen.coroutine
    def index(doc):
        p = partial(
           c.index_doc,
           'test_index',
           'test_doctype',
           serialize(doc),
        )
        res = yield gen.Task(p)
        raise gen.Return(res)


    @gen.coroutine
    def get(doc_id):
        p = partial(
           c.get_doc,
           'test_index',
            doc_id,
        )
        res = yield gen.Task(p)
        raise gen.Return(res)


    @gen.coroutine
    def main_coro():
        res = yield index({"user": "foo", "age": 100})
        doc_id = json.loads(res.body).get('_id', '')
        res = yield get(doc_id)
        print(res.body)


    ioloop.IOLoop.instance().run_sync(main_coro)


.. code-block:: bash

    {"_index":"test_index","_type":"test_doctype","_id":"AVQmGdzo66UC-UgKXqlX","_version":1,"found":true,"_source":{"age": 100, "user": "foo"}
    }


Python Compatibility
--------------------
Tested with python:
2.6, 2.7, 3.2, 3.3, 3.4, 3.5 and pypy


License
-------
Copyright 2014-2016 Daniel Hodges

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


Requirements
------------
.. image:: https://requires.io/github/hodgesds/elasticsearch_tornado/requirements.svg?branch=master
    :target: https://requires.io/github/hodgesds/elasticsearch_tornado/requirements/?branch=master
    :alt: Requirements Status


Build status
------------
.. image:: https://travis-ci.org/hodgesds/elasticsearch_tornado.svg?branch=master
    :target: https://travis-ci.org/hodgesds/elasticsearch_tornado
