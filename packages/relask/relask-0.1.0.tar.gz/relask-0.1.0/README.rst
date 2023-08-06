===============================
Relask
===============================

.. image:: https://img.shields.io/pypi/v/relask.svg
        :target: https://pypi.python.org/pypi/relask

.. image:: https://img.shields.io/travis/decentfox/relask.svg
        :target: https://travis-ci.org/decentfox/relask

.. image:: https://readthedocs.io/projects/relask/badge/?version=latest
        :target: https://readthedocs.io/projects/relask/?badge=latest
        :alt: Documentation Status

.. image:: https://requires.io/github/decentfox/relask/requirements.svg?branch=master
        :target: https://requires.io/github/decentfox/relask/requirements?branch=master
        :alt: Dependencies


A Relay-based web development kit on Flask.

* Free software: BSD license
* Documentation: https://relask.readthedocs.io.

Features
--------

* Fast web development setup with ES6, React and Relay
* Batteries included: React Router, Webpack and Babel
* Server is powered by Python, Flask and Graphene
* JWT integrated, with a working example using Flask-Login

Usage
-----

1. Install Relask:

.. code:: bash

  pip install git+https://github.com/decentfox/relask

2. Create a Flask application, for example: http://flask.pocoo.org/docs/quickstart/

3. Initialize your Flask application with Relask (this requires `npm`):

.. code:: bash

  FLASK_APP=xxx flask init-relask

4. Under the root path of your Flask application, create `scripts/app.js` with something like this:

.. code:: javascript

  import React from "react";
  import ReactDOM from "react-dom";
  import {Route, IndexRoute} from "react-router";
  import Relay from "react-relay";
  import {Relask, RelayContainer} from "babel-loader!relask";


  @RelayContainer
  class Hello extends React.Component {
      render() {
          return (
              <div>Hello, {this.props.hello.name}!</div>
          );
      }

      static relay = {
          fragments: {
              hello: () => Relay.QL`fragment on Hello { name }`
          }
      };
  }

  ReactDOM.render((
      <Relask>
          <Route path="/" component={Hello} queries={{
              hello: () => Relay.QL`query { hello }`
          }}/>
      </Relask>
  ), document.getElementById('app'));

5. Initialize the Relask extension with something like this:

.. code:: python

  import graphene
  from flask import Flask
  from graphene import relay
  from relask import Relask


  class Hello(relay.Node):
      name = graphene.String()

      def resolve_name(self, args, info):
          return 'World'

      @classmethod
      def get_node(cls, id, info):
          return Hello(id=id)


  class Query(graphene.ObjectType):
      node = relay.NodeField()
      hello = graphene.Field(Hello)

      def resolve_hello(self, args, info):
          return Hello.get_node(1, None)


  app = Flask(__name__)
  relask = Relask(app)
  relask.schema.query = Query

6. See your result with one command - don't worry about webpack any more:

.. code:: bash

  FLASK_APP=xxx flask run


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
