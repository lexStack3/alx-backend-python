# Unittests and Integration Test

## Objective
Unit testing is the process of testing that a particular function returns expected results for different set of inputs. A unit test is supposed to test standard inputs and corner cases. A unit test should only test the logic defined inside the tested function. Most calls to additional functions should be mocked, especially if they make network or database calls.

The goal of a unit test is to answer the question: if everything defined outside this function works as expected, does this function work as expected?

Integration test aim to test a code path end-to-end. In general, only low level functions that make external calls such as HTTP requests, filr I/O, database I/O, etc. are mocked.

Integration test will test interactions between every part of your code.
```bash
$ python -m unittest path/to/test_file.py
```
## Resources
- [unittest - Unit testing framework]('https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertMultiLineEqual')
- [unittest.mock]('https://docs.python.org/3/library/unittest.mock.html#filter-dir')
- [How to mock a readonly property with mock?]('https://stackoverflow.com/questions/11836436/how-to-mock-a-readonly-property-with-mock')
- [parameterized]('https://pypi.org/project/parameterized/')
- [Memoization]('https://en.wikipedia.org/wiki/Memoization')

## Learning Objectives
At the end of this project, you are expected to be able to explain to anyone, **without the help of Google**:
- The difference between unit and integration test.
- Common testing patterns such as mocking, parametrizations and fixtures
