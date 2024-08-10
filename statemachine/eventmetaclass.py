class Event:
    def __init__( self ):
        self.listeners = [ ]

    def register( self, listener ):
        self.listeners.append( listener )

    def trigger( self, *args, **kwargs ):
        for listener in self.listeners:
            listener( *args, **kwargs )


class EventMetaclass( type ):
    def __new__( cls, name, bases, dct ):
        original_method_one = dct.get( 'method_one' )

        def method_one_wrapper( self, *args, **kwargs ):
            result = original_method_one( self, *args, **kwargs )
            self.event.trigger()
            return result

        if original_method_one:
            dct[ 'method_one' ] = method_one_wrapper

        return super().__new__( cls, name, bases, dct )


class BaseClass( metaclass = EventMetaclass ):
    def __init__( self, event ):
        self.event = event
        self.event.register( self.method_two )

    def method_one( self ):
        print( "Base Method One is activated." )

    def method_two( self ):
        print( "Method Two is now activated by the event." )


class SubClass( BaseClass ):
    def method_one( self ):
        print( "Overridden Method One is activated." )
        # No need to explicitly trigger the event


# Create an event instance
event = Event()

# Instantiate the subclass with the event
example = SubClass( event )

# Call method_one, which will automatically trigger method_two via the event
example.method_one()
