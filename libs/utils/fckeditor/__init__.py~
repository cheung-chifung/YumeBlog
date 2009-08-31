# Register as a namespace package if pkg_resources is available
try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    pass
