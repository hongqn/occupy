from occupy.resource import Resource, scan_package
import occupy.types

scan_package(occupy.types)
globals().update(Resource.registry)
__all__ = Resource.registry.keys()

