document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.diary-form');
    const textarea = form.querySelector('textarea[name="body"]');
    const alertBox = document.createElement('div');
    alertBox.className = 'alert alert-danger';
    alertBox.style.display = 'none';
    alertBox.role = 'alert';
    alertBox.innerText = 'Diary entry cannot be empty.';
    form.insertBefore(alertBox, form.firstChild);

    form.addEventListener('submit', function(event) {
        const content = textarea.value.trim();
        if (!content) {
            alertBox.style.display = 'block';
            event.preventDefault();
        } else {
            alertBox.style.display = 'none';
        }
    });

    const deleteButton = document.getElementById('delete-button');
    if (deleteButton) {
        deleteButton.addEventListener('click', function() {
            if (confirm('Are you sure you want to delete this diary entry?')) {
                const entryId = window.location.pathname.split('/').filter(Boolean).pop();
                fetch(`/diary/${entryId}/delete/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCSRFToken(),
                        'Accept': 'application/json',
                    },
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.location.href = '/diary';
                    } else {
                        alert('Failed to delete the diary entry.');
                    }
                })
                .catch(() => {
                    alert('An error occurred while deleting the diary entry.');
                });
            }
        });
    }

    const editButton = document.getElementById('edit-button');
    const diaryBody = document.getElementById('diary-body');
    const editFormContainer = document.getElementById('diary-edit-form');
    const cancelEditButton = document.getElementById('cancel-edit');
    const editDelete = document.querySelector('.edit-delete');

    if (editButton) {
        editButton.addEventListener('click', function() {
            diaryBody.style.display = 'none';
            editFormContainer.style.display = 'block';
            editDelete.style.display = 'none';
        });
    }

    if (cancelEditButton) {
        cancelEditButton.addEventListener('click', function() {
            editFormContainer.style.display = 'none';
            diaryBody.style.display = 'block';
            editDelete.style.display = 'block';
        });
    }

    const updateForm = document.getElementById('update-form');
    if (updateForm) {
        updateForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const newBody = updateForm.querySelector('textarea[name="body"]').value.trim();
            if (!newBody) {
                alertBox.style.display = 'block';
                return;
            }
            alertBox.style.display = 'none';

            const entryId = window.location.pathname.split('/').filter(Boolean).pop();
            fetch(`/diary/${entryId}/update/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCSRFToken(),
                    'Accept': 'application/json',
                },
                body: `body=${encodeURIComponent(newBody)}`,
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    diaryBody.innerHTML = `<p>${data.body.replace(/\n/g, '<br>')}</p>`;
                    editFormContainer.style.display = 'none';
                    diaryBody.style.display = 'block';
                    editDelete.style.display = 'block';
                } else {
                    alert(data.error || 'Failed to update the diary entry.');
                }
            })
            .catch(() => {
                alert('An error occurred while updating the diary entry.');
            });
        });
    }

    function getCSRFToken() {
        let cookieValue = null;
        const name = 'csrftoken';
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
