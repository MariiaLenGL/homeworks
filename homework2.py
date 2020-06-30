#!/usr/bin/python

"""
Homework 2:
Создать ряд классов, --> указывает на класс родитель
NetworkClient <-- BaseServer <-- Server <-- BuildServer
NetworkClient <-- BaseClient <-- Client <-- BuildCLient
Build --> BuildClient, BuildServer

Классы  NetworkClient,  Server,  BuildClient и Build должны иметь метод ping.
В каждом из которых принтится имя класса из которого вызывается метод и также возвращается имя класса.
Метод ping класса  Build поочередно вызывает методы ping классов:
BuildClient,  NetworkClient и  BuildClient и возвращает результат всех вызовов.
"""

class NetworkClient:
    
    @classmethod
    def ping(cls):
        class_name = cls.__name__
        print('Method was called from class {}'.format(class_name))
        return class_name
        
class BaseServer(NetworkClient):
    pass

class Server(BaseServer):
    pass

class BuildServer(Server):
    pass

class BaseClient(NetworkClient):
    pass

class Client(BaseClient):
    pass

class BuildClient(Client):
    pass

class Build(BuildServer, BuildClient):
    
    @classmethod
    def ping(cls):
        result = [BuildClient.ping(), NetworkClient.ping(), BuildServer.ping()] 
        return result       


if __name__ == "__main__":
    NetworkClient.ping()
    Server.ping()
    Build.ping()