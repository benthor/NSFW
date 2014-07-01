# NSFW #

HTML parser, pretty printer and datastructure supporting deep modifications to the tree. Has never heard of web standards.

Inspired by Beautiful Soup, which doesn't support deep mutation of the parsed tree however.

## Features ##

 * powerful (sub)tree search 
   * matching on tags
   * matching on attributes
   * matching on other features via custom match functions
 * built-in depth-first iterator
 * support for (sub)tree replacement/mutation/clone
 * support for deep copying
 * support for multiple trees in single parse
 * hassle-free pretty-print via ''__str__()'' override
 * funky method names


## ToDo ##

 * make SFW
 * improve output
 * add some convenient accessors
 * write more tests
 * raise more/better Exceptions in case of illegal actions
 * add setup.py for global installation
 * add more meaningful comments

## Dependencies ##

 * Python 3

