window.addEventListener('load', function() {
    // Example POST method implementation:
    async function kbPostData(url = '', data = {}) {
        // Default options are marked with *
        const response = await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'same-origin', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(data) // body data type must match "Content-Type" header
        });
    return response.json(); // parses JSON response into native JavaScript objects
  }

    document.querySelector(".kanban-board-move").addEventListener('click', function() { 
        kbPostData(this.dataset.link, { kb_parent_id: this.dataset.board, kb_element_id: this.dataset.element, kb_new_status: this.dataset.targetState })
            .then(data => {
                window.location.reload();
            });
    });
})