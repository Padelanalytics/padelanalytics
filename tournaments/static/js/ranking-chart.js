// Coppyright (c) 2020 Francisco Javier Revilla Linares to present.
// All rights reserved.

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

/**
 * Function to create a ranking chart. It creates a chart with two Y axis (points and positions)
 *
 * @param {*} ctx the document element to be replaced as Chart
 * @param {Array} yPositions the y axis ranking positions values
 * @param {Array} yPoints the y axis ranking points values
 * @param {Array} yPoints the x axis labels
 * @return Chart object from chartjs library ready to be renderized
 */
function createPersonRanking(ctx, yPositions, yPoints, xLabels) {
    // define chart
    var chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: xLabels,
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


/**
 * Function that creates a new variable per matrix row, the content of the new variables are the row-vectors
 * The variables are created globally
 *
 * @param {String} prefix the prefix for the varible names
 * @param {Array} matrix the matrix with the arrays to be created as variables
 */
function createRowVariables(prefix, matrix){
    var i;
    for(i = 0; i < matrix.length; i++) {
        eval('window.' + prefix + i + '= [' + matrix[i].toString() + '];');
    }
}
