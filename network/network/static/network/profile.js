var theUser = ""
var thePost = ""
var globalId = parseInt(0);

document.addEventListener('DOMContentLoaded', function() {    
    pageNum = document.querySelector('#thePageNumber').value;

    theUser = document.querySelector('#usersname').value
    load_info(theUser, pageNum);
    load_userpost(theUser, pageNum);
    
    document.addEventListener('#followButton', () => {
        follow_user(event);
    })


    document.addEventListener('click', event => {
        const element = event.target;

        if (element.className == 'btn btn-secondary') {            
            var theId = element.name;
            globalId = theId;
            getEditView(theId);
        }
    })

    document.addEventListener('click', event => {
        const element = event.target;

        if (element.className == 'btn btn-info') {            
            edit(globalId);
        }
    })

    document.addEventListener('click', event => {
        const element = event.target;

        if (element.className == 'btn btn-dark') {   
            var theId = element.name;
            globalId = theId;
         
            getPostFromID(theId);
            likePost(theId);
        }
    })

    document.addEventListener('click', event => {
        const element = event.target;

        if (element.className == 'btn btn-warning') {   
            var theId = element.name;
            globalId = theId;
         
            getPostFromID(theId);
            unlikePost(theId);
        }
    })

})

function load_info(user_name) {
    fetch('/getUserInfor/'+user_name)
    .then(response => response.json())
    .then(profileData => {
        profileData.forEach(function(item) {
            // Display Info to Page        
            document.querySelector('#profile-info').innerHTML += `<h1>${item.username}</h1> <p></p><h6>Followers: </h6> ${item.followers} <p></p> <h6>Following: </h6> ${item.following}`;
        });
    });
}

function load_userpost(user_name, pageNumber) {
    currentUser = document.querySelector('#logged-user').value;

    fetch('/getUserPost/'+user_name+'/'+pageNumber)
    .then(response => response.json())
    .then(postData => {
        postData.forEach(function(item) {
            // Display Info to Page        
            //document.querySelector('#post-order').innerHTML += `<div style="border-style: groove">${item.postText}<p></p> was posted by ${item.user} at ${item.timestamp}<p></p> &#128151; : ${item.postLikes}<br></br></div>`;
            const Posts = document.createElement('div');
            Posts.className = 'profile-posts';
            Posts.style = 'border-style: solid'
            Posts.innerHTML = `<div id="profile-posts-${item.id}" style="border-style: groove">${item.postText}<p></p> was posted by ${item.user} at ${item.timestamp}<p></p> &#128151; : ${item.postLikes} <br></br></div>`;
            document.querySelector('#post-order').append(Posts)
            
            if (currentUser == item.user) {
                const postButton = document.createElement('div');
                postButton.className = 'post';
                postButton.style = 'border-style: dashed';
                postButton.innerHTML =`<input id="edit-post-id" type="hidden" value="${item.id}"><input id="edit-post-button" name="${item.id}" class="btn btn-secondary" type="submit" value="Edit">`;
                document.querySelector('#post-order').append(postButton);
            }
            
            const LikePost = document.createElement('div');
            LikePost.className = 'like'
            LikePost.innerHTML = `<form id="like-form"><input name="${item.id}" type="submit" class="btn btn-dark" value="Like"></form>`;
            document.querySelector(`#profile-posts-${item.id}`).append(LikePost);    

            const UnLikePost = document.createElement('div');
            UnLikePost.className = 'unlike'
            UnLikePost.innerHTML = `<form id="like-form"><input name="${item.id}" type="submit" class="btn btn-warning" value="Unlike"></form>`;
            document.querySelector(`#profile-posts-${item.id}`).append(UnLikePost);    

        });
    });
}  

function getEditView(theID) {
    fetch('/editPost/'+theID)
    .then(response => response.json())
    .then(allFollowing => {
        allFollowing.forEach(function(item) {
            const EditPost = document.createElement('div');
            EditPost.className = 'edit-area';
            EditPost.style = 'border-style: dotted';
            EditPost.innerHTML = `<textarea class="form-control" id="edit-textarea" rows="5">${item.postText}</textarea>`;
            document.querySelector(`#profile-posts-${item.id}`).append(EditPost);    
        });
        updateDiv = document.querySelector('#edit-div');
        updateDiv.innerHTML = `<div><input id="update${theID}" class="btn btn-info" type="submit" value="Update"></input></div>`
        document.querySelector(`#profile-posts-${theID}`).append(updateDiv);
    });
}

function edit(theID) {
    fetch('/editUpdate/'+theID, {
        method: 'PUT',
        body: JSON.stringify({
            post_text: document.querySelector('#edit-textarea').value
        })
      });
}

function getPostFromID(postID) {
    fetch('/editPost/'+postID)
    .then(response => response.json())
    .then(allFollowing => {
        allFollowing.forEach(function(item) {
            if (item.id == postID) {
                thePost = item;
            }
        });
    });
}


function likePost(theID) {
    fetch('/likeUpdate/'+theID, {
        method: 'POST',
        body: JSON.stringify({
            user: theUser,
            likedPost: thePost
        })
      })
      .then(response => response.json())
      .then(result => {
          console.log(result);
      });
}

function unlikePost(theID) {
    fetch('/unlikeUpdate/'+theID, {
        method: 'POST',
        body: JSON.stringify({
            user: theUser,
            likedPost: thePost
        })
      })
      .then(response => response.json())
      .then(result => {
          console.log(result);
      });
}