# NL2SQL
NL2SQL seeks to transform natural language questions to SQL, allowing individuals to run unstructured queries against databases.

## Dependencies

* [NLTK](http://www.nltk.org/)
* [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/)
* [Plac](http://micheles.github.io/plac/)
* [Requests](http://docs.python-requests.org/)
* [MySQLdb](http://mysqldb.readthedocs.io)
* [Faker](https://faker.readthedocs.io)
* [NumPy](http://www.numpy.org/)

## Quickstart
```sh
$ pip install -r requirements.txt
$ python nl2sql.py download
$ python nl2sql.py setup
$ python nl2sql.py run
```

Enter sentences to be turned into SQL:

```sh
$ python nl2sql.py run

  Type 'exit' to quit

  How can I help you?

  >: Find several students registered for Constitutional Law
```

```sh
usage: python nl2sql.py {download,setup,run} ...

Command-line interface for NL2SQL

subcommands:
  {download,setup,run}
    download            Download the Stanford CoreNLP tools and related
                        models. Install the needed project dependencies.
    setup               Setup the project as needed.
    run                 Start NL2SQL to parse questions
```

### Download

To download Dependencies (may take a while):
```sh
$ pip install -r requirements.txt
$ python nl2sql.py download
```

Example run:
```sh
$ python nl2sql.py download

  Downloading stanford-corenlp-full-2016-10-31.zip from http://nlp.stanford.edu/software/stanford-corenlp-full-2016-10-31.zip

  [==================================================]
   
  Extracting stanford-corenlp-full-2016-10-31.zip to /Users/.../nl2sql/data

  Extracting stanford-corenlp-3.7.0-models.jar to /Users/.../nl2sql/data/stanford-corenlp-full-2016-10-31/stanford-corenlp-3.7.0-models
```

```sh
usage: python nl2sql.py download [-p PATH] [-f]

    Download the Stanford CoreNLP tools and related models.
    Install the needed project dependencies.

optional arguments:
  -p PATH, --path PATH  Path to download models and jar files (default:
                        ./data)
  -f, --force           Force download of all files
```

### Setup
To setup, first have a MySQL database ready and running, then run:
```sh
$ python nl2sql.py setup
```

Which will prompt you to enter a database information, then prompt you to
import the schema and seed the database.

Next, it will generate the `SchemaGraph` and `DBCorpus` and train all Classifiers and store them via pickle for later use.

Example run:

```sh
$ python nl2sql.py setup

  Setting up NL2SQL.

  Downloading WordNet corpora.

  [nltk_data] Downloading package wordnet to /...
  [nltk_data]   Package wordnet is already up-to-date!

  Configuring Database:

  Enter hostname: LOCALHOST
  Enter MySQL user: ROOT
  Enter MySQL password:
  Enter database name: DATABASE_NAME
  Database does not exist. Create it? [y/n]: y
  Do you want to import the database schema? [y/n]: y
  Do you want to seed the database? [y/n]: y

  Database configured.

  Constructing Database Graph.
  
  Database Graph constructed.
  
  Creating Database Corpus.

  Database Corpus created.

  Training database classifier.

  ==> Training (20 iterations)

      Iteration    Log Likelihood    Accuracy
      ---------------------------------------
             1          -2.70805        0.010
             2          -0.78485        0.974
             ...
            19          -0.10204        1.000
         Final          -0.09748        1.000

  Database classifier trained.

  Training SQL grammar classifier.

  SQL grammar classifier trained.

  Set up complete.

```

```sh
usage: python nl2sql.py setup [-f]

    Setup the project as needed.

optional arguments:
  -f, --force  Force setup to rerun
```

### Run

To start the system, run the two previous commands, then run:
```sh
$ python nl2sql.py setup
```

You will be prompted to enter a statement which will be turned into SQL and executed.

Example Run:
```sh
$ python nl2sql.py run

  Type 'exit' to quit

  How can I help you?

  >: How many sections are located in Rhode Island in Spring 2017?

  +------------+
  | COUNT(*)   |
  +------------+
  | 15         |
  +------------+

   What else would you like to know?

   >:
```

```sh
usage: python nl2sql.py run [-d]

    Start NL2SQL to parse questions

optional arguments:
  -d, --debug  Print out debug statements
```