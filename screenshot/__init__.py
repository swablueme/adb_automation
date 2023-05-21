import os
#this loads all modules in the folder
__all__ = [ basename(f)[:-3] for f in os.listdir() if os.path.isfile(f) and not f.endswith('__init__.py') and f.endswith(".py")]
