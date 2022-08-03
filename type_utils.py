def type_strict(type_test):
    def value_wrapper(value):
        if not isinstance(value, type_test):
            raise TypeError(f"{value} doesn't belong to type {type_test}")
        return value

    return value_wrapper


def type_nullable(type_test):
    def value_wrapper(value):
        if not isinstance(value, type_test) and value is not None:
            raise TypeError(f"{value} doesn't belong to type {type_test}")
        return value

    return value_wrapper


class GeneralDescriptor:
    allowed_type = object
    nullable = True

    def __set_name__(self, owner, name):
        self.name = "__" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if self.nullable:
            m = type_nullable(self.allowed_type)
        else:
            m = type_strict(self.allowed_type)
        setattr(instance, self.name, m(value))


integer_type = type_strict(int)


