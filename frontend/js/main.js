$.ajaxSetup({
    beforeSend: function beforeSend(xhr, settings) {
        function getCookie(name) {
            let cookieValue = null;


            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');

                for (let i = 0; i < cookies.length; i += 1) {
                    const cookie = jQuery.trim(cookies[i]);

                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (`${name}=`)) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }

            return cookieValue;
        }

        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        }
    },
});

// if message longer than 180 characters, this function displays the slice 
// notifies user to go to details to read the whole message
function showShortMessages(){
    let shortMessageLength = 100    
    let messages = $(".js-post-message")    
    let dots = $(".js-post-dots") 
    let currentLocation = window.location.href    
        
    if (currentLocation.search("details") != -1){       
        $(".js-post-message").innerText = messages[0]
    }
    else{
        // if not in the details view      
        for(var x = 0; x < messages.length; x++){
            if (messages[x].innerText.length > shortMessageLength){                
                var message_to_post = messages[x].innerText
                message_to_post = message_to_post.slice(0,shortMessageLength)
                messages[x].innerHTML = message_to_post
                dots[x].style.display = 'inline'                               
                dots[x].innerHTML = " ... <small><strong>(Details In Read More)</strong></small>"                     
            }                    
        }
    }    
}
window.onbeforeunload = showShortMessages()

$(document).on("click", ".js-toggle-modal",function(e){
    e.preventDefault()
    // reset modal form before next post 
    if ($(".js-submit").text().trim() == "Edit Post"){
        $(".js-modal-title").text("NewPost")
        $(".js-submit").prop("disabled", false).text("New Post");
        $(".js-post-text").val('')
        $(".js-post-text").attr("data-post-url", "/new/")                    
    }      
    $(".js-modal").toggleClass("hidden") 
})
.on("click", ".js-submit", function(e){
    e.preventDefault()    
    const text = $(".js-post-text").val().trim()
    const $btn = $(this)
    const postUrl = $(".js-post-text").data("post-url")    

    if(!text.length){
        return false
    }
    else {
        $(".js-modal").addClass("hidden")
        $(".js-post-text").val("")
        
        $btn.prop("disabled", true).text("Posting!")
        $.ajax({
            type: 'POST',
            url: postUrl,
            data: {
                text: text
            },
            success: (dataHtml) => {
                $(".js-modal").addClass("hidden");
                //$("#posts-container").prepend(dataHtml);
                $("#posts-container").load(location.href + " #posts-container") // refresh the messages list
                $(".js-post-message").load(location.href + " .js-post-message")
                $btn.prop("disabled", false).text("New Post");
                $(".js-post-text").val('')                                            
            },
            error: (error) => {
                console.warn(error)
                $btn.prop("disabled", false).text("Error");
            }
        });        
    }
    // refresh modal    
    $(".js-modal").load(location.href + " .js-modal")   
})
.on("click", ".js-follow", function(e){
    e.preventDefault()
    const action = $(this).attr("data-action")    

    $.ajax({
        type: 'POST',
        url: $(this).data("url"),
        data: {
            action: action,
            username: $(this).data("username"),
        },
        success: (data) => {           
            $(".js-follow-text").text(data.wording)
            if(action == "follow"){
                // change wording to unfollow
                $(this).attr("data-action", "unfollow")
            }
            else{
                // change to follow
                $(this).attr("data-action", "follow")
            }
            // counter refresh
            $(".js-followers_counter").load(location.href + " .js-followers_counter")
        },
        error: (error) => {
            console.warn(error)                
        }
    });
})

// this function gets the contents of a selected post, gets it ready for edit
.on("mouseenter", "div .js-post", function(e){
    e.preventDefault()
    var posts = $('.js-post')
    var index = posts.index(this)
    postMessage = $('.js-post-message')[index].innerText    
})

// gets a message content from the above event handler and sends it the the back end for update   
.on("click", ".js-edit-post", function(e){
    e.preventDefault()
    var updateUrl = $(this).attr("href")   
    console.log(updateUrl)    
    
    if (postMessage.length){
        $(".js-modal").toggleClass("hidden")
        $(".js-modal-title").text("Edit Post") 
        $(".js-submit").prop("disabled", false).text("Edit Post")
        $(".js-post-text")
            .val(postMessage)              
            .attr("data-post-url", updateUrl)               
    }
    else{
        return false
    }       
})