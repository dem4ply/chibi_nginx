# -*- coding: utf-8 -*-
from chibi.atlas.multi import Chibi_atlas_multi


def parse( content ):
    content = filter( bool, content.split( '\n' ) )
    content = filter( lambda x: not x.startswith( '#' ), content )
    content = map( str.strip, content )
    content = list( content )
    asdf = iter( content )
    result = parse_internal( asdf )
    return result


def to_string( d, tabs=0 ):
    result = []
    t = '\t' * tabs
    for k, v in d.items():
        if isinstance( v, dict ):
            result.append( f'{t}{k}' + ' {' )
            result.append( to_string( v, tabs=tabs + 1 ) )
            result.append( f'{t}' + '}' )
        elif isinstance( v, list ):
            for vv in v:
                result.append( f'{t}{k} {vv};' )
        else:
            result.append( f'{t}{k} {v};' )
    return "\n".join( result )


def parse_internal( content_iter ):
    result = Chibi_atlas_multi()
    for line in content_iter:
        if '{' in line:
            line = line.strip( ' {}' )
            result[ line ] = parse_internal( content_iter )
        elif '}' in line:
            return result
        else:
            content = line.split( ' ', 1 )
            content = filter( bool, content )
            content = map( str.strip, content )
            content = list( content )
            result[ content[0] ] = clean_value( content[1:] )
    return result


def clean_value( content ):
    if len( content ) == 1:
        result = content[0]
        result = result.rstrip( ';' )
    else:
        raise NotImplementedError()
    return result
