var labels = ["2017-01", "2017-02", "2017-03", "2017-04", "2017-05", "2017-06", "2017-07", "2017-08", "2017-09", "2017-10", "2017-11", "2017-12"]
var dataChart = []

for (var i = 0; i < labels.length; i++) {
  dataChart.push({year: labels[i], data: conso_watt[11+i]});
}
Morris.Line({
  element: 'chart-watt-conso',
  data: dataChart,
  xkey: 'year',
  ykeys: ['data'],
  labels: ['Watts']
});
