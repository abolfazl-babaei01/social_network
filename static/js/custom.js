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
    $(document).on('click', '.like-post', function () {
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

    $(document).on('click', '.save-post', function () {
        const $this = $(this);
        const postId = $(this).data('post-id');
        const csrfToken = $(this).data('csrf-token');

        $.ajax({
            type: 'POST',
            url: '/account/save-post/',
            data: {'csrfmiddlewaretoken': csrfToken, 'post_id': postId},
            success: function (response) {
                const icon = $this.find('svg');
                if (response.saved) {
                    icon.removeClass('far').addClass('fas fa-bookmark');
                    $.notify('saved post!', 'success')
                } else {
                    icon.removeClass('fas').addClass('far fa-bookmark');
                    $.notify('un saved post!', 'error')
                }
            }
        })
    });

    $(document).on('click', '.send-comment', function (e) {
        e.preventDefault()
        const commentText = $('#comment-text').val();
        const parentId = $('.parent-id').val();
        const postId = $(this).data('post-id');
        const csrfToken = $(this).data('csrf-token');
        $.ajax({
            type: 'POST',
            url: '/account/add-comment/',
            data: {
                'post_id': postId,
                'comment_text': commentText,
                'parent_id': parentId,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function (data) {

                $('#comment').html(data.html)
                $('#comment-text').val('');
                $('.parent-id').val('');
            },
        })
    })
});

function addParentId(parentId) {
    $('.parent-id').val(parentId);
    $.notify('activate reply', 'info')
}

function showPostDetail(postId) {
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


window.onclick = function (event) {
    let modal = document.getElementById('postModal');
    if (event.target === modal) {
        modal.style.display = "none";
    }
};

