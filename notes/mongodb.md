# Introduction to MongoDb

## Reading

- [NoSQL Distilled](http://learning.acm.org/books/book_detail.cfm?id=2381014&type=safari) chapter 9
- [MongoDb server docs](https://docs.mongodb.com/manual/)
- [MongoDb Drivers for various languages](https://docs.mongodb.com/ecosystem/drivers)
- [Mongo shell reference](https://docs.mongodb.com/manual/reference/method/)

### Reading questions

-

## Notes

MongoDb is a premier document-based database with many features.

### Setting up

You can run MongoDb in various ways:

- You can [install](https://docs.mongodb.com/manual/installation/) it locally to your computer.
- You can play around in an [online shell](https://www.tutorialspoint.com/codingground.htm).
- You can create an account with [mlab](https://mlab.com).

We will follow this last method. You gain access to 500MB space for free. Here are the steps:

- Follow the above link for [mlab](https://mlab.com) and sign up. Notice that you have an "account name", think of it as a group name, and it's separate from your username. For example your instructor used `wranglingclass` for the account name.
- You will also need to verify the email address. Check your email and click the link there.
- When you log in, you will be presented with your (empty) list of "deployments". We will create a new one by clicking on the "Create new" button.
- You can choose between three "cloud providers". They all offer a 500MB free "sandbox" option, choose whichever you like. Your instructor chose the Google Cloud Platform option.
- Make sure to choose "Single node" and Sandbox.
- Choose a database name. Your instructor named theirs "wrangling".
- Click the Create button to finalize the setup.
- Congratulations! You now have your first cloud-storage-based database in place. Let's learn how to access it.
- Click on the newly created deployment, and a new page will appear with information on how to access it.
- Click on the Users tab and add a new user for the database. You will use these credentials to remotely access the database later on.

### Using the mongo shell

There are two standard ways to interact with your Mongodb database. In this section we'll use the `mongo` shell.

- Open up a terminal.
- At the top of the mlab webpage with your deployment you'll see a link like: `mongo ds011168.mlab.com:11168/wranging -u <dbuser> -p <dbpassword>`. Yours will have a different database number probably. You'll need to paste that link and change the `<dbuser>` and `<dbpassword>` entries to your setup.
- You should now be presented with a welcome message. This is an interactive shell from where you can ask for details from the database. Start by typing:
    ```
    db
    ```
    which should show you the name of the database you are currently using. In general `db` is like an "object" that we will use to access the current database.
- We will now create a new **collection**. Collections are like tables in mysql. But since there is no strict form that documents in MongoDb need to follow, we don't need to really specify anything about the collection. We just start using it. We're going to call our collection "gpas". Here is how we can add an entry to it:
    ```
    db.gpas.insert({ name: 'student0', gpa: _rand() * 4 })
    db.gpas.find()
    ```
    You should get back a response that shows you the new stored document, and it will also contain a "ObjectId". This is an automatically generated by MongoDb. We could also manually generate it, but we will never have a need to do so.
- Let's remove the entry we added:
    ```
    db.gpas.remove({ name: 'student0' })
    ```
- The MongoDb shell uses a mini programming language that looks a bit like Javascript, for those familiar with Javascript. For example we used `_rand()` to generate a random number. We will now insert a large number of values all at once. We first create them as a "Javascript" object:
    ```js
    var d = []; for (var i = 0; i < 10000; i++) {
      d.push({ name: "student" + i, gpa: _rand()*4 })
    }
    db.gpas.insertMany(d)
    ```
- Let us now learn how to search for information in the documents. The main tool at our disposal is the `find` method. Its parameter is an object that describes the query. For example we can get the entries with a specific student name:
    ```js
    db.gpas.find({ name: 'student100' })
    ```
    or we can perform more complex queries. For example, this asks for all entries whose gpa is over 3.95:
    ```js
    db.gpas.find({ gpa: { $gt: 3.98 }})
    ```
    The shell will probably link only some of the results. We will discuss how to work with the result of a `find`, which is what is known as a *cursor*. In the meantime, if we only want to know how many results there are, we can use `count`:
    ```js
    db.gpas.count({ gpa: { $gt: 3.98 }})
    ```
- Next we will do an update query: We will add an "atRisk" field to all students with a gpa of 2 or less. The query takes two parameters: The first specifies which entries to locate, the other specifies what changes to make.
    ```js
    db.gpas.updateMany({ gpa: { $lte: 2 }}, { $set: { atRisk: true }})
    ```
    We'll see that about half of the documents were updated. Now half the documents have this "atRisk" field, while the other half don't have it at all.
- Let us now do a more complex query, that captures all students whose gpa is less than 2.5, and adjusts that gpa by up to plus/minus 1 point.
    ```js
    db.gpas.updateMany({ gpa: { $lte: 2.5 }}, { $inc: { gpa: _rand() * 2 - 1 }})
    ```
    Now we will look for students who were at-risk but whose gpa is now over 2. We will then mark all those to no-longer at risk:
    ```js
    db.gpas.count({ gpa: { $gt: 2 }, atRisk: true })
    db.gpas.updateMany({ gpa: { $gt: 2 }, atRisk: true }, { $set: { atRisk: false }})
    ```
    Now we want to search for all students that are not at risk. We cannot simply look for `atRisk: false` because this doesn't include those students where there is no `atRisk` entry at all. We can do this in two ways:
    ```js
    db.gpas.count({
      $or: [
        { atRisk: { $exists: false } },
        { atRisk: false }
      ]
    })

    db.gpas.count({
      atRisk: { $ne: true }
    })
    ```
- We will now arbitrarily assign all students into four groups. This may take a while as it has to update each entry:
    ```true
    db.gpas.find().forEach(function(doc) {
      db.gpas.update(doc, { $set: { group: Math.ceil(_rand() * 4) }})
    })
    ```
    This is also the first time where we say the use of a *cursor method*: The result of the `find` call is a "cursor", which is basically a fancy word for something that we can iterate over. We therefore perform a `forEach` on it. That takes an arbitrary function as input, and it executes that function for every result. Let's see how the above worked. Everyone should be more or less equally divided into four "groups", identified by the numbers 1 through 4:
    ```true
    for (var i = 1; i < 5; i++) {
      print(db.gpas.count({ group: i }))
    }
    ```

Some practice problems:

- Find out how many students in each group are at risk.
- Find out how many students have a gpa of 2.0 or below and are marked as at-risk. These students were at risk before we changed the grades, and still are.
- Find out how many students have a gpa of 2.0 or below and are not marked as at-risk.
- Mark those students from the previous part as being at-risk.
- Remove from the collection all students with a gpa less than 1.
- Find all at-risk students and put them in their own "group", with number 5.