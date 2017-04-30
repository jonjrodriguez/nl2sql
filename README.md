# NL2SQL
NL2SQL seeks to transform natural language questions to SQL, allowing individuals to run unstructured queries against databases.

## Dependencies

* [NLTK](http://www.nltk.org/)
* [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/)
* [Plac](http://micheles.github.io/plac/)
* [Requests](http://docs.python-requests.org/)
* [MySQLdb](http://mysqldb.readthedocs.io)
* [Faker](https://faker.readthedocs.io)

### Setup

To install Dependencies (may take a while):
```sh
$ pip install -r requirements.txt
$ python nl2sql.py download
```

To setup, first have a MySQL database ready and running, then run:
```sh
$ python nl2sql.py setup
```

Which will prompt you to enter a database information, then prompt you to
import the schema and seed the database.

Example run:

```sh
$ python nl2sql.py setup

  Setting up NL2SQL.


  Configuring Database:

  Enter hostname: LOCALHOST
  Enter MySQL user: ROOT
  Enter MySQL password:
  Enter database name: DATABASE_NAME

  Do you want to import the database schema? [y/n]: y

  Importing Database schema.


  Database schema import complete.


  Do you want to seed the database? [y/n]: y

  Seeding Database with data.

  Creating terms
  Creating campuses
  Creating faculty members
  Creating courses
  Creating sections
  Creating students
  Creating registrations

  Saving seeds to database

  Finished Seeding Database.


  Database configured.


  Set up complete.

```

## NL2SQL Pipeline

To convert natural language to SQL, we will attempt to split up the task into at least three parts. Each one depending on the ones before it. The pipeline will attempt to extract at least one SQL statement out of the given text. It is possible that there may be no SQL statement.

### Question Classification

The first step in creating the NL2SQL interface is to break down the question into subcategories of questions. Doing so would help us define what kind of answer the user is looking for, thus helping us generate SQL. To start, we divided most questions into some categories.

  1. __Yes/No__: These questions generally have a yes/no value as an answer, so the SQL result can expect to be cast as boolean.
  2. __Who__: 'Who' questions probably expect a `PERSON` or a `CORPORATION`.
  3. __What__: 'What' questions probably expect an entity, but probably not a `PERSON`.
  4. __When__: 'When' questions will let us know we're probably looking for a `datetime` or similar data value.
  5. __Num__: These questions will probably want a `COUNT`, `AVG`, `SUM` or something of that nature as the SQL return value.

#### Inputs
As an input, the Classifier takes in a full english statement

#### Outputs
As output, the classifier will return one of the above mentioned categories.

### Parsing

Parsing the statement is the next step of the pipeline. If we have the question classified, we can parse the sentence using a parsing library to try and discover the `SUBJECT` or `SUBJECTS` of the question. This could be useful to identify the tables we will try and explore. We can also parse out `DIRECT OBJECT(S)`, in an effort to see what columns we can select. With a collection of both, we can construct a list of possible `FROM` candidates, and a list of possible `SELECT` candidates.

#### Inputs
As an input, the parser will accept a full english statement, with the category defined by the classifier.

#### Outputs
As output, the parser will return two lists, one of possible `FROM` candidates (table names), and one of possible `SELECT` candidates (fields on tables)

### Lookup/Validation

The final stage of the pipeline is the validator. The validator must try to match the candidate tables and columns to the proper table and column names in the DB. Using word similarity and synonym matching, the validator must have a high condfidence level to match the table names and field names. Because the inputs are for multiple possible table names and column names, the validator will attempt to see what combination matches best. To do so, it will have to learn common synonyms and abbrevations for table/column names. For example, the word `ids` should match the column name `ID`, and the word `sect` would likely match the table name `Sections`.

#### Inputs
Two lists, one of possible `FROM` candidates (table names), and one of possible `SELECT` candidates (fields on tables).

#### Outputs
A list of `<SELECT,FROM>` tuples, and their confidence levels.
