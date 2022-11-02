
var ctx = document.getElementById('lineChart').getContext('2d');
var playtimeChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: {{ playtime_label | tojson }},
        datasets: [{
            label: 'Earnings in $',
            data: {{ playtime_data | tojson }},
            backgroundColor: [
                'rgba(85, 85, 85, 1)'
            ],
            borderColor: [
                'rgb(41, 155, 99)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

var ctx2 = document.getElementById('doughnut').getContext('2d');
var genreChart = new Chart(ctx2, {
    type: 'doughnut',
    data: {
        labels: {{ genre_label | tojson }},
        datasets: [{
            label: 'Genres',
            data: {{ genre_data | tojson }},
            backgroundColor: [
                'rgba(41, 155, 99, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(120, 46, 139, 1)',
            ],
            borderColor: [
                'rgba(41, 155, 99, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(120, 46, 139, 1)',
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

var publisherRes={{publisher_data|tojson}}

var publisherLabels=publisherRes.parray.map(function(e){
    return e.publisher
});

var publisherData=publisherRes.parray.map(function(e){
    return e.count
})

let publisherChart=new Chart("publisher", {
    type:'bar',
    data:{
        labels : publisherLabels,
        datasets:[{
            label:'My Publishers',
            data: publisherData, 
            backgroundColor: [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(255, 205, 86)',
                'rgb(153, 102, 255)',
                'rgb(201, 203, 207)',
                'rgb(255, 159, 64)',
                'rgb(75, 192, 192)',
                'rgb(255, 153, 0)',
                'rgb(255, 0, 102)',
                'rgb(153, 102, 204)']
        }]
    }
});

let wordRes={{wordcloud_data|tojson}};

anychart.onDocumentReady(function () {
    var data = wordRes.wordarray;
        
    var chart = anychart.tagCloud(data);
    chart.angles([0]);
    chart.container("container");
    chart.draw();
});