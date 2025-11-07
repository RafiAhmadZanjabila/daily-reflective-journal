document.addEventListener('DOMContentLoaded', function() {
    let selectedEnergyType = null;
    let selectedEmotionId = null;
    let selectedEmotionName = '';
    let emotionColor = '';
    const sections = ['section-1', 'section-2', 'section-3', 'section-4', 'section-5'];
    const energyColors = {
        'HEU': '#ec4325',
        'HEP': '#f9d50d',
        'LEU': '#016fdc',
        'LEP': '#06a074'
    };

    const currentHour = new Date().getHours();
    let timeOfDay = '';
    if (currentHour < 12 && currentHour >= 5) {
        timeOfDay = 'morning';
    } else if (currentHour < 18 && currentHour >= 12) {
        timeOfDay = 'afternoon';
    } else {
        timeOfDay = 'evening';
    }
    document.getElementById('time_of_day').textContent = timeOfDay;

    // Section 1
    document.querySelectorAll('.energy-button').forEach(button => {
        button.addEventListener('click', () => {
            selectedEnergyType = button.dataset.type;
            emotionColor = energyColors[selectedEnergyType];
            document.documentElement.style.setProperty('--emotion-color', emotionColor);
            fetch('/api/emotions/?type=' + selectedEnergyType)
                .then(response => response.json())
                .then(data => {
                    const emotionsList = document.getElementById('emotions-list');
                    emotionsList.innerHTML = '';
                    data.forEach(emotion => {
                        const emotionDiv = document.createElement('div');
                        emotionDiv.classList.add('emotion-item');
                        emotionDiv.dataset.id = emotion.id;
                        emotionDiv.dataset.name = emotion.name;
                        emotionDiv.style.backgroundColor = emotionColor;
                        emotionDiv.innerHTML = `<h4>${emotion.name}</h4><p>${emotion.description}</p>`;
                        emotionsList.appendChild(emotionDiv);
                    });
                    showSection('section-2');
                });
        });
    });

    // Section 2
    document.getElementById('back-to-section-1').addEventListener('click', () => {
        showSection('section-1');
    });

    document.getElementById('emotions-list').addEventListener('click', event => {
        if (event.target.closest('.emotion-item')) {
            const emotionItem = event.target.closest('.emotion-item');
            selectedEmotionId = emotionItem.dataset.id;
            selectedEmotionName = emotionItem.dataset.name;
            document.querySelectorAll('.selected-emotion-name').forEach(el => {
                el.textContent = selectedEmotionName;
                el.style.color = emotionColor;
            });
            showSection('section-3');
        }
    });

    let selectedThemes = [];
    let selectedPlaces = [];
    let selectedSurroundings = [];

    // Section 3
    document.getElementById('back-to-section-2').addEventListener('click', () => {
        showSection('section-2');
    });

    document.getElementById('next-to-section-4').addEventListener('click', () => {
        if (selectedThemes.length > 0 && selectedPlaces.length > 0 && selectedSurroundings.length > 0) {
            showSection('section-4');
        } else {
            alert('Please select at least one option in Themes, Places, and Surroundings.');
        }
    });

    document.getElementById('section-3').addEventListener('click', event => {
        if (event.target.classList.contains('option-item')) {
            const item = event.target;
            const id = item.getAttribute('data-id');
            const type = item.getAttribute('data-type');

            item.classList.toggle('selected');

            if (type === 'theme') {
                if (selectedThemes.includes(id)) {
                    selectedThemes = selectedThemes.filter(itemId => itemId !== id);
                } else {
                    selectedThemes.push(id);
                }
            } else if (type === 'place') {
                if (selectedPlaces.includes(id)) {
                    selectedPlaces = selectedPlaces.filter(itemId => itemId !== id);
                } else {
                    selectedPlaces.push(id);
                }
            } else if (type === 'surrounding') {
                if (selectedSurroundings.includes(id)) {
                    selectedSurroundings = selectedSurroundings.filter(itemId => itemId !== id);
                } else {
                    selectedSurroundings.push(id);
                }
            }
        }
    });

    // Section 4
    document.getElementById('back-to-section-3').addEventListener('click', () => {
        showSection('section-3');
    });

    document.getElementById('next-to-section-5').addEventListener('click', () => {
        const description = document.getElementById('description').value.trim();
        if (description.length > 0) {
            showSection('section-5');
        } else {
            alert('Please enter a description.');
        }
    });

    // Section 5
    document.getElementById('back-to-section-4').addEventListener('click', () => {
        showSection('section-4');
    });

    let weatherCondition = '';

    document.querySelectorAll('.weather-icon').forEach(icon => {
        icon.addEventListener('click', () => {
            document.querySelectorAll('.weather-icon').forEach(i => i.classList.remove('selected'));
            icon.classList.add('selected');
            weatherCondition = icon.getAttribute('data-condition');
        });
    });

    // Submit mood entry
    document.getElementById('submit-mood').addEventListener('click', () => {
        const description = document.getElementById('description').value.trim();

        const sleepHours = parseInt(document.getElementById('sleep_hours').value) || 0;
        const sleepMinutes = parseInt(document.getElementById('sleep_minutes').value) || 0;
        const sleep_time = sleepHours * 60 + sleepMinutes;

        const exerciseHours = parseInt(document.getElementById('exercise_hours').value) || 0;
        const exerciseMinutes = parseInt(document.getElementById('exercise_minutes').value) || 0;
        const exercise_time = exerciseHours * 60 + exerciseMinutes;

        const steps = parseInt(document.getElementById('steps').value) || 0;

        const temperature = parseInt(document.getElementById('temperature').value) || 0;

        const createdAt = document.getElementById('created_at').value;

        if (!createdAt || !weatherCondition) {
            alert('Please fill in all required fields.');
            return;
        }

        const data = {
            'emotion_id': selectedEmotionId,
            'themes': selectedThemes,
            'places': selectedPlaces,
            'surroundings': selectedSurroundings,
            'description': description,
            'sleep_time': sleep_time,
            'exercise_minutes': exercise_time,
            'steps': steps,
            'temperature': temperature,
            'weather_condition': weatherCondition,
            'created_at': createdAt,
        };

        fetch('/mood/check-in', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                window.location.href = '/mood';
            } else {
                alert('Error saving mood entry.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error saving mood entry.');
        });
    });

    function showSection(sectionId) {
        sections.forEach(id => {
            document.getElementById(id).style.display = (id === sectionId) ? 'block' : 'none';
        });
    }

    function getCSRFToken() {
        let csrfToken = null;
        const cookies = document.cookie.split(';');
        cookies.forEach(cookie => {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                csrfToken = value;
            }
        });
        return csrfToken;
    }
});
