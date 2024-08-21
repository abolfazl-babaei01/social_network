$(document).ready(function () {
    // this function for user follow and un follow
    $('#follow-and-unfollow').on('click', function () {
        const button = $(this);
        const userId = button.val();
        const csrfToken = button.data('csrf-token');

        $.ajax({
            type: 'POST',
            url: '/account/follow-user/',
            data: {'csrfmiddlewaretoken': csrfToken, 'user_id': userId},
            success: function (response) {
                if (response.followed) {
                    $('#follow-and-unfollow').text('Un Follow');

                } else {
                    $('#follow-and-unfollow').text('Follow');
                }
                if (response.follow_yourself) {
                    alert('You cannot follow yourself!')
                }
                $('#followers-count').text(response.followers_count);
                $('#following-count').text(response.following_count);

            }
        });

    });
    // this function for like post
    $(document).on('click', '.like-post', function() {
        const $this = $(this);
        const postId = $(this).data('post-id');
        const csrfToken = $(this).data('csrf-token');
        $.ajax({
            type: 'POST',
            url: '/account/like-post/',
            data: {'csrfmiddlewaretoken': csrfToken, 'post_id': postId},
            success: function (response) {
                const icon = $this.find('svg');
                if (response.liked) {
                    icon.removeClass('fa-regular').addClass('fa-solid');
                } else {
                    icon.removeClass('fa-solid').addClass('fa-regular');
                }
                $this.find('.like-count').text(response.like_count);
            }
        })
    });

    $(document).on('click', '.save-post', function() {
        const $this = $(this);
        const postId = $(this).data('post-id');
        const csrfToken = $(this).data('csrf-token');

        $.ajax({
            type: 'POST',
            url : '/account/save-post/',
            data: {'csrfmiddlewaretoken': csrfToken, 'post_id': postId},
            success: function (response){
                const icon = $this.find('svg');
                console.log(icon)
                if (response.saved){
                    icon.removeClass('fa').addClass('fa-calendar-week');
                }else {
                    icon.removeClass('fa').addClass('fa-calendar-plus');
                }
            }
        })
    })
})

function showPostDetail(postId) {
    // Perform an AJAX request to get the post details
    fetch(`/post/${postId}/`)
        .then(response => response.text())
        .then(data => {
            document.getElementById('modal-body').innerHTML = data;
            document.getElementById('postModal').style.display = 'block';
        });
}

function closeModal() {
    document.getElementById('postModal').style.display = 'none';
}

// Close the modal if the user clicks outside the modal-content area
window.onclick = function(event) {
    let modal = document.getElementById('postModal');
    if (event.target === modal) {
        modal.style.display = "none";
    }
};