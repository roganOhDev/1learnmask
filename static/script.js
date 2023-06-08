var pm10 = jsonData.pm10_grade;
var pm25 = jsonData.pm25_grade;
var covid = jsonData.covid_grade;
var cold = jsonData.cold_grade;
var yellow = jsonData.yellow_dust_grade;
var grade = jsonData.grade;

var masktext = '';
var pm10text = '';
var pm25text = '';
var covidtext = '';
var coldtext = '';
var yellowtext = '';

/* function isMobileDevice() {
  return (typeof window.orientation !== "undefined") || (navigator.userAgent.indexOf('IEMobile') !== -1);
} */

window.onload = function () {
    // 페이지 로드 후 실행할 작업들을 여기에 작성합니다.
    // 예: 이미지 보여주기 함수 호출
    logcheck();
    pm10image();
    pm25image();
    covidimage();
    coldimage();
    yellowimage();
    drawchart();
    setBackgroundImage();
}

window.addEventListener('DOMContentLoaded', function () {
    /*   var chart1 = document.getElementById('chart1');
      var canvas = document.getElementById('chart11');
      canvas.width = chart1.offsetWidth;
      canvas.height = chart1.offsetHeight;
      var chart2 = document.getElementById('chart2');
      var canvas = document.getElementById('chart22');
      canvas.width = chart2.offsetWidth;
      canvas.height = chart2.offsetHeight;
      var chart3 = document.getElementById('chart3');
      var canvas = document.getElementById('chart33');
      canvas.width = chart3.offsetWidth;
      canvas.height = chart3.offsetHeight; */
    var canvas = document.getElementById('chart11');
    canvas.height = 250;
    var canvas = document.getElementById('chart22');
    canvas.height = 250;
    var canvas = document.getElementById('chart33');
    canvas.height = 250;
});

function logcheck() {
    console.log("코로나", jsonData.covid_grade);
    console.log("감기", jsonData.cold_grade);
    console.log("미세", jsonData.pm10_grade);
    console.log("초미세", jsonData.pm25_grade);
    console.log("황사", jsonData.yellow_dust_grade);
    console.log("총합", jsonData.grade);
    if (grade >= 30) {
        masktext = "MASK ON";
        document.getElementById("div1-5").style.backgroundColor = "#ff1a1a";
    } else {
        masktext = "MASK OFF"
        document.getElementById("div1-5").style.backgroundColor = "#219adf";
    }
    document.getElementById("p6").textContent = masktext;
}

function pm10image() {
    if (pm10 < 7) {
        document.getElementById("div2-1").style.backgroundImage = "url('static/img/good.png')";
        pm10text = "미세먼지가 좋음입니다";
    } else if (pm10 < 15) {
        document.getElementById("div2-1").style.backgroundImage = "url('static/img/soso.png')";
        pm10text = "미세먼지가 보통입니다";
    } else if (pm10 < 30) {
        document.getElementById("div2-1").style.backgroundImage = "url('static/img/bad.png')";
        pm10text = "미세먼지가 나쁨입니다";
    } else {
        document.getElementById("div2-1").style.backgroundImage = "url('static/img/sobad.png')";
        pm10text = "미세먼지가 매우나빠요";
    }
    document.getElementById("s1").textContent = pm10text;
}

function pm25image() {
    if (pm25 < 7) {
        document.getElementById("div3-1").style.backgroundImage = "url('static/img/good.png')";
        pm25text = "초미세먼지가 좋음입니다";
    } else if (pm25 < 15) {
        document.getElementById("div3-1").style.backgroundImage = "url('static/img/soso.png')";
        pm25text = "초미세먼지가 보통입니다";
    } else if (pm25 < 30) {
        document.getElementById("div3-1").style.backgroundImage = "url('static/img/bad.png')";
        pm25text = "초미세먼지가 나쁨입니다";
    } else {
        document.getElementById("div3-1").style.backgroundImage = "url('static/img/sobad.png')";
        pm25text = "초미세먼지가 매우나빠요";
    }
    document.getElementById("s2").textContent = pm25text;
}

function covidimage() {
    if (covid < 7) {
        document.getElementById("div4-1").style.backgroundImage = "url('static/img/good.png')";
        covidtext = "코로나가 좋음입니다";
    } else if (covid < 15) {
        document.getElementById("div4-1").style.backgroundImage = "url('static/img/soso.png')";
        covidtext = "코로나가 보통입니다";
    } else if (covid < 30) {
        document.getElementById("div4-1").style.backgroundImage = "url('static/img/bad.png')";
        covidtext = "코로나가 나쁨입니다";
    } else {
        document.getElementById("div4-1").style.backgroundImage = "url('static/img/sobad.png')";
        covidtext = "코로나가 매우나빠요";
    }
    document.getElementById("s3").textContent = covidtext;
}

function coldimage() {
    if (cold < 7) {
        document.getElementById("div5-1").style.backgroundImage = "url('static/img/good.png')";
        coldtext = "감기가 좋음입니다";
    } else if (cold < 15) {
        document.getElementById("div5-1").style.backgroundImage = "url('static/img/soso.png')";
        coldtext = "감기가 보통입니다";
    } else if (cold < 30) {
        document.getElementById("div5-1").style.backgroundImage = "url('static/img/bad.png')";
        coldtext = "감기가 나쁨입니다";
    } else {
        document.getElementById("div5-1").style.backgroundImage = "url('static/img/sobad.png')";
        coldtext = "감기가 매우나빠요";
    }
    document.getElementById("s4").textContent = coldtext;
}

function yellowimage() {
    if (yellow < 7) {
        document.getElementById("div6-1").style.backgroundImage = "url('static/img/good.png')";
        yellowtext = "황사가 좋음입니다";
    } else if (yellow < 15) {
        document.getElementById("div6-1").style.backgroundImage = "url('static/img/soso.png')";
        yellowtext = "황사가 보통입니다";
    } else if (yellow < 30) {
        document.getElementById("div6-1").style.backgroundImage = "url('static/img/bad.png')";
        yellowtext = "황사가 나쁨입니다";
    } else {
        document.getElementById("div6-1").style.backgroundImage = "url('static/img/sobad.png')";
        yellowtext = "황사가 매우나빠요";
    }
    document.getElementById("s5").textContent = yellowtext;
}

function drawchart() {
    // 미세먼지 차트
    jsonData.air_quality_graph_data.reverse();
    const ctx1 = document.getElementById('chart11');
    document.getElementById('chart11').addEventListener('click', (event) => {
        html2canvas(document.getElementById("chart11")).then(canvas => {
            var dataUrl = canvas.toDataURL();
            new Popup({
                id: "chart1PopUp",
                title: "Fine Dust Data",
                content: '<img src="' + dataUrl + '" style="width: 80%; height: 80%;" alt="Chart"/>',
            }).show();
        });
    });
    const lineChart1 = new Chart(ctx1, {
        type: 'line',
        data: {
            labels: jsonData.air_quality_graph_data.map(item => {
                const date = new Date(item[0]);
                const month = date.getMonth() + 1;
                const day = date.getDate();
                const hours = date.getHours();
                const minutes = date.getMinutes();
                return `${month < 10 ? '0' + month : month}-${day < 10 ? '0' + day : day} ${hours}:${minutes < 10 ? '0' + minutes : minutes}`;
            }),
            datasets: [{
                label: '미세먼지',
                data: jsonData.air_quality_graph_data.map(item => item[1]),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    min: 0
                }
            }
        }
    });
    // 초미세먼지 차트
    const ctx2 = document.getElementById('chart22');
    document.getElementById('chart22').addEventListener('click', (event) => {
        html2canvas(document.getElementById("chart22")).then(canvas => {
            var dataUrl = canvas.toDataURL();
            new Popup({
                id: "chart2PopUp",
                title: "Ultrafine Fine Dust Data",
                content: '<img src="' + dataUrl + '" alt="Chart"/>'
            }).show();
        });
    });
    const lineChart2 = new Chart(ctx2, {
        type: 'line',
        data: {
            labels: jsonData.air_quality_graph_data.map(item => {
                const date = new Date(item[0]);
                const month = date.getMonth() + 1;
                const day = date.getDate();
                const hours = date.getHours();
                const minutes = date.getMinutes();
                return `${month < 10 ? '0' + month : month}-${day < 10 ? '0' + day : day} ${hours}:${minutes < 10 ? '0' + minutes : minutes}`;
            }),
            datasets: [{
                label: '초미세먼지',
                data: jsonData.air_quality_graph_data.map(item => item[2]),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    min: 0
                }
            }
        }
    });
    // 코로나 차트
    const ctx3 = document.getElementById('chart33');
    document.getElementById('chart33').addEventListener('click', (event) => {
        html2canvas(document.getElementById("chart33")).then(canvas => {
            var dataUrl = canvas.toDataURL();
            new Popup({
                id: "chart3PopUp",
                title: "Covid Data",
                content: '<img src="' + dataUrl + '" alt="Chart"/>'
            }).show();
        });
    });
    const lineChart3 = new Chart(ctx3, {
        type: 'line',
        data: {
            labels: jsonData.covid_graph_data.map(item => item[0]),
            datasets: [{
                label: '코로나',
                data: jsonData.covid_graph_data.map(item => item[1]),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    min: 0
                }
            }
        }
    });
}

document.querySelector('.down').addEventListener('click', function (e) {
    e.preventDefault();

    const targetElement = document.querySelector('#sec2');

    window.scrollTo({
    top: targetElement.offsetTop+100,
    behavior: 'smooth'
    });
})
document.querySelector('.down2').addEventListener('click', function (e) {
    e.preventDefault();

    const targetElement = document.querySelector('#sec3');

    window.scrollTo({
    top: targetElement.offsetTop+100,
        behavior: 'smooth'
    });
});

// down3 버튼
document.querySelector('.down3').addEventListener('click', function (e) {
    e.preventDefault();

    const targetElement = document.querySelector('#sec4');

    window.scrollTo({
    top: targetElement.offsetTop+100,
        behavior: 'smooth'
    });
});

document.querySelector('.down4').addEventListener('click', function (e) {
    e.preventDefault();

    const targetElement = document.querySelector('#sec5');

    window.scrollTo({
    top: targetElement.offsetTop+100,
        behavior: 'smooth'
    });
});

document.querySelector('.down5').addEventListener('click', function (e) {
    e.preventDefault();

    const targetElement = document.querySelector('#sec1');

    window.scrollTo({
    top: targetElement.offsetTop+100,
        behavior: 'smooth'
    });
});

function setBackgroundImage() {
    var currentDate = new Date();
    var currentHour = currentDate.getHours();
    var backgroundElement = document.querySelector('.fixed');

    if (currentHour >= 6 && currentHour < 18) {
        backgroundElement.style.backgroundImage = "url('static/img/citysky3.jpg')";
    } else {
        backgroundElement.style.backgroundImage = "url('static/img/citysky1.jpg')";
    }
}
