Mailr
=====
**Open Source webmail client with Gmail like conversations.**

I love emails.

I have been using Gmail during last seven years. I had tried to move away many times, but 
always returned back. I have tried probably all possible alternatives and no one can't fit 
for me as the best conversations making by Google.

Now many who trying to invent new generation of emails. There are services made by 
corporations like gmail.com, mail.yahoo.com, outlook,com, mailboxapp.com, mail.yandex.com 
and smaller companies with fastmail.fm, hashmail.com, inboxapp.com and some small open 
source teams like mailpile.is, Geary (desktop email client with Gmail like conversations). 
And Mailr wants to be a good alternative for them.

The most similar to Mailr is Mailpile. They both Open Sourced, both web based and both 
using Python.

I think Mailpile has main principle **security**.

Mailr has main principle **simplicity**
 - simple, but flexible and useful interface
 - codebase with simplicity in mind (less dependencies, less code - means simpler for 
   supporting in the future)
 - simple way for installation and deployment

I started Mailr couple months ago and it has pretty well public demo with narrow feature 
set. I can read all my emails through Mailr interface and I really like it (sure, because 
I've been making it). I want to build the first powerful version in four months for 
replacing gmail in my daily using.

Why I think I can do this?
--------------------------
1. **Right instruments**

   **Python** is really right language. I love Python. It has powerful standard library 
   and lots of useful third party libraries (sqlalchemy, werkzeug, jinja2, lxml). Mailpile 
   and InboxApp both have been making with Python.

   **PosgresSQL** is right storage. It can be use with transactions, replication and 
   backups for saving my emails carefully. It has useful feature set for searching and 
   indexing, so I don't need invent wheel for these things.

2. **Right way** (for getting the first usable version as soon as possible)

   **Gmail** as first backend through IMAP with bidirectional synchronization. Gmail has 
   good storage for emails, filters for incoming messages, powerful spam filter, email 
   clients for smartphones and tablets. So I can concentrate on useful interface and other 
   thing can wait for later. And I always can return to Gmail again and use it as usual or 
   just use it in parallel mode.

   So with Gmail I can do most important features first and some can wait for later. I 
   can read emails through Mailr, next feature is writing emails. And I need to 
   implement, to optimize, and to polish big set of features: conversations, email 
   parsing, synchronizing, search, detecting and folding quotes, hotkeys, settings, 
   themes, label handling, filtering of incoming messages, SSL support and etc.

   Probably **Mailgun** as second backend. Setup and supporting my own email server with 
   good spam filter and good reliability is horrible thing. So services like Mailgun can 
   help me with this stuff.

   If I'd implement Mailgun and make good replication for my PosgreSQL I can remove 
   synchronization with Gmail (not from supporting, just from usage), that simplify and 
   speed Mailr installation, because synchronization part is complicated and sometimes 
   slow.

   And then other IMAP servers (so Mailr can be used with full own setup).

::

  I even make up quatrain
    With right instruments
    During right way
    You can get big resultants
    Not far away

So goal is four months for $10.000
----------------------------------
I will work full-time on Mailr with two iterations (each in two months).

First iteration, named "I have moved away from Gmail but with Gmail behind my back":
 - composing and sending email
 - improving conversation with all important actions
 - improving and optimizing synchronization through IMAP
 - improving email parsing
 - improving detecting and folding quotes and signatures
 - preparing docker image and ansible playbook
 - preparing instructions for installation
 - publishing

After first iteration I suppose I will switch to Mailr in daily basis.

Second iteration, named "Really? I have moved away from Gmail!"
 - improving all optimization all existing features
 - improving themes and implementing new ones
 - filtering incoming messages
 - multi-accounts support
 - Mailgun support
 - publishing

After second iteration I suppose Mailr will be perfect alternative for webmail.

Why fundraiser?
---------------
I have experience about seven years in web development. I usually work as Python Developer 
on full-time position (often remote). I have been sometimes as fully backend developer
Last year I have spend my time mostly on my own projects (includes my newborn first son) 
and Mailr is last one which I have been working maybe last four months, including 
researching and the first prototype which I left and start developing Mailr from scratch 
(it takes probably two month and a little). Now I have spent mostly all the money which I 
have (I didn't earn anything during last year) and I need to get job for supporting my 
family. But I want to develop Mailr. Now I dive deep in context, I have a lot of 
enthusiasm and this is right time, because if I get a job I will dive deep in new role and 
new project and Mailr can late for about year. So I really want to work on email stuff and 
I need some money.


Just examples of campaigns
--------------------------
- https://www.indiegogo.com/projects/mailpile-taking-e-mail-back

  Funding duration: August 03, 2013 - September 10, 2013 (11:59pm PT).

  | https://news.ycombinator.com/item?id=6152046
  | Mailpile: Lets take email back
  | 507 points by threedaymonk 8 months ago 234 comments
  | 2013-08-03T13:48:10.000Z

  | https://news.ycombinator.com/item?id=6243936
  | Mailpile taking e-mail back
  | 316 points by tim_hutton 8 months ago 151 comments
  | 2013-08-20T14:36:59.000Z

  | https://news.ycombinator.com/item?id=6333203
  | PayPal Freezes Mailpile Campaign Funds 507 points
  | 507 points by capgre 7 months ago 351 comments
  | 2013-09-05T10:20:21.000Z

- https://www.bountysource.com/teams/neovim/fundraiser

  | https://news.ycombinator.com/item?id=7449663
  | Bram Moolenaar responds to Neovim
  | 208 points by dviola 2 months ago 149 comments
  | 2014-02-23T21:26:12.000Z

  | https://news.ycombinator.com/item?id=7278214
  | Neovim  838 points by tarruda 2 months ago 367 comments
  | 2014-02-21T17:48:07.000Z

- https://www.bountysource.com/teams/rvm/fundraiser