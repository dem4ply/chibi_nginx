#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from chibi_nginx.nginx import parse, to_string


nginx_content = """
worker_processes  2;

# set open fd limit to 30000
worker_rlimit_nofile 30000;

events{
	worker_connections 10000;
	accept_mutex off;
}

http {
	include /etc/nginx/conf.d/*.conf;
	include mime.types;
	default_type json;
	sendfile off;
	keepalive_timeout   65;

	access_log /var/log/nginx/access.log upstream_time;
	error_log /var/log/nginx/error.log;

	server {
		listen 80 default_server;
		return 444;
	}

	include /etc/nginx/sites_enabled/*;

}
"""


nginx_to_string_expected = """worker_processes 2;
worker_rlimit_nofile 30000;
events {
	worker_connections 10000;
	accept_mutex off;
}
http {
	include /etc/nginx/conf.d/*.conf;
	include mime.types;
	include /etc/nginx/sites_enabled/*;
	default_type json;
	sendfile off;
	keepalive_timeout 65;
	access_log /var/log/nginx/access.log upstream_time;
	error_log /var/log/nginx/error.log;
	server {
		listen 80 default_server;
		return 444;
	}
}"""

nginx_expected = {
    'events': {
        'accept_mutex': 'off', 'worker_connections': '10000'
    },
    'http': {
        'access_log': '/var/log/nginx/access.log upstream_time',
        'default_type': 'json',
        'error_log': '/var/log/nginx/error.log',
        'include': [
            '/etc/nginx/conf.d/*.conf',
            'mime.types',
            '/etc/nginx/sites_enabled/*' ],
        'keepalive_timeout': '65',
        'sendfile': 'off',
        'server': {
            'listen': '80 default_server',
            'return': '444'
        }
    },
    'worker_processes': '2',
    'worker_rlimit_nofile': '30000'
}



class Test_chibi_nginx( unittest.TestCase ):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_should_work(self):
        data = parse( nginx_content )
        self.assertEqual( data, nginx_expected )

    def test_to_string_should_work(self):
        data = parse( nginx_content )
        result = to_string( data )
        self.assertEqual( result, nginx_to_string_expected )
