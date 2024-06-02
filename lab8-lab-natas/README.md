# Module 8 Lab Natas

## Introduction

- In this lab assignment, I will complete the [capture the flag assignment](https://overthewire.org/wargames/natas/)

- In this capture the flag assignment I will learn the basics of serverside web-security

- Team members:

### Levels

#### Level 0:

- Logged in with the given username and password.

- Using the inspector tool in the browser, I found the line om the div element where id="content":

- `The password for natas1 is g9D9cREhslqBKtcA2uocGHPfMZVzeFK6`

#### Level 0 -> 1:

- I submitted the password with my inspector already loaded in
- I found the line:

`The password for natas2 is h4ubbcXrWqsTo7GGnnUMLppXbOogfBZ7`

#### Level 1 -> 2:

- While inspecting the page, I noticed a src image in the folder files.
- I located a file at this url: `http://natas2.natas.labs.overthewire.org/files/users.txt`
- Password was displayed: `G6ctbMJ5Nb4cbFwhpMPSvxGHhQ7I6W8Q`

#### Level 2 -> 3:

- Looking at the robots.txt file of webpage, I was able to back to the page that has the users.txt file in there.
- Password: `natas4:tKOcJIbzM4lTs8hbCmzn5Zr4434fGZQm`

#### Level 3 -> 4:

- Using a Firefox extension, called [Referer Control](https://addons.mozilla.org/en-US/firefox/addon/referercontrol/), I was able to access the website and change my Referer to be `http://natas5.natas.labs.overthewire.org/`
- Password: `Z0NsrtIkJoKALBCLi5eqFfcRN82Au2oD`

#### Level 4 -> 5:

- To change my user status to logged in, I went to the application settings where the cookies storage information was located.
- In here the value of `loggedin` was set to 0 so I changed it 1 and refreshed the page.
- Password: `fOIvE0MDtPTgRhqmmvvAOt2EfXR6uQgR`

#### Level 5 -> 6:

- Looking at the sourecode, I found out that I can examine this link: `http://natas6.natas.labs.overthewire.org/includes/secret.inc`
- I found out the secret and was able to submit the query
- Password: `jmxSiH3SP6Sonf8dv66ng8v1cIEdjXWr`

#### Level 6 -> 7:

- In the source section, I found a hint that had the path: `/etc/natas_webpass/natas8`
- I entered it as the page parameter into the url: `http://natas7.natas.labs.overthewire.org/index.php?page=/etc/natas_webpass/natas8`
- Password: `a6bZCNYwdKqN5cGP11ZdtPg0iImQQhAB`

#### Level 7 -> 8:

1. View the source code and find the secret before conversion
2. Hex to Ascii Text convertor: `==QcCtmMml1ViV3b`
3. Reverse string: `b3ViV1lmMmtCcQ==`
4. Decode Bas64 string: `oubWYf2kBq`

- Password: `Sda6t0vkOPkM8YeOZkAGVhFoaplvlJFd`

#### Level 8 -> 9:

- Using terminal commands, such as `ls`, I was able to analyze different files in the app directory.
- Searching at this location `;ls ../../../../../etc/natas_webpass/natas10`, I found that I can now cat this response
- `;cat ../../../../../etc/natas_webpass/natas10`
- Password: `D44EcsFkLxPIkAAKLosx8z3hxX1Z4MCE`

#### Level 9 -> 10:

- I searched for: `a /etc/natas_webpass/natas11`
- I I found this line `/etc/natas_webpass/natas11:1KFqoJXi6hRaPluAmk8ESDW4fSysRoIg`
- Password: `1KFqoJXi6hRaPluAmk8ESDW4fSysRoIg`

#### Level 10 -> 11:

- CTF URL: https://overthewire.org/wargames/natas/natas11.html
- URL: http://natas11.natas.labs.overthewire.org/
- Username: natas11
- password: `1KFqoJXi6hRaPluAmk8ESDW4fSysRoIg`
