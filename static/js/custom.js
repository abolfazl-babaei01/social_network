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
    // this function for save post
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
        const postId = $(this).data('post-id');
        const commentText = $('#comment-text-' + postId).val();
        const parentId = $('#parent-id-' + postId).val();

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

                $('#comment-' + postId).html(data.html)
                $('#comment-text-' + postId).val('');
                $('#parent-id-' + postId).val('');
            },
        })
    })
});

function addParentId(parentId, postId) {
    $('#parent-id-' + postId).val(parentId);
    $.notify('reply to comment was activated', 'success')
}


function showPostDetail(postId) {
    fetch(`/post/${postId}/`)
        .then(response => response.text())
        .then(data => {
            document.getElementById('modal-body').innerHTML = data;
            var deleteLink = document.getElementById("delete-post-link");
            if (deleteLink) {
                deleteLink.href = '/account/delete-post/' + postId
            }

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


document.getElementById('add-more').addEventListener('click', function () {
    let formsetDiv = document.getElementById('image-formset');
    let totalForms = document.getElementById('id_form-TOTAL_FORMS');
    let currentForms = parseInt(totalForms.value);
    let maxForms = 10;
    if (currentForms < maxForms) {
        let newForm = formsetDiv.querySelector('.form-row').cloneNode(true);
        let formRegex = new RegExp(`form-(\\d){1}-`, 'g');
        newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${currentForms}-`);
        formsetDiv.appendChild(newForm);
        totalForms.value = currentForms + 1;
    } else {
        $.notify("You can only add up to 10 images.", "error");
    }
});

