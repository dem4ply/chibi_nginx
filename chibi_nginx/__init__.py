# -*- coding: utf-8 -*-
from chibi.file import Chibi_file
from chibi_nginx.nginx import parse, to_string


__author__ = """dem4ply"""
__email__ = 'dem4ply@gmail.com'
__version__ = '0.2.0'


class Chibi_nginx( Chibi_file ):
    def read( self ):
        string = super().read()
        result = parse( string )
        return result

    def write( self, data ):
        result = to_string( data )
        super().write( result )
