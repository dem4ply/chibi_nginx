import unittest

from chibi_nginx.nginx import parse, to_string


nginx_content = """
upstream some_upstream {
	server some_host:8000 fail_timeout=1;
}

server {
	listen 80;
	server_name server_name.com;
	return 301 https://server_name.com$request_uri;

	access_log /var/log/nginx/http__some_host.log upstream_time;
	error_log /var/log/nginx/http__some_host_error.log;
}

server {
	listen 443 ssl;
	client_max_body_size 4G;
	server_name some_host.com;

	ssl_certificate /etc/nginx/cert/cert.com.crt;
	ssl_certificate_key /etc/nginx/cert/cert.com.key;

	ssl on;
	ssl_session_cache builtin:1000  shared:SSL:10m;
	ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
	ssl_ciphers HIGH:!aNULL:!eNULL:!EXPORT:!CAMELLIA:!DES:!MD5:!PSK:!RC4;
	ssl_prefer_server_ciphers on;

	access_log /var/log/nginx/some_host_react.log upstream_time;
	error_log /var/log/nginx/some_host_error.log;

	keepalive_timeout 5;

	location / {
		proxy_set_header Host $host;
		proxy_set_header X-Forwarded-Host $server_name;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_set_header X-Forwarded-Proto $scheme;

		proxy_pass http://some_host;
	}
}
"""

nginx_expected = {
    'server': [
        {
            'access_log': '/var/log/nginx/http__some_host.log upstream_time',
            'error_log': '/var/log/nginx/http__some_host_error.log',
            'listen': '80',
            'return': '301 https://server_name.com$request_uri',
            'server_name': 'server_name.com'
        },
        {
            'access_log': '/var/log/nginx/some_host_react.log upstream_time',
            'client_max_body_size': '4G',
            'error_log': '/var/log/nginx/some_host_error.log',
            'keepalive_timeout': '5',
            'listen': '443 ssl',
            'location /': {
                'proxy_pass': 'http://some_host',
                'proxy_set_header': [
                    'Host $host',
                    'X-Forwarded-Host ' '$server_name',
                    'X-Real-IP $remote_addr', 'X-Forwarded-For '
                    '$proxy_add_x_forwarded_for',
                    'X-Forwarded-Proto $scheme'
                ]
            },
            'server_name': 'some_host.com',
            'ssl': 'on',
            'ssl_certificate': '/etc/nginx/cert/cert.com.crt',
            'ssl_certificate_key': '/etc/nginx/cert/cert.com.key',
            'ssl_ciphers': (
                'HIGH:!aNULL:!eNULL:!EXPORT:!CAMELLIA:!DES:!MD5:'
                '!PSK:!RC4' ),
            'ssl_prefer_server_ciphers': 'on',
            'ssl_protocols': 'TLSv1 TLSv1.1 TLSv1.2',
            'ssl_session_cache': 'builtin:1000  shared:SSL:10m'
        }
    ],
    'upstream some_upstream': {
        'server': 'some_host:8000 fail_timeout=1'
    }
}


class Test_chibi_nginx_with_ssl( unittest.TestCase ):
    def test_parser_should_work( self ):
        data = parse( nginx_content )
        self.assertEqual( data, nginx_expected )

    def test_parser_should_work_inverse( self ):
        data = parse( nginx_content )
        result = to_string( data )
        expected = "\n".join( filter( bool, nginx_content.split( '\n' ) ) )
        self.maxDiff = None
        self.assertEqual( result, expected )
