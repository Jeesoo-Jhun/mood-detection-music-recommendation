document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData();
    var imageFile = document.getElementById('image').files[0];
    formData.append('image', imageFile);

    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        var resultDiv = document.getElementById('result');
        if (data.playlist) {
            resultDiv.innerHTML = `<p>Recommended Playlist: <a href="${data.playlist}" target="_blank">${data.playlist}</a></p>`;
        } else {
            resultDiv.innerHTML = '<p>No playlist found for the detected emotion.</p>';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
