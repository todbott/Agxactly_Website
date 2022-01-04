$(document).ready(function makeRateOfLossChart(d) {
	var rateOfLossChart = new CanvasJS.Chart("rateOfLossContainer", {
		animationEnabled: true,
		zoomEnabled: true,
		panEnabled: true,
		title: {
			text: "Is the rate of loss increasing, or is it stable? (by ranch)",
			fontFamily: "Verdana, Geneva",
			fontSize: 20
		},
		axisX: {
			title: "Flyover number",
			minimum: 0,
			interval: 1
		},
		axisY2: {
			title: "Percent of crops present (cumulative)",
			suffix: "%",
			maximum: 100
		},
		toolTip: {
			shared: false,
			content: "{name}: {y}" 
		},
		legend: {
			cursor: "pointer",
			verticalAlign: "top",
			horizontalAlign: "center",
			itemclick: toggleDataSeries
		},
		data: [d]
	});
	rateOfLossChart.render();
});

function toggleDataSeries(e) {
	if (typeof (e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
		e.dataSeries.visible = false;
	} else {
		e.dataSeries.visible = true;
	}
	e.chart.render();
};
