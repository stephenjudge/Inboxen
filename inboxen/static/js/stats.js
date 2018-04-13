/*!
 * Copyright (c) 2016 Jessica Tallon & Matt Molyneaux
 * Licensed under AGPLv3 (https://github.com/Inboxen/Inboxen/blob/master/LICENSE)
 */

(function($, Chart) {
    'use strict';

    var chartOpts = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }],
            xAxes: [{
                gridLines: false
            }]
        },
        elements: {
            line: {
                tension: 0
            }
        },
        legend: {
            reverse: true
        },
        animation: {
            duration: 0, // general animation time
        },
        hover: {
            animationDuration: 0, // duration of animations when hovering an item
        },
        responsiveAnimationDuration: 0, // animation duration after a resize
    };

    $.fn.inboxenCharts = function(chartData) {
        return this.each(function() {
            var $this = $(this);
            var statsUrl = $this.data("url");

            if ($this._inboxenCharts !== undefined) {
                return;
            }

            $this._inboxenCharts = [];

            $.get(statsUrl, function(data) {
                if (data.dates === undefined) {
                    console.error("No data returned from server");
                    return;
                }

                // horrible hack to avoid printing the full dates under the X axis
                var fakeLabels = new Array(data.dates.length);
                for (var i = 0; i < data.dates.length; i++) {
                    fakeLabels[i] = "";
                }

                chartData.forEach(function(obj) {
                    var $canvas = $("<canvas></canvas>");
                    var dataSets = [];

                    obj.data.forEach(function(d) {
                        dataSets.push({
                            label: d.label,
                            backgroundColor: d.backgroundColor,
                            borderColor: d.borderColor,
                            data: data[d.dataAttr],
                        });
                    });

                    $this.find(obj.selector).prepend($canvas);

                    $this._inboxenCharts.push(new Chart($canvas, {
                        type: 'line',
                        data: {
                            labels: fakeLabels,
                            datasets: dataSets,
                        },
                        options: chartOpts
                    }));
                });
            });
        });
    };
})(jQuery, Chart);

(function($, Chart) {
    'use strict';

    var colour1 = "rgb(217, 83, 79)";
    var colour2 = "rgb(51, 122, 183)";
    var fill1 = "rgba(217, 83, 79, 0.75)";
    var fill2 = "rgba(51, 122, 183, 0.75)";

    var chartData = [
        {
            selector: "#users-chart",
            data: [
                {
                    label: "Users with inboxes",
                    backgroundColor: fill2,
                    borderColor: colour2,
                    dataAttr: "active_users",
                },
                {
                    label: "Users",
                    backgroundColor: fill1,
                    borderColor: colour1,
                    dataAttr: "users",
                }
            ],
        },
        {
            selector: "#inboxes-chart",
            data: [
                {
                    label: "Inboxes with emails",
                    backgroundColor: fill2,
                    borderColor: colour2,
                    dataAttr: "active_inboxes",
                },
                {
                    label: "Inboxes",
                    backgroundColor: fill1,
                    borderColor: colour1,
                    dataAttr: "inboxes",
                }
            ],
        },
        {
            selector: "#emails-chart",
            data: [
                {
                    label: "Emails read",
                    backgroundColor: fill2,
                    borderColor: colour2,
                    dataAttr: "read_emails",
                },
                {
                    label: "Emails",
                    backgroundColor: fill1,
                    borderColor: colour1,
                    dataAttr: "emails",
                }
            ],
        },
    ];
    $("#stats-chart").inboxenCharts(chartData);
})(jQuery);
