var theUser = "";
var thePost = "";
document.addEventListener('DOMContentLoaded', function() {
    checkPage = document.querySelector('#checkFollowerPage');
    pageNum = document.querySelector('#thePageNumber').value;
    var globalId = parseInt(0);

    if (checkPage == null) {
        load_posts(pageNum);
    } else {
        getFollowers(pageNum);
    }

    document.addEventListener('click', event => {
        const element = event.target;

        if (element.className == 'btn btn-secondary') {            
            var theId = element.name;
            globalId = theId;
            edit(theId);
        }
    })

    document.addEventListener('click', event => {
        const element = event.target;

        if (element.className == 'btn btn-info') {            
            getEditView(globalId);
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

function load_posts(pageNumber) {
    currentUser = document.querySelector('#loggedInUser').value;

    fetch('/loadPostContent/'+pageNumber)
    .then(response => response.json())
    .then(allPosts => {
        allPosts.forEach(function(item) {               
            const Posts = document.createElement('div');
            Posts.style = 'border-style: solid';
            Posts.innerHTML = `<div id="posts-${item.id}" style="border-style: groove">${item.postText}<p></p> was posted by  <a href="/%23/${item.user}">${item.user}</a> at ${item.timestamp}<p></p> &#128151; : ${item.postLikes}<br></br></div>`;
            document.querySelector('#post-content').append(Posts);

            const LikePost = document.createElement('div');
            LikePost.className = 'like'
            LikePost.innerHTML = `<form id="like-form"><input name="${item.id}" type="submit" class="btn btn-dark" value="Like"></form>`;
            document.querySelector(`#posts-${item.id}`).append(LikePost);    

            const UnLikePost = document.createElement('div');
            UnLikePost.className = 'unlike'
            UnLikePost.innerHTML = `<form id="like-form"><input name="${item.id}" type="submit" class="btn btn-warning" value="Unlike"></form>`;
            document.querySelector(`#posts-${item.id}`).append(UnLikePost);        

            if (currentUser == item.user) {
                const postButton = document.createElement('div');
                postButton.className = 'post';
                postButton.style = 'border-style: dashed';
                postButton.innerHTML =`<input id="edit-post-id" type="hidden" value="${item.id}"><input id="edit-post-button" name="${item.id}" class="btn btn-secondary" type="submit" value="Edit">`;
                document.querySelector('#post-content').append(postButton);
            }
        });
    });
}  

function getFollowers(pageNumber) {
    fetch('/getFollowerPosts/'+pageNumber)
    .then(response => response.json())
    .then(allFollowing => {
        allFollowing.forEach(function(item) {
            const Posts = document.createElement('div');
            Posts.style = 'border-style: solid';
            Posts.innerHTML = `<div id="posts-${item.id}" style="border-style: groove">${item.postText}<p></p> was posted by  <a href="/%23/${item.user}">${item.user}</a> at ${item.timestamp}<p></p> &#128151; : ${item.postLikes}<br></br></div>`;
            document.querySelector('#follower-post-content').append(Posts);

            const LikePost = document.createElement('div');
            LikePost.className = 'like'
            LikePost.innerHTML = `<form id="like-form"><input name="${item.id}" type="submit" class="btn btn-dark" value="Like"></form>`;
            document.querySelector(`#posts-${item.id}`).append(LikePost);    

            const UnLikePost = document.createElement('div');
            UnLikePost.className = 'unlike'
            UnLikePost.innerHTML = `<form id="like-form"><input name="${item.id}" type="submit" class="btn btn-warning" value="Unlike"></form>`;
            document.querySelector(`#posts-${item.id}`).append(UnLikePost);        
        });
    });
}

function edit(theID) {
    document.querySelector('#new-id').value = parseInt(0);

    fetch('/editPost/'+theID)
    .then(response => response.json())
    .then(allFollowing => {
        allFollowing.forEach(function(item) {
            document.querySelector('#add-post-textarea').value = item.postText
        });
        updateDiv = document.querySelector('#updateDiv');
        updateDiv.innerHTML = `<div><input id="update${theID}" class="btn btn-info" type="submit" value="Update"></input></div>`
        document.querySelector('#updateDiv').append(updateDiv);
    });
}

function getEditView(theID) {
    fetch('/editUpdate/'+theID, {
        method: 'PUT',
        body: JSON.stringify({
            post_text: document.querySelector('#add-post-textarea').value
        })
      })
}

function getPostFromID(postID) {
    fetch('/editPost/'+postID)
    .then(response => response.json())
    .then(allFollowing => {
        allFollowing.forEach(function(item) {
            if (item.id == postID) {
                thePost = item;
                theUser = item.user;
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