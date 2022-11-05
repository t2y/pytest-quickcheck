
ChangeLog
=========

0.9.0 (2022-11-06)
------------------

* support pytest > 6.0
* drop supporting python 3.6

0.8.6 (2020-11-15)
------------------

* fix ignored ncalls parameter when a function annotation is used
* change to be able to use the same argument in randomize marker and function annotation

0.8.5 (2020-09-19)
------------------

* fix a critical issue pytest cannot detect randomize marker
* drop supporting pytest < 4.0.0
* drop supporting python 3.5

0.8.4 (2020-03-06)
------------------

* fix an issue related to pytest-4.x/5.x
* drop supporting python 3.3 and 3.4

0.8.3 (2017-05-27)
------------------

* fix an issue related to pytest-3.1.0
* drop supporting python 2.6 and 3.2

0.8.2 (2015-03-02)
------------------

* transfer the code repository to pytest-dev

0.8.1 (2014-12-25)
------------------

* support min_length for str data type
* removed distribute dependency
* add pytest-flakes testing

0.8 (2013-12-08)
----------------

* fix use the parameter length for string generator even if the set of
  available characters is less than it (#2)

* support new feature: Generating Collections from sonoflilit

0.7 (2012-10-20)
----------------

* the types in the arguments are specified by the types themselves (#1)

0.6 (2012-03-29)
----------------
* add generating data feature from function annotation

0.5 (2012-03-18)
----------------
* first release
