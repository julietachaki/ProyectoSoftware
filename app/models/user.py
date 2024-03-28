from dataclasses import dataclass

'''
class User
'''

@dataclass(init=False)
class User:
    username :str
    email:str
    password:str