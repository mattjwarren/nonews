'''
Created on 15 Nov 2012

@author: matt
'''
def raise_missing_args(required_args,received_args,raise_exception=True):
    '''if raise_exception is True then raise exception if missing args. Otherwise
    return a list of missing args, or an empty list if there are none.'''
    if type(required_args) is dict:
        required_args=required_args.keys()
    required_args=set(required_args if required_args else [])
    received_args=set(received_args.keys() if received_args else [])
    missing_args=required_args-received_args
    if missing_args and raise_exception:
        raise Exception("Missing keyword args: %s" % ','.join(missing_args))
    
def set_args(instance,args,keyvalues):
    for arg in args if args else []:
        if type(args) is dict:
            default=args[arg]
        try:
            setattr(instance,arg,keyvalues[arg])
        except KeyError:
            try:
                setattr(instance,arg,default)
                del(default)
            except NameError:
                raise Exception("Argument %s not found." % arg)
            
def process_kwargs(instance,required_args,args_with_defaults,keywords):
        """Raise eception for missing args, if no args missing then
        set them as attributes on instance"""
        
        #<required args>        
        raise_missing_args(required_args,keywords)
        set_args(instance,required_args,keywords)
        #</required args>

        #<args with defaults>
        set_args(instance,args_with_defaults,keywords)
        #</args with defaults>