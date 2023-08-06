ChangeLog
=========

0.0.7 (2016/05/02)
------------------

- fix the function fromurl when path is given.

0.0.6 (2016/05/02)
------------------

- fix the function fromurl in adding the parameter scheme in the middleware caller constructor.

0.0.5 (2016/05/02)
------------------

- fix the function fromurl when using the function b3j0f.utils.iterable.first.

0.0.4 (2016/05/02)
------------------

- fix the function getmcallers at initialization of the first iteration of found middlewares.

0.0.3 (2016/05/02)
------------------

- fix build error.

0.0.2 (2016/05/02)
------------------

- remove the function 'core.get'.
- add the function 'core.getmcallers' in order to get all middleware callers bound to input protocols.
- ensure resolution of successive protocols inside an url scheme with the separator '+'.
- ensure resolution of multiple protocols inside an url scheme with the separator '-'.
- add the parameter 'cache' in the function 'url.fromurl'.

0.0.1 (2016/02/09)
------------------

- library creation.
