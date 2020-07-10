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

    $('body').on('click', '.edit', function(){
        console.log("Editing")
        edit(this)
    });

    $('body').on('click', '.save', function(){
        console.log("Saved")
        save(this)
    });

});

function follow(user){

    info = $(user)
    info.addClass('unfollow')
    info.removeClass('follow')
    info.html('Following!')

    count = $('#followersCount').html()
    count++
    $('#followersCount').html(count)
    
    data = fetch(`/follow/${user.name}`)

}

function unfollow(user){

    info = $(user)
    info.addClass('follow')
    info.removeClass('unfollow')
    info.html('Follow!')

    count = $('#followersCount').html()
    count--
    $('#followersCount').html(count)

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

function edit(post){
    content = $(`div[name=${post.id}]`)
    console.log(content.html())
    data = content.html()
    content.html(`<textarea id='${post.id}'>${data}</textarea>`)
    
    info = $(post)
    info.html('Save')
    info.removeClass('edit')
    info.addClass('save')
}

function save(post){
    content = $(`div[name=${post.id}]`)
    newdata = $(`textarea[id=${post.id}]`).val()
    console.log(newdata)
    content.html(newdata)


    info = $(post)
    info.html('Edit')
    info.removeClass('save')
    info.addClass('edit')

    data = fetch(`/save/${post.id}/${newdata}`)
}