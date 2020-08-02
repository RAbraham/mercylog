from typing import TypeVar, Generic
Error = TypeVar('Error')
Result = TypeVar('Result')
# from pfun.either import Either


# R = TypeVar('R', contravariant=True)
# E = TypeVar('E', covariant=True)
# A = TypeVar('A', covariant=True)


# class Effect(Generic[R, E, A]):
    # def run(self, r: R) -> A:
    #     """
    #     May raise E
    #     """
    #     ...

# validate :: Person -> V (Array Error) Person
# validate person = { first: _, last: _, email: _ }
#   <$> validateName person.first
#   <*> validateName person.last
#   <*> validateEmail person.email

# class V(Generic[Error, Result]):
    # pass


# def validate(person: Person):
    # person % validate_name person.first * validate_name person.last * validate_email person.email