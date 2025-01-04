#!python3
# -*- coding: utf-8 -*-

"""
Found on
https://bugs.python.org/issue2480 and updated for py3 and minor readability.
"""

import io
import pickle

class LazySave( object ):
    '''Out of band marker for lazy saves among lazy writes.'''
    def __init__( self, obj ):
        self.obj = obj
    def __repr__( self ):
        return f"<LazySave {self.obj}>"

class LazyMemo( object ):
    '''Out of band marker for lazy memos among lazy writes.'''
    def __init__( self, obj ):
        self.obj = obj
    def __repr__( self ):
        return f"<LazyMemo {self.obj}>"

MEMOIMPORTANT = True # turning this on creates pickles identical to the
# original implementation -- otherwise the memo ids are in a different order

class NonrecursivePickler( pickle._Pickler ):

    def __init__( self, file, protocol=None ):
        pickle._Pickler.__init__( self, file, protocol )
        self.lazywrites = []
        self.realwrite = file.write

        # TODO: this creates a reference loop and prevents gc
        self.write = self.lazywrite

    def lazywrite( self, *args ):
        if self.lazywrites:
            self.lazywrites.append( args )
        else:
            self.realwrite( *args )

    def save( self, obj ):
        self.lazywrites.append( LazySave( obj ) )

    realsave = pickle._Pickler.save

    def lazymemoize( self, obj ):
        """Store an object in the memo."""
        if self.lazywrites:
            self.lazywrites.append( LazyMemo( obj ) )
        else:
            self.realmemoize( obj )

    if MEMOIMPORTANT:
        memoize = lazymemoize
    realmemoize = pickle._Pickler.memoize

    def dump(self, obj):
        """Write a pickled representation of obj to the open file."""
        if self.proto >= 2:
            self.write( pickle.PROTO + chr( self.proto ).encode('ascii') )
        self.realsave( obj )
        while self.lazywrites:
            lws = self.lazywrites
            self.lazywrites = []
            while lws:
                lw = lws.pop( 0 )
                if type( lw ) is LazySave:
                    self.realsave( lw.obj )
                    if self.lazywrites:
                        self.lazywrites.extend( lws )
                        break
                elif type( lw ) is LazyMemo:
                    self.realmemoize( lw.obj )
                else:
                    self.realwrite( *lw )
        self.realwrite( pickle.STOP )


def dumps(obj, protocol=pickle.DEFAULT_PROTOCOL):
    f = io.BytesIO()
    p = NonrecursivePickler(f, protocol=protocol)
    p.dump(obj)
    return f.getvalue()

