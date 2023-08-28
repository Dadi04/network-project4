document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#edit_post').addEventListener('click', () => {
        // doesn't work yet, will work
        let text = document.querySelector('.text').innerHTML
        console.log(text)
    });
});