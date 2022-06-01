function timeStampToLabels(timestamp){
    let labels = [];
    for (let i = 0; i < timestamp.length; i++) {
        let tt = timestamp[i];
        labels.push(tt.split("-")[1]);
    }
    return labels
}

function RenderFullChart(fullchart, config){
    let datasets = [];
    let labels = [];
    config.forEach(chartConfig => {
        labels = chartConfig.data.labels;
        datasets.push(chartConfig.data.datasets[0]);
    })

    let myChart = new Chart(fullchart, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets
        }
    });
    return myChart;
}

(function (){
    const fullchartconfig = [];
    //let fullchart;


    const charts = document.getElementsByClassName('chart-data');
    Chart.defaults.color = 'white';
    let socket = [];
    let chart = [];
    for (let i = 0; i < charts.length; i++){
        const chartData = JSON.parse(charts[i].dataset.chart.replace(/'/g, '"'));
        const chartConfig = {
            type: chartData.type,
            data: {
                labels: timeStampToLabels(chartData.datetime),
                datasets: [{
                    label: chartData.name,
                    data: chartData.data,
                    borderColor: chartData.color,
                    backgroundColor: chartData.color,
                    tension: 0.3
                }]
            }
        };
        chart[chartData['id']] = new Chart(document.getElementById(`chart-${chartData['id']}`), chartConfig);
        //fullchartconfig[chartData['id']] = chartConfig;

        if (location.protocol === 'http:') {
            socket[chartData.id] = new WebSocket('ws://' + location.host +
                                                    `/chart/data/${chartData['device_id']}/${chartData['sensor']}/${chartData['samples'] }`);
        } else {
            socket[chartData.id] = new WebSocket('wss://' + location.host +
                                                     `/chart/data/${chartData['device_id']}/${chartData['sensor']}/${chartData['samples'] }`);
        }
        socket[chartData.id].addEventListener('message', ev => {
            const data = JSON.parse(ev.data);
            //fullchartconfig[chartData['id']].data.datasets[0].data = data.data;
            //fullchartconfig[chartData['id']].data.labels = timeStampToLabels(data.timestamp);
            //fullchart.update();
            chart[chartData['id']].data.labels = timeStampToLabels(data.timestamp);
            chart[chartData['id']].data.datasets[0].data = data.data;
            chart[chartData['id']].update();
        })
    }
    //fullchart = RenderFullChart(document.getElementById('full-chart'), fullchartconfig);

})();
