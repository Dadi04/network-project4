document.addEventListener('DOMContentLoaded', () => {
    // Edit Post Logic
    let all_edit_buttons = document.querySelectorAll('.edit_button');
    all_edit_buttons.forEach(edit_button => {
        edit_button.addEventListener('click', () => {
            // get the post id
            let id = edit_button.getAttribute('data-id');

            // get Edit and Submit buttons
            let edit = document.getElementById(`edit_post_${id}`);
            let submit = document.getElementById(`submit_${id}`);

            // after clicking the button hide Edit and show Submit
            edit.style.display = 'none';
            submit.style.display = 'block';

            // get the existing post text and textarea before the change
            let paragrapf = document.getElementById(`text_${id}`);
            let textarea = document.getElementById(`textarea_${id}`);

            // hide existing post text and show a field to edit the text
            paragrapf.style.display = 'none';
            textarea.style.display = 'block';

            submit.addEventListener('click', () => {
                // after submiting the changes show now edited text and hide text area
                paragrapf.style.display = 'block';
                textarea.style.display = 'none';
                
                paragrapf.innerHTML = textarea.value;

                // and show Edit button again, but hide Submit
                edit.style.display = 'block';
                submit.style.display = 'none';

                // and post changes to database
                fetch(`/edit/${id}`, {
                    method: "POST",
                    headers: {"Content-type": "application/json", "X-CSRFToken": getCookie("csrftoken")},
                    body: JSON.stringify({
                        text: paragrapf.innerHTML
                    })
                })
                .then(response => response.json())
                .catch(error => {
                    console.error(error);
                });
            });
        });
    });
    
    // Like/Unlike Post Logic

    // Unlike need to be implemented
    let all_like_buttons = document.querySelectorAll('.like_button');
    all_like_buttons.forEach(like_button => {
        like_button.addEventListener('click', () => {
            let id = like_button.getAttribute('data-id');
            if (!like_button.classList.contains('liked')) {
                let likes = parseInt(like_button.textContent);
                likes = likes + 1;
                like_button.textContent = likes;

                like_button.classList.add('liked');

                fetch(`/like/${id}`, {
                    method: "POST",
                    headers: {"Content-type": "application/json", "X-CSRFToken": getCookie("csrftoken")},
                    body: JSON.stringify({
                        likes: like_button.textContent
                    })
                })
                .then(response => response.json())
                .catch(error => {
                    console.error(error);
                });
            }
        });
    });
});

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length == 2) return parts.pop().split(';').shift();
}