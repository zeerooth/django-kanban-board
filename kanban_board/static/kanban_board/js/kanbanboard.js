window.addEventListener('load', function() {
    // Example POST method implementation:
    async function kbPostData(url = '', data = {}, headers = {}) {
        // Default options are marked with *
        const response = await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'same-origin', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: headers,
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(data) // body data type must match "Content-Type" header
        });
        return response.json(); // parses JSON response into native JavaScript objects
    }

    function kbGetCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = kbGetCookie('csrftoken');
    var allMoveButtons = document.querySelectorAll(".kanban-board-move");

    Array.from(allMoveButtons).forEach(btn => {
        btn.addEventListener('click', function(event) {
            kbPostData(event.target.dataset.link, { kb_parent_id: event.target.dataset.board, kb_element_id: event.target.dataset.element, kb_new_status: event.target.dataset.targetState }, { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken })
            .then(data => {
                window.location.reload();
            });
        });
    });
})