$(document).ready(function () {
    // this function for user follow and un follow
    $('[id^=follow-and-unfollow-]').on('click', function () {
        const button = $(this);
        const userId = button.val();
        const csrfToken = button.data('csrf-token');

        $.ajax({
            type: 'POST',
            url: '/account/follow-user/',
            data: {'csrfmiddlewaretoken': csrfToken, 'user_id': userId},
            success: function (response) {
                if (response.followed) {
                    button.text('Un Follow');

                } else {
                    button.text('Follow');
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
    });


//     this code for post list in explore
    $(document).ready(function () {
        let page = 2;
        let urlPage = '/explore/'
        let loading = false;

        $(window).scroll(function () {
            if ($(window).scrollTop() + $(window).height() >= $(document).height() - 1) {
                if (!loading) {
                    loading = true;

                    $.ajax({
                        type: 'GET',
                        url: urlPage + "?page=" + page,
                        dataType: 'html',
                        success: function (data) {
                            $('#post-list').append(data);
                            page += 1;
                            loading = false;
                        },
                        error: function () {
                            loading = false;
                        }
                    });
                }
            }
        });
    });


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
            const deleteLink = document.getElementById("delete-post-link");
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


function showStoryDetail(userId) {
    fetch(`/story-detail/${userId}/`)
        .then(response => response.text())
        .then(data => {
            if (data.trim()) {
                document.getElementById('modal-content-story').innerHTML = data;
                document.getElementById('storyModal').style.display = 'flex';

                const storyItems = document.querySelectorAll('.item');
                let currentIndex = 0;

                function sendViewRequest(storyItem) {
                    const storyId = storyItem.dataset.storyId;
                    fetch(`/add-visit-story/${storyId}/${userId}/`)
                        .then(response => response.json())
                        .then(data => {
                            const deleteStoryLink = document.getElementById('delete-story-link')
                            if (deleteStoryLink){
                                deleteStoryLink.href = `/delete-story/${storyId}/`
                            }
                            const storyCreatedDate = document.getElementById('story-created-date');
                            storyCreatedDate.innerHTML = '';
                            storyCreatedDate.innerHTML = data.time_since_created + ' ago';


                            const viewers = data.viewers;
                            const viewerListContainer = document.querySelector('.viewer-list-container');
                            viewerListContainer.innerHTML = '';
                            viewers.forEach(viewer => {
                                const userElement = document.createElement('div');
                                userElement.classList.add('viewer-item');
                                 userElement.innerHTML = `
                                    <img src="/media/${viewer.user__avatar}" alt="Profile Picture" class="viewer-profile-pic">
                                    <div class="viewer-info">
                                        <h4 class="viewer-username">
                                            <a href="/explore/user/${viewer.user__username}">
                                            ${viewer.user__username}
                                            </a>
                                        </h4>
                                        <p class="viewer-fullname">${viewer.user__username}</p>
                                     </div>
            `;
                                 viewerListContainer.appendChild(userElement);


                            })
                            console.log(data.visit_count)
                            document.getElementById('view-count').innerHTML = data.visit_count;



                        })
                }


                sendViewRequest(storyItems[currentIndex]);

                document.querySelector('.next-button').addEventListener('click', function () {
                    currentIndex = (currentIndex + 1) % storyItems.length;
                    showCurrentStory();
                });

                document.querySelector('.prev-button').addEventListener('click', function () {
                    currentIndex = (currentIndex - 1 + storyItems.length) % storyItems.length;
                    showCurrentStory();
                });

                function showCurrentStory() {
                    storyItems.forEach((item, index) => {
                        item.style.display = index === currentIndex ? 'block' : 'none';
                    });
                    sendViewRequest(storyItems[currentIndex]);
                }

                showCurrentStory();
            } else {
                console.warn("No story content available.");
            }
        })
        .catch(error => console.error("Error loading story details:", error));
}

function previewFile() {
    const previewContainer = document.getElementById('preview-container');
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];


    previewContainer.innerHTML = '';

    if (file) {
        const fileType = file.type;


        if (fileType.startsWith('image')) {
            const img = document.createElement('img');
            img.src = URL.createObjectURL(file);
            img.classList.add('preview-image');
            previewContainer.appendChild(img);
        } else if (fileType.startsWith('video')) {
            const video = document.createElement('video');
            video.src = URL.createObjectURL(file);
            video.controls = true;
            video.classList.add('preview-video');
            previewContainer.appendChild(video);
        }
    }
}
