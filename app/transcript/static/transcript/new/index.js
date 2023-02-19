const form = document.getElementById("form");
const inputFile = document.getElementById("file");

const formData = new FormData();

const handleSubmit = (event) => {
    event.preventDefault();

    for (const file of inputFile.files) {
        formData.append("file", file);
    }
    var audio_id;
    var language;
    fetch("http://localhost:8000/api/v1/audio/", {
        method: "post", body: formData,
    }).then((response) => {
        if (response.status != 200) {
            alert('Failed to upload audio. Maybe filename exists')
            throw new Error('Failed to upload audio')
        }
        return response.json()
    })
        .then((result) => {
            audio_id = result.id
            language = $('input[name="customRadioInline1"]:checked').val()
            console.log(result.id)
            console.log('Audio uploaded')
            fetch("http://localhost:8000/api/v1/transcript", {
                method: "post", body: JSON.stringify({audio_id: audio_id, language: language}), headers: {
                    'Content-Type': 'application/json',
                },
            }).then((response) => {
                if (response.status != 200) {
                    alert('Failed to create new transcript')
                    throw new Error('Failed to create transcript')
                }
                return response.json()
            }).then((data) => {
                alert("Success. Transcript id:" + data.id.toString())
                window.location.replace("/transcript");
            })
        })
        .catch((error) => {
            console.log(error)
        })
};

form.addEventListener("submit", handleSubmit);