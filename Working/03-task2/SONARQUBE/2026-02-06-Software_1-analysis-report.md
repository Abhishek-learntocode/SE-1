# Code analysis
## Software_1 
#### Branch main
#### Version 6.1.5 

**By: Administrator**

*Date: 2026-02-06*

*Analyzed the: 2026-02-06*

## Introduction
This document contains results of the code analysis of Software_1

Roller is an open source blog server built with open source Java
        libraries including Struts2, Velocity, ROME and Guice.

## Configuration

- Quality Profiles
    - Names: Sonar way [CSS]; Sonar way [Java]; Sonar way [JavaScript]; Sonar way [JSP]; Sonar way [XML]; 
    - Files: f53700e5-5193-4395-9e0a-0554a69645f8.json; bae3dbf1-8691-4c60-b49c-c3978473feab.json; 6c765719-e4b9-4f01-8302-e0ed9882f829.json; f1b9a61a-cb03-4d0a-83f4-7127655db18e.json; e26ea2fb-48db-4bc9-bba1-23f1a0cd3caa.json; 


 - Quality Gate
    - Name: Sonar way
    - File: Sonar way.xml

## Synthesis

### Analysis Status

Reliability | Security | Security Review | Maintainability |
:---:|:---:|:---:|:---:
E | E | E | A |

### Quality gate status

| Quality Gate Status | OK |
|-|-|



### Metrics

Coverage | Duplications | Comment density | Median number of lines of code per file | Adherence to coding standard |
:---:|:---:|:---:|:---:|:---:
0.0 % | 3.8 % | 13.2 % | 69.0 | 94.3 %

### Tests

Total | Success Rate | Skipped | Errors | Failures |
:---:|:---:|:---:|:---:|:---:
0 | 0 % | 0 | 0 | 0

### Detailed technical debt

Reliability|Security|Maintainability|Total
---|---|---|---
2d 1h 48min|5d 1h 15min|40d 5h 34min|48d 0h 37min


### Metrics Range

\ | Cyclomatic Complexity | Cognitive Complexity | Lines of code per file | Coverage | Comment density (%) | Duplication (%)
:---|:---:|:---:|:---:|:---:|:---:|:---:
Min | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0
Max | 9276.0 | 7611.0 | 66541.0 | 0.0 | 91.3 | 92.9

### Volume

Language|Number
---|---
CSS|9757
Java|47634
JavaScript|532
JSP|6184
XML|2611
Total|66718


## Issues

### Issues count by severity and types

Type / Severity|INFO|MINOR|MAJOR|CRITICAL|BLOCKER
---|---|---|---|---|---
BUG|0|21|66|12|55
VULNERABILITY|0|111|0|6|5
CODE_SMELL|396|580|859|477|14


### Issues List

Name|Description|Type|Severity|Number
---|---|---|---|---
Resources should be closed||BUG|BLOCKER|54
"wait(...)" should be used instead of "Thread.sleep(...)" when a lock is held||BUG|BLOCKER|1
HTML elements should have unique "id" attribute values||BUG|CRITICAL|4
Assertions comparing incompatible types should not be made||BUG|CRITICAL|8
"<title>" should be present in all pages||BUG|MAJOR|1
"<html>" element should have a language attribute||BUG|MAJOR|11
Tables should have headers||BUG|MAJOR|7
Font declarations should contain at least one generic font family||BUG|MAJOR|3
Properties should not be duplicated||BUG|MAJOR|3
Media features should be valid||BUG|MAJOR|1
Classes should not be compared by name||BUG|MAJOR|1
"InterruptedException" and "ThreadDeath" should not be ignored||BUG|MAJOR|16
Null pointers should not be dereferenced||BUG|MAJOR|14
Blocks should be synchronized on "private final" fields||BUG|MAJOR|2
Conditionally executed code should be reachable||BUG|MAJOR|6
Alternatives in regular expressions should be grouped when used with anchors||BUG|MAJOR|1
"<frames>" should have a "title" attribute||BUG|MINOR|2
Mouse events should have corresponding keyboard events||BUG|MINOR|11
Math operands should be cast before assignment||BUG|MINOR|2
Non-primitive fields should not be "volatile"||BUG|MINOR|1
Return values should not be ignored when they contain the operation status code||BUG|MINOR|5
Methods and field names should not be the same or differ only by capitalization||CODE_SMELL|BLOCKER|4
TestCases should contain tests||CODE_SMELL|BLOCKER|3
Child class fields should not shadow parent class fields||CODE_SMELL|BLOCKER|3
Methods returns should not be invariant||CODE_SMELL|BLOCKER|3
Variables should be declared explicitly||CODE_SMELL|BLOCKER|1
Constant names should comply with a naming convention||CODE_SMELL|CRITICAL|9
Methods should not be empty||CODE_SMELL|CRITICAL|77
String literals should not be duplicated||CODE_SMELL|CRITICAL|84
"switch" statements should have "default" clauses||CODE_SMELL|CRITICAL|1
Generic wildcard types should not be used in return types||CODE_SMELL|CRITICAL|2
Fields in a "Serializable" class should either be transient or serializable||CODE_SMELL|CRITICAL|60
Try-with-resources should be used||CODE_SMELL|CRITICAL|5
"indexOf" checks should not be for positive numbers||CODE_SMELL|CRITICAL|2
Instance methods should not write to "static" fields||CODE_SMELL|CRITICAL|7
"static" base class members should not be accessed via derived types||CODE_SMELL|CRITICAL|3
Cognitive Complexity of methods should not be too high||CODE_SMELL|CRITICAL|99
"String#replace" should be preferred to "String#replaceAll"||CODE_SMELL|CRITICAL|1
Variables should be declared with "let" or "const"||CODE_SMELL|CRITICAL|125
Cognitive Complexity of functions should not be too high||CODE_SMELL|CRITICAL|2
Track uses of "TODO" tags||CODE_SMELL|INFO|2
Deprecated code should be removed||CODE_SMELL|INFO|6
Track uses of "TODO" tags||CODE_SMELL|INFO|133
JUnit5 test classes and methods should have default package visibility||CODE_SMELL|INFO|233
Methods should not perform too many tasks (aka Brain method)||CODE_SMELL|INFO|12
The Singleton design pattern should be used with care||CODE_SMELL|INFO|9
Track uses of "TODO" tags||CODE_SMELL|INFO|1
Attributes deprecated in HTML5 should not be used||CODE_SMELL|MAJOR|119
"aria-label" or "aria-labelledby" attributes should be used to differentiate similar elements||CODE_SMELL|MAJOR|4
Prefer tag over ARIA role||CODE_SMELL|MAJOR|19
"tabIndex" values should be 0 or -1||CODE_SMELL|MAJOR|18
Non-interactive DOM elements should not have interactive ARIA roles||CODE_SMELL|MAJOR|2
Anchor tags should not be used as buttons||CODE_SMELL|MAJOR|19
Non-interactive elements shouldn't have event handlers||CODE_SMELL|MAJOR|3
Non-interactive DOM elements should not have an interactive handler||CODE_SMELL|MAJOR|3
Heading elements should have accessible content||CODE_SMELL|MAJOR|2
Label elements should have a text label and an associated control||CODE_SMELL|MAJOR|31
Sections of code should not be commented out||CODE_SMELL|MAJOR|2
Duplicated font names should be removed||CODE_SMELL|MAJOR|1
Selectors should not be duplicated||CODE_SMELL|MAJOR|25
Text and background colors should have sufficient contrast||CODE_SMELL|MAJOR|43
Standard outputs should not be used directly to log anything||CODE_SMELL|MAJOR|46
Mergeable "if" statements should be combined||CODE_SMELL|MAJOR|7
Unused "private" fields should be removed||CODE_SMELL|MAJOR|3
Methods should not have too many parameters||CODE_SMELL|MAJOR|12
Nested blocks of code should not be left empty||CODE_SMELL|MAJOR|44
Inheritance tree of classes should not be too deep||CODE_SMELL|MAJOR|1
Local variables should not shadow class fields||CODE_SMELL|MAJOR|4
Utility classes should not have public constructors||CODE_SMELL|MAJOR|14
Generic exceptions should never be thrown||CODE_SMELL|MAJOR|45
Deprecated elements should have both the annotation and the Javadoc tag||CODE_SMELL|MAJOR|2
Try-catch blocks should not be nested||CODE_SMELL|MAJOR|19
Unused "private" methods should be removed||CODE_SMELL|MAJOR|8
Synchronized classes "Vector", "Hashtable", "Stack" and "StringBuffer" should not be used||CODE_SMELL|MAJOR|22
"@Override" should be used on overriding and implementing methods||CODE_SMELL|MAJOR|1
Empty arrays and collections should be returned instead of null||CODE_SMELL|MAJOR|4
Unused method parameters should be removed||CODE_SMELL|MAJOR|21
Throwable and Error should not be caught||CODE_SMELL|MAJOR|2
Sections of code should not be commented out||CODE_SMELL|MAJOR|92
"for" loop stop conditions should be invariant||CODE_SMELL|MAJOR|5
Anonymous inner classes containing only one method should become lambdas||CODE_SMELL|MAJOR|1
JUnit4 @Ignored and JUnit5 @Disabled annotations should be used to disable tests and should provide a rationale||CODE_SMELL|MAJOR|1
A field should not duplicate the name of its containing class||CODE_SMELL|MAJOR|2
Unused assignments should be removed||CODE_SMELL|MAJOR|67
Two branches in a conditional structure should not have exactly the same implementation||CODE_SMELL|MAJOR|7
Classes with only "static" methods should not be instantiated||CODE_SMELL|MAJOR|1
Boolean expressions should not be gratuitous||CODE_SMELL|MAJOR|4
"Thread.sleep" should not be used in tests||CODE_SMELL|MAJOR|9
Reflection should not be used to increase accessibility of classes, methods, or fields||CODE_SMELL|MAJOR|3
Ternary operators should not be nested||CODE_SMELL|MAJOR|2
Assertion arguments should be passed in the correct order||CODE_SMELL|MAJOR|1
"Map.get" and value test should be replaced with single method call||CODE_SMELL|MAJOR|2
"java.nio.Files#delete" should be preferred||CODE_SMELL|MAJOR|5
Methods should not have identical implementations||CODE_SMELL|MAJOR|5
Assignments should not be redundant||CODE_SMELL|MAJOR|2
"@Deprecated" code marked for removal should never be used||CODE_SMELL|MAJOR|2
JUnit assertTrue/assertFalse should be simplified to the corresponding dedicated assertion||CODE_SMELL|MAJOR|4
Regular expressions should not be too complicated||CODE_SMELL|MAJOR|3
Test methods should not contain too many assertions||CODE_SMELL|MAJOR|2
Similar tests should be grouped in a single Parameterized test||CODE_SMELL|MAJOR|1
Constructors of an "abstract" class should not be declared "public"||CODE_SMELL|MAJOR|13
Single-character alternations in regular expressions should be replaced with character classes||CODE_SMELL|MAJOR|15
Restricted Identifiers should not be used as Identifiers||CODE_SMELL|MAJOR|13
Deprecated annotations should include explanations||CODE_SMELL|MAJOR|6
Non-capturing groups without quantifier should not be used||CODE_SMELL|MAJOR|1
Character classes in regular expressions should not contain only one character||CODE_SMELL|MAJOR|1
Use batch Processing in JDBC||CODE_SMELL|MAJOR|10
Increment and decrement operators (++/--) should not be used with floating point variables||CODE_SMELL|MAJOR|5
Sections of code should not be commented out||CODE_SMELL|MAJOR|1
"arguments.caller" and "arguments.callee" should not be used||CODE_SMELL|MAJOR|4
Regular expressions should not be too complicated||CODE_SMELL|MAJOR|1
Unnecessary character escapes should be removed||CODE_SMELL|MAJOR|4
Ends of strings should be checked with "startsWith()" and "endsWith()"||CODE_SMELL|MAJOR|2
DOM nodes should be removed using "remove()" instead of "removeChild()"||CODE_SMELL|MAJOR|3
Modern DOM manipulation methods should be used instead of legacy alternatives||CODE_SMELL|MAJOR|9
Sections of code should not be commented out||CODE_SMELL|MAJOR|4
Image, area and button with image elements should have an "alt" attribute||CODE_SMELL|MINOR|8
Anchors should contain accessible content||CODE_SMELL|MINOR|2
URIs should not be hardcoded||CODE_SMELL|MINOR|8
Class variable fields should not have public accessibility||CODE_SMELL|MINOR|12
Empty statements should be removed||CODE_SMELL|MINOR|4
Modifiers should be declared in the correct order||CODE_SMELL|MINOR|10
Boolean literals should not be redundant||CODE_SMELL|MINOR|1
Return of boolean expressions should not be wrapped into an "if-then-else" statement||CODE_SMELL|MINOR|6
Unnecessary imports should be removed||CODE_SMELL|MINOR|42
Exceptions in "throws" clauses should not be superfluous||CODE_SMELL|MINOR|42
Field names should comply with a naming convention||CODE_SMELL|MINOR|3
Exception classes should have final fields||CODE_SMELL|MINOR|2
Local variable and method parameter names should comply with a naming convention||CODE_SMELL|MINOR|24
Public constants and fields initialized at declaration should be "static final" rather than merely "final"||CODE_SMELL|MINOR|2
Array designators "[]" should be on the type, not the variable||CODE_SMELL|MINOR|17
Nested code blocks should not be used||CODE_SMELL|MINOR|1
"equals(Object obj)" should be overridden along with the "compareTo(T obj)" method||CODE_SMELL|MINOR|2
"switch" statements should have at least 3 "case" clauses||CODE_SMELL|MINOR|2
Declarations should use Java collection interfaces such as "List" rather than specific implementation classes such as "LinkedList"||CODE_SMELL|MINOR|3
Loops should not contain more than a single "break" or "continue" statement||CODE_SMELL|MINOR|10
"public static" fields should be constant||CODE_SMELL|MINOR|5
Private fields only used as local variables in methods should become local variables||CODE_SMELL|MINOR|1
Unused local variables should be removed||CODE_SMELL|MINOR|15
Local variables should not be declared and then immediately returned or thrown||CODE_SMELL|MINOR|1
Strings should not be concatenated using '+' in a loop||CODE_SMELL|MINOR|21
Multiple variables should not be declared on the same line||CODE_SMELL|MINOR|2
"@Deprecated" code should not be used||CODE_SMELL|MINOR|190
Redundant casts should not be used||CODE_SMELL|MINOR|2
Fields in non-serializable classes should not be "transient"||CODE_SMELL|MINOR|1
Parsing should be used to convert "Strings" to primitives||CODE_SMELL|MINOR|1
Catches should be combined||CODE_SMELL|MINOR|3
Subclasses that add fields to classes that override "equals" should also override "equals"||CODE_SMELL|MINOR|4
The diamond operator ("<>") should be used||CODE_SMELL|MINOR|1
Mutable fields should not be "public static"||CODE_SMELL|MINOR|1
Static non-final field names should comply with a naming convention||CODE_SMELL|MINOR|7
Arguments to "append" should not be concatenated||CODE_SMELL|MINOR|1
Loggers should be named for their enclosing classes||CODE_SMELL|MINOR|2
Jump statements should not be redundant||CODE_SMELL|MINOR|3
Arrays should not be created for varargs parameters||CODE_SMELL|MINOR|7
Collection contents should be used||CODE_SMELL|MINOR|1
An iteration on a Collection should be performed on the type handled by the Collection||CODE_SMELL|MINOR|5
Avoid using boxed "Boolean" types directly in boolean expressions||CODE_SMELL|MINOR|15
Character classes should be preferred over reluctant quantifiers in regular expressions||CODE_SMELL|MINOR|1
"String.isEmpty()" should be used to test for emptiness||CODE_SMELL|MINOR|33
Deprecated APIs should not be used||CODE_SMELL|MINOR|10
Exceptions should not be ignored||CODE_SMELL|MINOR|5
"for of" should be used with Iterables||CODE_SMELL|MINOR|16
Regular expression quantifiers and character classes should be used concisely||CODE_SMELL|MINOR|6
"RegExp.exec()" should be preferred over "String.match()"||CODE_SMELL|MINOR|2
Error parameters in catch clauses should follow a consistent naming convention||CODE_SMELL|MINOR|1
Negated conditions should be avoided when an else clause is present||CODE_SMELL|MINOR|1
Use "globalThis" instead of "window", "self", or "global"||CODE_SMELL|MINOR|3
Existence checks should use ".includes()" instead of ".indexOf()" or ".lastIndexOf()"||CODE_SMELL|MINOR|8
Strings should use "replaceAll()" instead of "replace()" with global regex||CODE_SMELL|MINOR|4
XML parsers should not be vulnerable to XXE attacks||VULNERABILITY|BLOCKER|5
Passwords should not be stored in plaintext or with a fast hashing algorithm||VULNERABILITY|CRITICAL|5
Struts filters should not miss their corresponding filter-map||VULNERABILITY|CRITICAL|1
Exceptions should not be thrown from servlet methods||VULNERABILITY|MINOR|111


## Security Hotspots

### Security hotspots count by category and priority

Category / Priority|LOW|MEDIUM|HIGH
---|---|---|---
LDAP Injection|0|0|0
Object Injection|0|0|0
Server-Side Request Forgery (SSRF)|0|0|0
XML External Entity (XXE)|0|0|0
Insecure Configuration|6|0|0
XPath Injection|0|0|0
Authentication|0|0|1
Weak Cryptography|0|3|0
Denial of Service (DoS)|0|8|0
Log Injection|0|0|0
Cross-Site Request Forgery (CSRF)|0|0|0
Open Redirect|0|0|0
Permission|0|0|0
SQL Injection|0|0|0
Encryption of Sensitive Data|0|0|0
Traceability|0|0|0
Buffer Overflow|0|0|0
File Manipulation|0|0|0
Code Injection (RCE)|0|0|0
Cross-Site Scripting (XSS)|0|0|0
Command Injection|0|0|0
Path Traversal Injection|0|0|0
HTTP Response Splitting|0|0|0
Others|13|0|0


### Security hotspots

Category|Name|Priority|Severity|Count
---|---|---|---|---
Insecure Configuration|Delivering code in production with debug features activated is security-sensitive|LOW|MINOR|6
Others|Allowing user enumeration is security-sensitive|LOW|MAJOR|1
Others|Using weak hashing algorithms is security-sensitive|LOW|CRITICAL|10
Others|Using publicly writable directories is security-sensitive|LOW|CRITICAL|2
Denial of Service (DoS)|Using slow regular expressions is security-sensitive|MEDIUM|CRITICAL|8
Authentication|Hard-coded passwords are security-sensitive|HIGH|BLOCKER|1
Weak Cryptography|Using pseudorandom number generators (PRNGs) is security-sensitive|MEDIUM|CRITICAL|3

