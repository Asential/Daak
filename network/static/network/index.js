document.addEventListener('DOMContentLoaded', function() {
    $('body').on('click', '.like', function(){
        console.log("Liked!")
        like(this)
    });
    $('body').on('click', '.dislike', function(){
        console.log("Disliked!")
        dislike(this)
    });
});


function like(post){

    info = $(post)
    info.addClass('dislike')
    info.removeClass('like')
    count = info.html()
    count++
    info.html(count)
    data = fetch(`likes/${post.id}`)
    
}

function dislike(post){

    info = $(post)
    info.addClass('like')
    info.removeClass('dislike')
    count = info.html()
    count--
    info.html(count)
    data = fetch(`dislikes/${post.id}`)

}