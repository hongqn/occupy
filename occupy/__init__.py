from occupy.resource import Resource, scan_package
import occupy.types
from occupy.functions import read

scan_package(occupy.types)
globals().update(Resource.registry)

__all__ = list(Resource.registry.keys())
__all__ += ['read']
