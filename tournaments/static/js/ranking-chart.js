// define some colors to use it for the graphs
var chartColors = {
    red: 'rgb(255, 99, 132)',
    orange: 'rgb(255, 159, 64)',
    yellow: 'rgb(255, 205, 86)',
    green: 'rgb(75, 192, 192)',
    blue: 'rgb(54, 162, 235)',
    purple: 'rgb(153, 102, 255)',
    grey: 'rgb(201, 203, 207)'
};

// function to create a ranking chart
function createPersonRanking(ctx, yPositions, yPoints) {
    // define chart
    var chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: grLabels,
            datasets: [
                {
                    label: 'Points',
                    fill: false,
                    borderColor: 'royalblue',
                    backgroundColor: 'royalblue',
                    data: yPoints,
                    yAxisID: 'y-axis-1'
                },
                {
                    label: 'Position',
                    fill: false,
                    borderColor: chartColors.red,
                    backgroundColor: chartColors.red,
                    data: yPositions,
                    yAxisID: 'y-axis-2'
                }
            ]
        },
        options : {
            //layout: { padding:10 },
            scales: {
                yAxes: [
                        {
                            id: 'y-axis-1',
                            scaleLabel:
                            {
                              display: true,
                              labelString: 'Points',
                              fontColor: 'royalblue',
                              fontStyle: 'bold',
                              fontSize: '15'
                            }
                        },
                        {
                            id: 'y-axis-2',
                            position: 'right',
                            scaleLabel:
                            {
                              display: true,
                              labelString: 'Position',
                              fontColor: chartColors.red,
                              fontStyle: 'bold',
                              fontSize: '15'
                            },
                            ticks: { reverse: true, min: 1 }
                        }
                    ],
                xAxes: [{scaleLabel: {display: true, labelString: 'Date'}}]
            }
        }
    });
    // return chart
    return chart;
}
