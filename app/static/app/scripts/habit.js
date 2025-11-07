document.addEventListener('DOMContentLoaded', function() {
    function getCSRFToken() {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith('csrftoken=')) {
                    cookieValue = decodeURIComponent(cookie.substring('csrftoken='.length));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const habitSelect = document.getElementById('habit-select');
    if (habitSelect) {
        const habitNameInput = document.getElementById('habit-name');
        habitSelect.addEventListener('change', toggleInputs);
        habitNameInput.addEventListener('input', toggleInputs);
        habitSelect.style.cursor = 'pointer';

        function toggleInputs() {
            if (habitSelect.value) {
                habitNameInput.disabled = true;
                habitNameInput.style.cursor = 'not-allowed';
                habitNameInput.value = '';
            } else {
                habitNameInput.disabled = false;
                habitNameInput.style.cursor = 'auto';
            }
            if (habitNameInput.value.trim()) {
                habitSelect.disabled = true;
                habitSelect.style.cursor = 'not-allowed';
                habitSelect.value = '';
            } else {
                habitSelect.disabled = false;
                habitSelect.style.cursor = 'pointer';
            }
        }
    
        const addForm = document.querySelector('.diary-form');
        if (addForm && addForm.id !== 'update-form') {
            addForm.addEventListener('submit', function(event) {
                event.preventDefault();
    
                const habitSelect = addForm.querySelector('select[name="habit_id"]');
                const habitNameInput = addForm.querySelector('input[name="habit_name"]');
                const startTime = addForm.querySelector('input[name="start_time"]').value;
                const endTime = addForm.querySelector('input[name="end_time"]').value;
                const description = addForm.querySelector('textarea[name="description"]').value.trim();
    
                if ((!habitSelect.value && !habitNameInput.value.trim()) || !startTime || !endTime) {
                    alert('Please provide all required fields.');
                    return;
                }
    
                if (new Date(startTime) >= new Date(endTime)) {
                    alert('End time must be after start time.');
                    return;
                }
    
                const data = new URLSearchParams();
                if (habitSelect.value) {
                    data.append('habit_id', habitSelect.value);
                } else {
                    data.append('habit_name', habitNameInput.value.trim());
                }
                data.append('start_time', startTime);
                data.append('end_time', endTime);
                data.append('description', description);
    
                fetch(addForm.action, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCSRFToken(),
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Accept': 'application/json',
                    },
                    body: data,
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.location.href = '/habits';
                    } else {
                        alert(data.error || 'Failed to add the habit entry.');
                    }
                })
                .catch(() => {
                    alert('An error occurred while adding the habit entry.');
                });
            });
        }
    }

    const updateForm = document.getElementById('update-form');
    if (updateForm) {
        updateForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const description = updateForm.querySelector('textarea[name="description"]').value.trim();
            const startTime = updateForm.querySelector('input[name="start_time"]').value;
            const endTime = updateForm.querySelector('input[name="end_time"]').value;
            if (!startTime || !endTime) {
                alert('Start time and end time are required.');
                return;
            }
            if (new Date(startTime) >= new Date(endTime)) {
                alert('End time must be after start time.');
                return;
            }
            const entryId = window.location.pathname.split('/').filter(Boolean).pop();
            const data = new URLSearchParams();
            data.append('description', description);
            data.append('start_time', startTime);
            data.append('end_time', endTime);
            fetch(`/habits/${entryId}/update/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept': 'application/json',
                },
                body: data,
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert(data.error || 'Failed to update the habit entry.');
                }
            })
            .catch(() => {
                alert('An error occurred while updating the habit entry.');
            });
        });
    }

    const editButton = document.getElementById('edit-button');
    const deleteButton = document.getElementById('delete-button');
    const habitDescription = document.getElementById('habit-description');
    const habitEditForm = document.getElementById('habit-edit-form');
    const cancelEditButton = document.getElementById('cancel-edit');
    const editDelete = document.querySelector('.edit-delete');

    if (editButton && habitEditForm) {
        editButton.addEventListener('click', function() {
            habitDescription.style.display = 'none';
            habitEditForm.style.display = 'block';
            editDelete.style.display = 'none';
        });
    }

    if (cancelEditButton && habitEditForm) {
        cancelEditButton.addEventListener('click', function() {
            habitEditForm.style.display = 'none';
            habitDescription.style.display = 'block';
            editDelete.style.display = 'block';
        });
    }

    if (deleteButton) {
        deleteButton.addEventListener('click', function() {
            if (confirm('Are you sure you want to delete this habit entry?')) {
                const entryId = window.location.pathname.split('/').filter(Boolean).pop();
                fetch(`/habits/${entryId}/delete/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCSRFToken(),
                        'Accept': 'application/json',
                    },
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.location.href = '/habits';
                    } else {
                        alert(data.error || 'Failed to delete the habit entry.');
                    }
                })
                .catch(() => {
                    alert('An error occurred while deleting the habit entry.');
                });
            }
        });
    }
});
