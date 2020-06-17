# Application of Blockchain Tecnology in Online Voting System

# Using the GUI

We have implemented a GUI using the Flask library in python. To run the GUI, simply open the terminal in the main directory of this application. Run the 'app.py' file using the following command:

```sh
python app.py
```

Now, open your browser and navigate to:

localhost:5000/

### Login ###

You will be redirected to the login page. We already have a database file where the voterID is the ID no. and password is the name of the people who have worked on this project. Here are the voter ID and Passwords:

VID        Password  
462        garvit  
500        adrian  
502	       govil  

NOTE: Once, you caste a vote, this database will be considered final. No more users can be added and the votes will be final. If you tamper the database after casting even one vote from whichever user it be, the application fails to verify the blockchain as integrity is lost. If you want to update the database before voting, jump to 'Insert in database' section. 

You can now login and vote for your desired candidate. You will be redirected to the main login page with either of these 3 messages:
1. "Thanks for Voting"
	If you are greeted with this message, your vote has successfully been casted and stored in the blockchain. Bare in mind, the candidate you have voted for remains in the blockchain and not the database.
2. "You have already voted"
	If you had already given a vote, you cannot give another vote.
3. "Database Tampered"
	This means that someone had altered the present database and hence, no more votes can be casted.

### Insert In Database ###

NOTE: Only insert if no vote has been casted yet. Else, integrity of the blockchain is lost.

To insert any voter in the database, for a convinience factor we have created another page inaccessible with any navigation buttons. 
Navigate to:

localhost:5000/insert_db

Here, just enter a voterID and a password. The database only consists of there columns: vid - voterID, pwd - A hashed value of password, voted - A bit value set if a vote is casted.

### View the User Transactions ###

Again, for ease of use, we have a page accessible only via a URL. Simply navigate to:

localhost:5000/view_user

Just enter the voterID present in the database and it will tell you the party you have voted for.


### Implementation of Blockchain ###

We created 2 classes, namely 'Block' and 'Chain'. Chain has a list of blocks as a major attribute and Block contains various attributes like the data and hash of the block.
The 4 major functions are:

- createBlock()

	This function calls the constructor of the Block class. It takes parameters data and previous hash. It helps create a block for each transaction that takes place. In this application, for every vote casted.

- verifyTransaction()

	A part of the Chain class, before every vote is casted and put in the chain, the transaction is validated by checking whether the database is tampered or not. This is done by checking the hash of the previous block and the current hash before adding transaction to the block and updating the database. If they are equal, integrity till now has been maintained.

- mineBlock()

	A part of the process before adding block to chain, we use the mineBlock() function which gives us a proof of work by using the difficulty attribute of the Chain class and hash of the block. Again, ensures the blockchain integrity and difficulty.

- viewUser()

	the viewUser function is used to access the chain and find the corresponding voterID in the chain (If that person has casetd a vote), and return the transaction details including who the voter has voted for.
