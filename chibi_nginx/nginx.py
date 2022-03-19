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
    return "\n".join( iter_to_string( d, tabs=tabs ) )


def iter_to_string( d, tabs=0 ):
    t = '\t' * tabs
    for k, v in d.items():
        if isinstance( v, dict ):
            yield f'{t}{k}' + ' {'
            yield from iter_to_string( v, tabs=tabs + 1 )
            yield f'{t}' + '}'
        elif isinstance( v, list ):
            for vv in v:
                if isinstance( vv, dict ):
                    yield f'{t}{k}' + ' {'
                    yield from iter_to_string( vv, tabs + 1 )
                    yield f'{t}' + '}'
                else:
                    yield f'{t}{k} {vv};'
        else:
            yield f'{t}{k} {v};'


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
