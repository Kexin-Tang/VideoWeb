# VideoWeb

This project mainly focuses on **Web Development** via a very popular framework called **Django**.

In this project, I have mastered lots of fundamental concepts about web development and programming tricks.

This project includes:
- *HTML/CSS*
- *Javascript*, *jQuery* &amp; *DOM*
- *MVC* structure
- *AJAX*
- *Redis* &amp; *Celery* (Distributed Task Queue)
- *Cookies* &amp; *Session*
- *MySQL* &amp; *Python ORM*
- *Nginx*

## Introduction

This website is designed for collecting useful MOOC courses, such as *Intro to XXX*, *XXX premier plus*, etc.

* Administrator 
  * upload videoes from other websites such as Youtube and Bilibili;
  * manage users' videoes, comments and authorities
* User
  * register and/or login
  * upload and operate their own videoes and articles
  * comment

## Innovation

* Used *Celery* to prevent users from waiting while uploading videos;
* Adopted both *Cookies* and *Session* methods to achieve different versions "LOGIN", "LOGOUT" and "REGISTER";
* Designed beautiful and user-friendly UI via *Bootstrap*, which may be replaced by *React.js* in future;

## TODO

- [ ] Responsive Design
- [x] Comments
- [ ] Remember me
- [ ] Login via phone number and email