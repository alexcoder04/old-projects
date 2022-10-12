const audioDomEl = document.getElementById("player");
const playPauseBtn = document.getElementById("play-pause");
const skipBtn = document.getElementById("skip");
const songSelectBtns = Array.from(document.getElementsByClassName("song-select"));
const addSongBtn = document.getElementById("add-song");
const currentSongDisp = document.getElementById("current-song");
const songSearchEl = document.getElementById("song-search");

const getNewSong = () => {
    audioDomEl.src = "/module/streamer/random-song";
};

const togglePlayPause = () => {
    if (audioDomEl.paused){
        audioDomEl.play();
        playPauseBtn.innerHTML = "<i class='fa fa-pause'></i>Pause";
        return;
    }
    playPauseBtn.innerHTML = "<i class='fa fa-play'></i>Play";
    audioDomEl.pause();
};

const dl = () => {
    fetch(`/module/streamer/dl?url=${document.querySelector('#dl-link').value}`)
        .then(res => {
            window.location.href = window.location.href;
        })
        .catch(err => {
            console.error(err);
        });
};

playPauseBtn.addEventListener("click", togglePlayPause);
skipBtn.addEventListener("click", getNewSong);
songSelectBtns.forEach(btn => {
    btn.addEventListener("click", e => {
        audioDomEl.src = `/module/streamer/song?song=${e.target.dataset.href}`;
        currentSongDisp.innerText = e.target.innerText;
    });
});
addSongBtn.addEventListener("click", dl);
songSearchEl.addEventListener("keypress", e => {
    songSelectBtns.forEach(el => {
        if(!el.innerText.includes(songSearchEl.value)){
            el.classList.add("hidden");
        } else {
            el.classList.remove("hidden");
        }
    });
});
