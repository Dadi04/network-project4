document.addEventListener('DOMContentLoaded', () => {
    let all_edit_buttons = document.querySelectorAll('.edit_button');
    all_edit_buttons.forEach(edit_button => {
        edit_button.addEventListener('click', () => {
            // get the post id
            console.log(edit_button)
            let id = edit_button.getAttribute('data-id');
            console.log(id)
            // get Edit and Submit buttons
            let edit = document.getElementById(`edit_post_${id}`);
            let submit = document.getElementById(`submit_${id}`);
            console.log(edit, submit)
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

                edit.style.display = 'block';
                submit.style.display = 'none';
                
                console.log(id)
                fetch(`/edit/${id}`, {
                    method: "POST",
                    headers: {"Content-type": "application/json", "X-CSRFToken": getCookie("csrftoken")},
                    body: JSON.stringify({
                        text: paragrapf.innerHTML
                    })
                })
                .then(response => response.json())        
                .then(result => {
                    console.log(result);
                })
                .catch(error => {
                    console.error(error);
                });
            });
        });
    });  
});

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length == 2) return parts.pop().split(';').shift();
}