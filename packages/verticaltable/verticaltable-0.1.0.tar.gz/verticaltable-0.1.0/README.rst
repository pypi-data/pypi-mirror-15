verticaltable
~~~~~~~~~~~~~

This is an structured text parser.


format
------

example 1:

source:
::

  [Q] This is a question.
  [A] This is an answer.
  [Q] This is a question2.
  # This is comment
  [A] This is an answer2.

parsed:

::

  [
    {
      'Q': 'This is a question.',
      'A': 'This is an answer.',
    },
    {
      'Q': 'This is a question2.',
      'A': 'This is an answer2.',
    },
  ]

* If the same key appeared, Next record.
* Actuary, output is OrderedDict list. Not Dict list.

source:
::

  [Key1]
  Value1
  [Key2]
  Value2
  ----
  [Key3]
  Value3
  next line
  next line
  [Key4]

  Value4    4!

  [Key5]
  Value5

parsed:

::

  [
    {
      'Key1': 'Value1',
      'Key2': 'Value2',
    },
    {
      'Key3': 'Value3\nnext line\nnext line',
      'Key4': 'Value4    4!',
      'Key5': 'Value5',
    }

* Whitespace trimmed.
* "----" (Hyphens >= 4) is list separator.


usage
-----

::

  import verticaltable

  fp = open('sample.txt')

  parsed_list = verticaltable.loads(fp.read())

  parsed_list2 = verticaltable.load(open('sample2.txt'))
