document.getElementById('imageForm').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent form submission

    const imageInput = document.getElementById('imageInput');
    const uploadingAnimation = document.getElementById('uploadingAnimation');
    const resultMessage = document.getElementById('resultMessage');
    const imagePreviewContainer = document.getElementById('imagePreviewContainer');
    const imagePreview = document.getElementById('imagePreview');

    if (imageInput.files.length > 0) {
        const file = imageInput.files[0];
        const formData = new FormData();
        formData.append('image', file);

        // Reset previous results
        resultMessage.classList.add('hidden');
        imagePreviewContainer.classList.add('hidden');
        imagePreview.src = '';

        // Show uploading animation
        uploadingAnimation.classList.remove('hidden');

        // Simulate an upload with a mock API call
        setTimeout(() => {
            // Mock API response
            const fakeServerURL = URL.createObjectURL(file); // Simulate a server URL for the image

            // Hide uploading animation
            uploadingAnimation.classList.add('hidden');

            // Display "Good" message and the uploaded image
            resultMessage.classList.remove('hidden');
            imagePreviewContainer.classList.remove('hidden');
            imagePreview.src = fakeServerURL;
        }, 2000); // Simulate 2 seconds upload time
    } else {
        alert("Please select an image before submitting.");
    }
});
