from occupy.resource import Type

@Type.register('user')
class User(Type):
    @classmethod
    def iter_all(cls):
        return ['hongqn']
