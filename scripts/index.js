function play() {
    var audio = document.getElementById("audio");
    audio.play();
}

let ctx ;
let myChart;

function draw(freq) {    
    ctx = document.getElementById('myChart').getContext('2d');
    myChart = new Chart(ctx, {
        type: 'bar',
        data: {        
            datasets: [{
                //label: '出現頻度',
                data: freq,
                borderColor: [
                    'blue',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 5,
                barThickness: 20
            }],
            labels: ['綜合', '高', '中', '小']
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins:{
                legend: {
                display: false
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', function(){
    const wordObj = selection.getObject();

    let freq = [0,0,0,0];
    freq[0] = wordObj['frequency'];
    freq[1] = wordObj['senior'];
    freq[2] = wordObj['junior'];
    freq[3] = wordObj['elementary'];
    
    draw(freq);

    document.querySelector(".each_word h3").textContent = wordObj['word'];
    let eng_pro = wordObj['pronun_en'].split(',');
    document.querySelector(".pron_en").textContent = "[ "+eng_pro[0].trim()+" ]";
    let jp_pro = wordObj['pronun_jp'].split(',');
    document.querySelector(".pron_jp").textContent = "[ "+jp_pro[0].trim()+" ]";
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

    let freq = [0,0,0,0];
    freq[0] = wordObj['frequency'];
    freq[1] = wordObj['senior'];
    freq[2] = wordObj['junior'];
    freq[3] = wordObj['elementary'];
    myChart.data.datasets[0].data = freq;
    myChart.update();

    document.querySelector(".each_word h3").textContent = wordObj['word'];
    let eng_pro = wordObj['pronun_en'].split(',');
    document.querySelector(".pron_en").textContent = "[ "+eng_pro[0].trim()+" ]";
    let jp_pro = wordObj['pronun_jp'].split(',');
    document.querySelector(".pron_jp").textContent = "[ "+jp_pro[0].trim()+" ]";
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





