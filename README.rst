===========
chibi_nginx
===========


.. image:: https://img.shields.io/pypi/v/chibi_nginx.svg
        :target: https://pypi.python.org/pypi/chibi_nginx

.. image:: https://img.shields.io/travis/dem4ply/chibi_nginx.svg
        :target: https://travis-ci.org/dem4ply/chibi_nginx

.. image:: https://readthedocs.org/projects/chibi-nginx/badge/?version=latest
        :target: https://chibi-nginx.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


python lib for parse nginx conf files


* Free software: WTFPL
* Documentation: https://chibi-nginx.readthedocs.io.


=======
Install
=======


.. code-block:: bash

	pip install chibi-nginx


=====
Usage
=====


.. code-block:: bash

	cat > /etc/nginx/sites_available/default.conf << 'endmsg'
	# vi: set ft=nginx:
	server {
			server_name $hostname nginx;
			listen 80;

			access_log /var/log/nginx/default_access.log;
			error_log /var/log/nginx/default_error.log;

			root /var/www/default/;
			index index.html;
	}
	endmsg


.. code-block:: python

	from chibi_nginx import Chibi_nginx

	tmp = Chibi_nginx( '/etc/nginx/sites_available/default.conf' )
	result = tmp.read()
	expected = {
		'server': {
			'server_name': '$hostname nginx',
			'listen': '80',
			'access_log': '/var/log/nginx/default_access.log',
			'error_log': '/var/log/nginx/default_error.log',
			'root': '/var/www/default/',
			'index': 'index.html'}
	}
	assert result == expected
	result[ 'server' ][ 'root' ] = '/home/user/default_site/'
	tmp.write( result )
	new_result = tmp.read()
	assert new_result[ 'server' ][ 'root' ] = '/home/user/default_site/'


Features
--------

* read and write config files of nginx
