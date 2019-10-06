# Welcome to flask-scubadivedubai

## Intro

Welcome to flask-scubadivedubai. This app is developed using python and flask framework. It is created for scubadivedivedubai.com.
The bsics of the app it that it is an infomrative website site for Sandy Beach Dive Centre. This is a dive centre based in the UAE.
It offers daily diving trips and PADI scuba diving courses.

This app offers a platform fro users to log in and to post blog posts to the site. The current ittereation will only have one user.
This user will be the admin of the site who will update all posts and load new pages into the site. 

The site has a few static pages such as the landing page, about us page and contact page. All other pages are dynamic pages which are
rendered through the flask framework. The database is based on SQLLite and will be moved over to Prostgress SQL when needed.

### Current functionaility includes:
- User Register
- Log in / out
- Create PADI courses pages, update and delete
- Create Diive Sites, update and delete
- Upload Blog post, update and delete
- Contact form susbmission
- Dive Course request form susbmission
- Fun diving request susbmission

## Technical Overview

### Languages
- Python : Server side controller
- Javascript : Client side functionality and interactivity
- CSS : Originally written in SCSS and compiled to CSS for styling
- HTML : Basic webpage layout

### Frameworks
- Flask : Server side framework
- Bootsrap : Web page styling
- JQuery : Client side UX

### Flask modules
- 


# Architectual Pattern

This appp is developed with the **MVC** arcitechitual design pattern. The details of each componenet is borken down below.

## Model

### SQLLite database