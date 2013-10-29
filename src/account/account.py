#!/usr/bin/python
# coding=UTF-8
'''
Created on 2013年10月19日

@author: lichunxi
create table account(
  accountId bigint unsigned not null auto_increment,
  name varchar(100) not null unique,
  wallet varchar(256) not null,
  passwd varchar(256) not null,
  privateKey varchar(512) not null,
  publicKey varchar(512) not null,
  primary key (accountId)
);
'''
from sqlalchemy import MetaData, Table, create_engine, Column, String, Integer, and_
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy.orm.exc import NoResultFound
from hashlib import sha256
import rsa

conn_str = "mysql+mysqldb://zhebei:zhebei@127.0.0.1:3306/zhebei?charset=utf8"
db = create_engine(conn_str, echo=True)
#base = declarative_base()
Session = sessionmaker(bind=db)
session = Session()

metadata = MetaData()

accountTable = Table('account', metadata,
            Column('accountId', Integer, primary_key=True),
            Column('name', String, unique=True, nullable=False),
            Column('wallet', String, nullable=False),
            Column('passwd', String, nullable=False),
            Column('privateKey', String, nullable=False),
            Column('publicKey', String, nullable=False),
        )

class Account(object):
    
#     __tablename__ = 'account'
#     
#     accountId = Column(Integer, primary_key=True)
#     name = Column(String, unique=True, nullable=False)
#     wallet = Column(String, nullable=False)
#     passwd = Column(String, nullable=False)
#     privateKey = Column(String, nullable=False)
#     publicKey = Column(String, nullable=False)
    
    def __init__(self, name, wallet, passwd, privateKey, publicKey):
        self.name = name
        self.wallet = wallet
        self.passwd = passwd
        self.privateKey = privateKey
        self.publicKey = publicKey
        
    def __repr__(self):
        return "<Account('%s','%s','%s','%s','%s','%s')>" % (self.accountId, self.name, self.wallet, self.passwd, self.privateKey, self.publicKey)

mapper(Account, accountTable)

def create(name, passwd, wallet):
    (publicKey, privateKey) = genKeypair()
    account = Account(name, wallet, passwd, privateKey, publicKey)
    session.add(account)
    session.commit()
    
def update(accountId, name, wallet, privateKey, publicKey):
    session.query(Account).filter(Account.accountId == accountId).update({Account.name:name, Account.wallet:wallet, Account.privateKey:privateKey, Account.publicKey:publicKey})
    session.commit()
    
def updatePasswd(name, oldPasswd, newPasswd):
    try:
        session.query(Account).filter(and_(Account.name == name, Account.passwd == oldPasswd)).update({Account.passwd:newPasswd})
        session.commit()
        return True
    except NoResultFound, ex:
        print ex
        return False
    
def queryById(accountId):
    try:
        account = session.query(Account).filter(Account.accountId == accountId).one()
        return _accountMap(account)
    except NoResultFound, ex:
        print ex
        return {}

def queryByName(name, passwd):
    try:
        account = session.query(Account).filter(and_(Account.name == name, Account.passwd == passwd)).one()
        return _accountMap(account)
        #a = Account(account.name, account.wallet, account.passwd, account.privateKey, account.publicKey)
    except NoResultFound, ex:
        print ex
        return {}

def queryAll(page=1, length=200):
    '''分页查询所有的记录
       :param page:起始页码
       :param length:每页长度
    '''
    if page == 1:
        accountList = session.query(Account).order_by(Account.accountId).limit(length)
    else:
        accountList = session.query(Account).order_by(Account.accountId).limit(length).offset((page - 1) * length)
    accounts = []
    for account in accountList:
        accounts.append(_accountMap(account))
    return accounts

def deleteById(accountId):
    account = queryById(accountId)
    if account:
        session.delete(account)
        session.commit()

def check(name, passwd):
    '''检查该用户名和密码是否存在，如果不存在，返回False，如果存在，返回True
    :param name:用户名
    :param passwd:采用sha256算法对用户输入的密码做签名后的字符串
    '''
    try:
        session.query(Account).filter(and_(Account.name == name, Account.passwd == passwd)).one()
        return True
    except NoResultFound, ex:
        print ex
        return False

def _accountMap(account):
    _dict = {}
    _dict['name'] = account.name
    _dict['passwd'] = account.passwd
    _dict['wallet'] = account.wallet
    _dict['privateKey'] = account.privateKey
    _dict['publicKey'] = account.publicKey
    return _dict

def genHashPasswd(passwd):
    return sha256(passwd).hexdigest()

def genKeypair():
    return rsa.newkeys(512, poolsize=8)

if __name__ == '__main__':
    
    create('lichunxi5', 'lcx46@163.com', genHashPasswd('test'))
    
    # for account in queryAll(1, 10):
    #    print account.accountId, account.name, account.wallet, account.passwd, account.privateKey, account.publicKey
        
    print check('lichunxi', genHashPasswd('test'))
    # print queryById('4')
    # update('4', 'lichunxi2', 'lcx46@163.com', privateKey, publicKey)
        
    # deleteById('4')
    # for account in queryAll(1,100):
    #    print account.accountId, account.name, account.wallet, account.privateKey, account.publicKey
    
