# Project title: Wastify

## TLDR; 
This project is contained with docker containers and cocker compose. I you want to run this project, download Docker from their website, run the application. Then with terminal navigate to the project directory and run "docker-compose up". You will also have to create a new fireabse account to use the realtime messaging that is used in this project.

## Functional Specification:
The idea for this project is to create a social website with an easy login like Facebook, geo-location with google maps, posts like on facebook and optionally notifications. The focus of this website is to create the oportunity for people to gather around marked places with lots of garbage, that nobody cares about and to help clean it up.

## Technological specification:
For this project the technologies to be used (as of today) are: Vue.js for front-end developement, Firebase login for the login to the application, flask for the user database and Firebase firestore with real-time database for messaging. 

This project contains a lot of features, I will highlight some of them. 

## Signup
You can only signup using an email and password. The signup screen looks like below.
![alt text](https://github.com/Wojak27/Wastify/blob/master/Screenshot%202019-10-12%20at%2015.01.07.png)

## Feed
After the signup or login, you're met with the Feed screen showing all of the posted events and posts. You can either post an event, a short information, just with text or an event with Title text, description, location and an image.
![alt text](https://github.com/Wojak27/Wastify/blob/master/Screenshot%202019-10-12%20at%2014.45.44.png)
![alt text](https://github.com/Wojak27/Wastify/blob/master/Screenshot%202019-10-12%20at%2014.47.49.png)

## Explore
There is an Explore feature, where you can explore on a map the events happening next to you. When clicking on an event it will display the detailed information below along with the optional comments.
![alt text](https://github.com/Wojak27/Wastify/blob/master/Screenshot%202019-10-12%20at%2014.48.23.png)

## Messaging
You can also message different people in this webapp. There was little focus put into that function though.
![alt text](https://github.com/Wojak27/Wastify/blob/master/Screenshot%202019-10-12%20at%2014.49.35.png)

## Profile
There is also a profile where you can write your motto!
![alt text](https://github.com/Wojak27/Wastify/blob/master/Screenshot%202019-10-12%20at%2014.48.58.png)

