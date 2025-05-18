
const exampleNotification = {
  "account": {}, // reciepient account obj

  "content": {

    "from": {
      "username": "example00",
      "fullName": "Example",
      "avatar": "https://example.com/avatar.webp"
    },

    "title": "@mohamed liked your message!",
    "objectType": "writeup", // writeup, comment or text (if text then the object will be a str otherwise its serialized obj)
    "object": {}, // serialized write up or whatever object
    "icon": null, // heart, user, write up
    "link": null, // an internal link when the notification is clicked the router will push to

  },
  "created_at": "...",
  "updated_at": "...",
  "isRead": false
}



const icons = [
  "user", // follow
  "heart", // like
  "minus-user", // unfollow
  "chat", // reply or comment
]


const object_types = [
  "writeup",
  "comment",
]
