document.addEventListener('DOMContentLoaded', function() {
    $('body').on('click', '.like', function(){
        console.log("Liked!")
        like(this)
    });
    $('body').on('click', '.dislike', function(){
        console.log("Disliked!")
        dislike(this)
    });

    $('body').on('click', '.follow', function(){
        console.log("Following")
        follow(this)
    });

    $('body').on('click', '.unfollow', function(){
        console.log("Unfollowed!")
        unfollow(this)
    });


});

function follow(user){

    info = $(user)
    info.addClass('unfollow')
    info.removeClass('follow')
    info.html('Following!')
    data = fetch(`/follow/${user.name}`)

}

function unfollow(user){

    info = $(user)
    info.addClass('follow')
    info.removeClass('unfollow')
    info.html('Follow!')
    data = fetch(`/unfollow/${user.name}`)

}


function like(post){

    info = $(post)
    info.addClass('dislike')
    info.removeClass('like')
    count = info.html()
    count++
    info.html(count)
    data = fetch(`/likes/${post.id}`)
    
}

function dislike(post){

    info = $(post)
    info.addClass('like')
    info.removeClass('dislike')
    count = info.html()
    count--
    info.html(count)
    data = fetch(`/dislikes/${post.id}`)

}
