# Typical Blog Site
## 🔧 Technology used:
![](https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white)
![](https://img.shields.io/badge/django%20-%23092E20.svg?&style=for-the-badge&logo=django&logoColor=white)
![](https://img.shields.io/badge/sqlite-%2307405e.svg?&style=for-the-badge&logo=sqlite&logoColor=white)
![](https://img.shields.io/badge/smtp%20-%231572B6.svg?&style=for-the-badge)  
![](https://img.shields.io/badge/html%20-%23E34F26.svg?&style=for-the-badge&logo=html5&logoColor=white)
![](https://img.shields.io/badge/css%20-%231572B6.svg?&style=for-the-badge&logo=css3&logoColor=white)
![](https://img.shields.io/badge/javascript%20-%23323330.svg?&style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![](https://img.shields.io/badge/jquery%20-%231572B6.svg?&style=for-the-badge&logo=jquery&logoColor=white)

## [Live Demo](https://blogsite.pythonanywhere.com/)
I built this web app for better understanding of foreign keys and one to one, many to many relationships.
This web app handles 3 models-
- User CRUD
- Blog CRUD
- Comments CRD (Updation of comments is not allowed)  

> CRUD -- `Creation Retrieval Updation Deletion`
## Features:
- Users can register themselves
- Users can change their passwords
- Users can reset their password if forgot (process is handles using SMTP )
- Authenticated users can create their blogs
- Users can delete or edit their blogs ( Only the blogs that created by them)
- Users can make comments on all the blogs
- Users can delete their comments ( Only the comments that created by them)
- Users can like or dislike the blogs
- Trending blogs will be ranked automatically on the basis of number of likes and dislikes.
- User can search for blogs
- Users can contact the owner. (Process is handled using SMTP)
## New Features I would like to add: 
I would like to add some new feature to this site that is,
- User could reply to particular comment
- User could search other users and message them