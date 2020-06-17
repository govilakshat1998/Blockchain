import hashlib
import datetime,json
from random import randint
import sqlite3
from passlib.hash import sha256_crypt
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
import pickle

class Block():
    def __init__(self, dat, prevhash):
        self.nonce = 0       
        self.data = dat
        self.prev_hash = prevhash
        self.hash = self.get_hash()
    
    def get_hash(self):
        db = None
        with open('users.db','rb') as u:
           db = str(pickle.dumps(u.read()))
        id = (db + str(pickle.dumps(self.data)) + self.prev_hash + str(self.nonce)).encode('utf-8')
        return hashlib.sha256(id).hexdigest()
    
    def mineBlock(self, diff):
        temp_hash = self.get_hash()
        target = '0'*diff
        while not temp_hash.startswith(target):
            self.nonce += 1
            temp_hash = self.get_hash()
        self.hash = temp_hash
        return self.hash
    
    def isBlockMined(self, diff):
        target = '0'*diff
        return self.hash.startswith(target)


class Chain():
    
    def __init__(self):
        self.size = 0
        self.blocks = []
        self.prevhash = ''
        self.difficulty = 2
        
    def add_block(self, new_block):
        self.prevhash = new_block.hash
        print(new_block.hash)
        self.blocks.append(new_block)
        self.size += 1
    

    def verifyTransaction(self):
      if(blockchain.size == 0):
        return True
      else:
        if not blockchain.blocks[blockchain.size-1].isBlockMined(self.difficulty):
          return False
        if(blockchain.blocks[blockchain.size-1].get_hash() != blockchain.blocks[blockchain.size-1].hash):
          return False
        else:
          return True

def createBlock(data, prevhash):
  new_block = Block(data, prevhash)
  return new_block

def viewUser(vid):
  votedflag = 0
  pid = 0
  for i in range(blockchain.size):
    vote = blockchain.blocks[i].data
    if(vote['voter_id'] == vid):
      votedflag = 1
      pid = vote['party_id']
      return votedflag, pid
  return votedflag, pid


app = Flask(__name__)
app.secret_key = "Cryptography"

@app.route('/')
def index():
   return render_template("index.html")

@app.route('/login',methods = ['POST','GET'])
def login():
   if not blockchain.verifyTransaction():
      return render_template("index.html",msg="Database Tampered")
   if request.method == 'POST':
      conn = sqlite3.connect('users.db')
      vid = request.form['VoterID']
      session['vid'] = vid
      pwd = request.form['password']

      query = "SELECT * FROM users WHERE `vid`='" + vid + "'"
      cur = conn.execute(query)
      data = cur.fetchone()
      password = data[1]
      votedflag = data[2]

      if not sha256_crypt.verify(pwd, password):
        return render_template("index.html", msg="Password is incorrect")
      if votedflag == 0:
         conn.close()
         return render_template("voting.html")   
      conn.close()
      return render_template("index.html",msg="You have already voted")
   else:
      return redirect(url_for('index'))

@app.route('/validate',methods = ['POST', 'GET'])
def validate():
   if request.method == 'POST':
      conn = sqlite3.connect('users.db')
      vid=session['vid']
      pid=request.form['vote']
      time=datetime.datetime.now()
      time=str(time)
      query="update users set `voted`=1 where `vid`='"+vid+"'"

      if not blockchain.verifyTransaction():
        return render_template("index.html",msg="Database Tampered")

      conn.execute(query)
      conn.commit()
      print(conn.total_changes)
      vote = {}
      vote['voter_id']=vid
      vote['party_id']=pid
      vote['timestamp']=time
      session.pop('vid', None)
      conn.close()
      print(json.dumps(vote))
      blk = createBlock(vote, blockchain.prevhash)
      blk.mineBlock(blockchain.difficulty)
      blockchain.add_block(blk)
      with open('blockchain','wb') as f:
         pickle.dump(blockchain, f)
      return render_template("index.html",msg="Thanks For Voting")
   else:
      return redirect(url_for('index')) 

@app.route('/insert_db',methods = ['POST', 'GET'])
def insert_db():
  if request.method == 'POST':
    conn = sqlite3.connect('users.db')
    vid = request.form['VoterID']
    password = sha256_crypt.encrypt(str(request.form['password']))
    votedflag = 0
    query = "INSERT INTO users(`vid`,`pwd`,`voted`) VALUES('"+vid+"','"+password+"','"+str(votedflag)+"')"
    curs = conn.execute(query)
    conn.commit()
    conn.close()
  return render_template("insert_db.html")

@app.route('/view_user',methods = ['POST', 'GET'])
def view_user():
  party = ""
  voted = ""
  if request.method == 'POST':
    vid = request.form['VoterID']
    votedflag, pid = viewUser(vid)
    if(votedflag == 1):
      voted = "Yes"
      if(pid == '1'):
        party = "Bhartiya Janata Party"
      if(pid == '2'):
        party = "Indian National Congress"
      if(pid == '3'):
        party = "Bahujan Samaj Party"
      if(pid == '4'):
        party = "Communist Party of India"
    else:
      voted = "No"

  return render_template("view_user.html", partyname = party, votedflag = voted)


if __name__ == '__main__':
   blockchain = None
   try:
      with open('blockchain','rb') as f:
         blockchain = pickle.load(f)
   except:
      blockchain = Chain()
   app.run(debug = True)