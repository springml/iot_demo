$(function(){

    //get the doughnut chart canvas
    var ctx1 = $("#doughnut-chartcanvas-1");
    //var ctx2 = $("#doughnut-chartcanvas-2");

    //doughnut chart data
    var data1 = {
        labels: ["Temperature", "Humidity"],
        datasets: [
            {
                data: [50, 10],
                backgroundColor: [
                    "#ef5350",
                    "#D3D3D3"
                ],
                /*borderColor: [
                    "#CDA776",
                    "#989898",
                ],*/
		hoverBackgroundColor: [
                        "#b61827",
                        "#D3D3D3"
                ],
                borderWidth: [1, 1]
            }
        ]
    };

    //doughnut chart data
    /*var data2 = {
        labels: ["match1", "match2", "match3", "match4", "match5"],
        datasets: [
            {
                label: "TeamB Score",
                data: [20, 35, 40, 60, 50],
                backgroundColor: [
                    "#FAEBD7",
                    "#DCDCDC",
                    "#E9967A",
                    "#F5DEB3",
                    "#9ACD32"
                ],
                borderColor: [
                    "#E9DAC6",
                    "#CBCBCB",
                    "#D88569",
                    "#E4CDA2",
                    "#89BC21"
                ],
                borderWidth: [1, 1, 1, 1, 1]
            }
        ]
    }; */

    //options
    var options = {
        responsive: true,
	animation: {
                animateRotate: true,
                animateScale: true,
                animateRotate : true,
        }, 
	rotation: 3/4 * Math.PI,
        circumference: (3/2) * Math.PI, 
        title: {
            display: true,
            position: "top",
            text: "Doughnut Chart",
            fontSize: 18,
            fontColor: "#111"
        },
        legend: {
            display: true,
            position: "bottom",
            labels: {
                fontColor: "#333",
                fontSize: 16
            }
        }
    };

    //create Chart class object
    var chart1 = new Chart(ctx1, {
        type: "doughnut",
        data: data1,
        options: options
    });

    //create Chart class object
    /*var chart2 = new Chart(ctx2, {
        type: "doughnut",
        data: data2,
        options: options
    });*/
});

function getSensorReadings(device,unit){    
                var sensordata =  $.ajax({
                        type: "GET",
                        url:'http://192.168.2.22:8080/getSensorReadingsForDevice?deviceId='+unit+'&industrialPlantId='+device,
                        async: false
                }).responseText;
                var myObject = eval('(' + sensordata + ')');
                return myObject;
   }

