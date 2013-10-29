#!/usr/bin/python
# coding=UTF-8
'''
Created on 2013年10月20日

@author: lichunxi
'''
from bottle import post, get, put, request, run
import account

@post('/account')
def createAccount():
    name = request.forms.get("userName")
    passwd = request.forms.get("passwd")
    wallet = request.forms.get("wallet")
    account.create(name, passwd, wallet)
    
@get('/account')
def queryAccount():
    name = request.query.get("userName")
    passwd = request.query.get("passwd")
    return account.queryByName(name, passwd)

@get('/account/check')
def checkAccount():
    name = request.query.get("userName")
    passwd = request.query.get("passwd")
    return {'result':account.check(name, passwd)}

@put('/account/passwd')
def changePasswd():
    name = request.query.get("userName")
    oldPasswd = request.query.get("oldPasswd")
    newPasswd = request.query.get("newPasswd")
    return {'result':account.updatePasswd(name, oldPasswd, newPasswd)}

# def _toDict(obj):
#     _dict = {}
#     _dict.update(obj.__dict__)
#     return _dict

run(host='localhost', port=8080)
