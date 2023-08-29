document.addEventListener('DOMContentLoaded', () => {
    let id = document.querySelector('.profilelink').getAttribute('data-id');
    let edit = document.getElementById(`edit_post_${id}`);

    edit.addEventListener('click', () => {
        // after clicking the button hide Edit and show Submit
        let submit = document.getElementById(`submit_${id}`);

        edit.style.display = 'none';
        submit.style.display = 'block';

        // get this post id, existing post text and textarea before the change
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
            //let post_id = a
            //fetch(`/profile/${user}/${post_id}`, {
            //    method: 'PUT',
            //    body: JSON.stringify({
            //        text: paragrapf,
            //        timestamp: new Date()
            //    })
            //})
            //.catch(error);
        })
    });
});

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length == 2) return parts.pop().split(';').shift();
}