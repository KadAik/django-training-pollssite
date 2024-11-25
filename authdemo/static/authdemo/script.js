
console.log("Loaded ...");

function countdown(targetDate) {
    // Get the timer field and update it
    const daysTag = document.getElementById("days");
    const hourstag = document.getElementById("hours");
    const minutesTag = document.getElementById("minutes");
    const secondsTag = document.getElementById("seconds");

    function updateCountdown(){
        // Calculate the time left and update the UI
        let now = new Date().getTime();
        let timeRemaining = targetDate - now;

        // Format timeRemaining timestamp to days:hours:minutes:seconds
        // Note the timestamp is the number of milliseconds since January 1st, 1970

        const days = Math.floor(timeRemaining/(1000*60*60*24));
        const hours = Math.floor((timeRemaining%(1000*3600*24)) / (1000*60*60));
        const minutes = Math.floor((timeRemaining%(1000*60*60)) / (1000*60));
        const seconds = Math.floor((timeRemaining % (1000 * 60)) / 1000);

        //countdownTag.textContent = `${days}d ${hours}h ${minutes}m ${seconds}s`;

        daysTag.textContent = `${days}d`;
        hourstag.textContent = `${hours}h`;
        minutesTag.textContent = `${minutes}m`;
        secondsTag.textContent = `${seconds}s`;

        if (timeRemaining <= 0){
            clearInterval(interval);
            document.getElementById("timer").textContent = "Session expired";
        }
    }

    const interval = setInterval(updateCountdown, 1000);

}

function handle_file_preview(element){
    const file = element.files[0];
    const previewContainer = document.getElementById("preview-container");
    const fileNameField = document.getElementById("file-name");

    // Clear previous preview
    previewContainer.innerHTML = "";

    if (file){
        const url = URL.createObjectURL(file);
        const file_name = file.name;
        // The file is a video:
        if (file.type.startsWith("video/")){
            // Create a video element
            const video = document.createElement("video");
            video.src = url;
            video.controls = true;
            video.style.maxWidth = "100%";

            fileNameField.innerText = file_name;
            previewContainer.appendChild(video);
        }

        // The file is an image
        else if (file.type.startsWith("image/")){
            // Create an image element
            const image = document.createElement("img");
            image.src = url;
            image.alt = file.name;
            image.style.maxWidth = "100%";

            fileNameField.innerText = file_name;
            previewContainer.appendChild(image);
        }
        else{
            previewContainer.innerText = "Unsupported file type."
        }
    }

}

function uploadFile(uri) {

    const file = document.getElementById("file").files[0];
    const chunkSize = 10 * 1024 * 1024; // 10MB

    if (file) {
        uploadFileInChunks(file, chunkSize, uri);
    }
    else{
        console.log("No file selected");
    } 
}


function uploadFileInChunks(file, chunkSize, uri){

    const totalChunks = Math.ceil(file.size / chunkSize);
    const fileExtension = file.name.split('.').pop().toLowerCase();
    let fileName = file.name.split('.').slice(0, -1).join('.');

    // We should sanitize the file name to avoid 400 Bad request
    
    // Replace any non-alphanumeric characters (except for spaces, dots, underscores, and hyphens) with underscores
    fileName = fileName.replaceAll("-", '_').replace(/\s/g, "_").replace(/\W/g, "").replace(/__+/g, "_");

    for(let i = 0; i < totalChunks; i++){
        const chunkStart = i * chunkSize;
        const chunkEnd = Math.min(chunkStart + chunkSize, file.size);
        const fileChunk = file.slice(chunkStart, chunkEnd);

        uploadChunk(fileChunk, i+1, totalChunks, fileName, uri, fileExtension);
    }

}

function uploadChunk(chunk, chunkIndex, totalChunks, fileName, uri, fileExtension) {
    const formData = new FormData();
    formData.append('chunk', chunk);
    formData.append('chunkIndex', chunkIndex);
    formData.append('totalChunks', totalChunks);
    formData.append('fileName', fileName);
    formData.append('fileExtension', fileExtension);

    fetch(uri,
        {
            method: "POST",
            body: formData,
        }
    )
    .then(response => {
        if (response.ok) {
            console.log(`Chunk ${chunkIndex}/${totalChunks} uploaded`);
        } else {
            console.error(`Error uploading chunk ${chunkIndex}`);
        }
    })
    .catch(error => {
        console.error('Chunk upload failed', error);
    });

}