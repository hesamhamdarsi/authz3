
"click" will create a command prompt for us

checking:
```
(venv) hesam@HH-Host:~/Downloads/programming/python/MS-test-3/authz$ flask --help
Usage: flask [OPTIONS] COMMAND [ARGS]...

  A general utility script for Flask applications.

  Provides commands from Flask, extensions, and the application. Loads the
  application defined in the FLASK_APP environment variable, or from a
  wsgi.py file. Setting the FLASK_ENV environment variable to 'development'
  will enable debug mode.

    $ export FLASK_APP=hello.py
    $ export FLASK_ENV=development
    $ flask run

Options:
  --version  Show the flask version
  --help     Show this message and exit.

Commands:
  app     Application related commands.
  db      Perform database migrations.
  routes  Show the routes for the app.
  run     Run a development server.
  shell   Run a shell in the app context.
------------------------------------------------
(venv) hesam@HH-Host:~/Downloads/programming/python/MS-test-3/authz$ flask app --help
Usage: flask app [OPTIONS] COMMAND [ARGS]...

  Application related commands.

Options:
  --help  Show this message and exit.

Commands:
  test  Testing Application backing connections

```

what is result = db.engine.execute("SELECT 1;").first()?
flask provides a shell to execute some of the commands for libve test (not all commands)
from instance:

```
(venv) hesam@HH-Host:~/Downloads/programming/python/MS-test-3/authz$ flask shell
Python 3.8.5 (default, Jul 28 2020, 12:59:40) 
[GCC 9.3.0] on linux
App: authz [development]
Instance: /home/hesam/Downloads/programming/python/MS-test-3/authz/instance
>>> from authz import db
```

if you look at what is inside the db:
```
>>> dir(db)
['ARRAY', 'AliasOption', 'AttributeExtension', 'BIGINT', 'BINARY', 'BLANK_SCHEMA', 'BLOB', 'BOOLEAN', 'BigInteger', 'Binary', 'Boolean', 'Bundle', 'CHAR', 'CLOB', 'CheckConstraint', 'Column', 'ColumnDefault', 'ColumnProperty', 'ComparableProperty', 'CompositeProperty', 'Computed', 'Constraint', 'DATE', 'DATETIME', 'DDL', 'DECIMAL', 'Date', 'DateTime', 'DefaultClause', 'EXT_CONTINUE', 'EXT_SKIP', 'EXT_STOP', 'Enum', 'FLOAT', 'FetchedValue', 'Float', 'ForeignKey', 'ForeignKeyConstraint', 'INT', 'INTEGER', 'IdentityOptions', 'Index', 'Integer', 'Interval', 'JSON', 'LargeBinary', 'Load', 'Mapper', 'MapperExtension', 'MetaData', 'Model', 'NCHAR', 'NUMERIC', 'NVARCHAR', 'Numeric', 'PassiveDefault', 'PickleType', 'PrimaryKeyConstraint', 'PropComparator', 'Query', 'REAL', 'RelationshipProperty', 'SMALLINT', 'Sequence', 'Session', 'SessionExtension', 'SmallInteger', 'String', 'SynonymProperty', 'TEXT', 'TIME', 'TIMESTAMP', 'Table', 'Text', 'ThreadLocalMetaData', 'Time', 'TypeDecorator', 'Unicode', 'UnicodeText', 'UniqueConstraint', 'VARBINARY', 'VARCHAR', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_engine_lock', '_engine_options', '_execute_for_all_tables', 'alias', 'aliased', 'all_', 'and_', 'any_', 'app', 'apply_driver_hacks', 'apply_pool_defaults', 'asc', 'backref', 'between', 'bindparam', 'case', 'cast', 'class_mapper', 'clear_mappers', 'close_all_sessions', 'collate', 'column', 'column_property', 'comparable_property', 'compile_mappers', 'composite', 'configure_mappers', 'contains_alias', 'contains_eager', 'create_all', 'create_engine', 'create_scoped_session', 'create_session', 'defaultload', 'defer', 'deferred', 'delete', 'desc', 'distinct', 'drop_all', 'dynamic_loader', 'eagerload', 'eagerload_all', 'engine', 'engine_from_config', 'event', 'except_', 'except_all', 'exists', 'extract', 'false', 'foreign', 'func', 'funcfilter', 'get_app', 'get_binds', 'get_engine', 'get_tables_for_bind', 'immediateload', 'init_app', 'insert', 'inspect', 'intersect', 'intersect_all', 'join', 'joinedload', 'joinedload_all', 'lateral', 'lazyload', 'lazyload_all', 'literal', 'literal_column', 'load_only', 'make_connector', 'make_declarative_base', 'make_transient', 'make_transient_to_detached', 'mapper', 'metadata', 'modifier', 'noload', 'not_', 'null', 'nullsfirst', 'nullslast', 'object_mapper', 'object_session', 'or_', 'outerjoin', 'outparam', 'over', 'polymorphic_union', 'public_factory', 'query_expression', 'raiseload', 'reconstructor', 'reflect', 'relation', 'relationship', 'remote', 'scoped_session', 'select', 'selectin_polymorphic', 'selectinload', 'selectinload_all', 'session', 'sessionmaker', 'subquery', 'subqueryload', 'subqueryload_all', 'synonym', 'table', 'tablesample', 'text', 'true', 'tuple_', 'type_coerce', 'undefer', 'undefer_group', 'union', 'union_all', 'update', 'use_native_unicode', 'validates', 'was_deleted', 'with_expression', 'with_parent', 'with_polymorphic', 'within_group']
```

you see one of the functions are engine. in engine you have:
```
>>> dir(db.engine)
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_connection_cls', '_contextual_connect', '_echo', '_execute_clauseelement', '_execute_compiled', '_execute_default', '_execution_options', '_has_events', '_optional_conn_ctx_manager', '_run_visitor', '_should_log_debug', '_should_log_info', '_trans_ctx', '_wrap_pool_connect', 'begin', 'connect', 'contextual_connect', 'create', 'dialect', 'dispatch', 'dispose', 'driver', 'drop', 'echo', 'engine', 'execute', 'execution_options', 'get_execution_options', 'has_table', 'hide_parameters', 'logger', 'logging_name', 'name', 'pool', 'raw_connection', 'run_callable', 'scalar', 'schema_for_object', 'table_names', 'transaction', 'update_execution_options', 'url']
```

through engine you can execute a query on your database:
```
>>> db.engine.execute("SELECT * FROM model_user")
<sqlalchemy.engine.result.ResultProxy object at 0x7f1f95797e50>
>>> db.engine.execute("SELECT * FROM model_user").first()
('0329e7055c474a1ca8889c21d75d18a1', 'heddsamww', '123456')
```

you see that first result will be returned. but how you are able to check database is accessible without knowing a record?
simply use the folowing query:
```
>>> db.engine.execute("SELECT * FROM model_user;").first()
('0329e7055c474a1ca8889c21d75d18a1', 'heddsamww', '123456')
>>> db.engine.execute("SELECT 1;").first()
(1,)
```

#### notice: SELECT 1; will always return 1

---
Now we need to make a file called "start.py" to be run before ruuning the application to do appropriate actions and also calling this file 
authz > start.py