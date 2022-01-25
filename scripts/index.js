function play() {
    var audio = document.getElementById("audio");
    audio.play();
}

document.addEventListener('DOMContentLoaded', function(){
    const wordObj = selection.getObject();

    document.querySelector(".each_word h3").textContent = wordObj['word'];
    document.querySelector(".pron_en").textContent = wordObj['pronun_en'];
    document.querySelector(".pron_jp").textContent = wordObj['pronun_jp'];
    document.querySelector(".right").textContent = wordObj['meaning'];

    src_url =`https://github.com/suyongeum/website/blob/master/audios/${wordObj['word'].charAt(0)}/${wordObj['word']}.mp3?raw=true`;
    document.querySelector("audio").setAttribute('src', src_url); //  .textContent = src_url;

    let length = wordObj['sentence_en'].length;
    let sentence_en = '';
    let sentence_jp = '';
    let div_sentence = document.querySelector(".sentence .right");

    for(let i=0; i<length; i++) {
        sentence_en = (wordObj['sentence_en'])[i];
        p = document.createElement('p');
        p.innerHTML = sentence_en;
        p.className = 'en';
        div_sentence.append(p);

        sentence_jp = (wordObj['sentence_jp'])[i];
        p = document.createElement('p');
        p.innerHTML = sentence_jp;
        p.className = 'jp';
        div_sentence.append(p);

        if (i===5) {
            break;
        }
    }
});

document.addEventListener('dblclick', function(){
    const wordObj = selection.getObject();

    document.querySelector(".each_word h3").textContent = wordObj['word'];
    document.querySelector(".pron_en").textContent = "[ "+wordObj['pronun_en'].trim()+" ]";
    document.querySelector(".pron_jp").textContent = "[ "+wordObj['pronun_jp'].trim()+" ]";
    document.querySelector(".right").textContent = wordObj['meaning'];

    src_url =`https://github.com/suyongeum/website/blob/master/audios/${wordObj['word'].charAt(0)}/${wordObj['word']}.mp3?raw=true`;
    document.querySelector("audio").setAttribute('src', src_url); //  .textContent = src_url;

    let length = wordObj['sentence_en'].length;
    let sentence_en = '';
    let sentence_jp = '';
    let div_sentence = document.querySelector(".sentence .right");
    div_sentence.innerHTML = '';
    
    for(let i=0; i<length; i++) {
        sentence_en = (wordObj['sentence_en'])[i];
        p = document.createElement('p');
        p.innerHTML = sentence_en;
        p.className = 'en';
        div_sentence.append(p);

        sentence_jp = (wordObj['sentence_jp'])[i];
        p = document.createElement('p');
        p.innerHTML = sentence_jp;
        p.className = 'jp';
        div_sentence.append(p);
        if (i===5) {
            break;
        }
    }
});





