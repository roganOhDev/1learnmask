var boolchart1 = (jsonData.pm25_grade>=15);
var boolchart2 = (jsonData.pm10_grade>=15);
var boolchart3 = (jsonData.covid_grade>=15); // chart1,2,3 색 지정

// 배경색 변수 선언
var pinkColor = 'pink';
var greenColor = 'rgb(207, 255, 207)';

var covidElement = document.getElementById('covid');
var yellowDustElement = document.getElementById('yellowDust');
var pm10Element = document.getElementById('pm10');
var pm25Element = document.getElementById('pm25');
var coldElement = document.getElementById('cold');

covidElement.style.backgroundColor = jsonData.covid_grade >= 15 ? pinkColor : greenColor;
yellowDustElement.style.backgroundColor = jsonData.yellow_dust_grade >= 15 ? pinkColor : greenColor;
pm10Element.style.backgroundColor = jsonData.pm10_grade >= 15 ? pinkColor : greenColor;
pm25Element.style.backgroundColor = jsonData.pm25_grade >= 15 ? pinkColor : greenColor;
coldElement.style.backgroundColor = jsonData.cold_grade >= 15 ? pinkColor : greenColor;

jsonData.air_quality_graph_data.reverse();

// chart1 배경색 설정
var canvas1 = document.querySelector('.canvas1');
canvas1.style.backgroundColor = boolchart1 ? pinkColor : greenColor;

// chart2 배경색 설정
var canvas2 = document.querySelector('.canvas2');
canvas2.style.backgroundColor = boolchart2 ? pinkColor : greenColor;

// chart3 배경색 설정
var canvas3 = document.querySelector('.canvas3');
canvas3.style.backgroundColor = boolchart3 ? pinkColor : greenColor;

// air quality 차트
const ctx1 = document.getElementById('chart1');
const lineChart1 = new Chart(ctx1, {
  type: 'line',
  data: {
    labels: jsonData.air_quality_graph_data.map(item => item[0]),
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

// pm10 차트
const ctx2 = document.getElementById('chart2');
const lineChart2 = new Chart(ctx2, {
  type: 'line',
  data: {
    labels: jsonData.air_quality_graph_data.map(item => item[0]),
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

// COVID-19 차트
const ctx3 = document.getElementById('chart3');
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
