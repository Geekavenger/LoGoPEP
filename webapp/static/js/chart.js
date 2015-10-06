function checkAllCities(checkbox) {

    var centralBox = $('#centralCities');
    var innerBox = $('#innerSuburbs');
    var outerBox = $('#outerSuburbs');
    var cityBoxes = $('.city');

    if (checkbox.checked) {

        centralBox.attr('checked', false);
        innerBox.attr('checked', false);
        outerBox.attr('checked', false);
        cityBoxes.attr('checked', false);

    }

}


function lookForAllCities(checkbox) {

    var allCityBox = $('#allCities');

    allCityBox.attr('checked', false);

}


function checkCentralCities(checkbox) {

    var allCityBox = $('#allCities');
    var cityBoxes = $('.centralBox');

    if (checkbox.checked) {

        allCityBox.attr('checked', false);
        cityBoxes.prop('checked', true);

    }

    else {

        cityBoxes.attr('checked', false);

    }

}


function checkInnerCities(checkbox) {

    var allCityBox = $('#allCities');
    var cityBoxes = $('.innerBox');

    if (checkbox.checked) {

        allCityBox.attr('checked', false);
        cityBoxes.prop('checked', true);

    }

    else {

        cityBoxes.attr('checked', false);

    }

}


function checkOuterCities(checkbox) {

    var allCityBox = $('#allCities');
    var cityBoxes = $('.outerBox');

    if (checkbox.checked) {

        allCityBox.attr('checked', false);
        cityBoxes.prop('checked', true);

    }

    else {

        cityBoxes.attr('checked', false);

    }

}


function unCheckNormalizes(checkbox) {

    var normalizeBoxes = $('.normalize');

    if (checkbox.checked) {

        ///// UN-CHECK NORMALIZE BOXES /////
        normalizeBoxes.attr('checked', false);

        ///// RE-CHECK ONLY THE SELECTED BOX /////
        checkbox.checked = true

    }

    else {

        $('#noNormalize').prop('checked', true);

    }

}


function unCheckAverages(checkbox) {

    var averageBoxes = $('.average');

    if (checkbox.checked) {

        ///// UN-CHECK AVERAGE BOXES /////
        averageBoxes.attr('checked', false);

        ///// RE-CHECK ONLY THE SELECTED BOX /////
        checkbox.checked = true

    }

}


////////////////////
//  UPDATE CHART  //
////////////////////
function findAllSelectedBoxes(chartType) {

    var l = $("input:checked").length;
    var testArea = $('#testArea');

    if (l == 0) {

        // Nothing checked //

    }

    else {

        var aList = "";
        $('input:checked').each(function () {
            aList += (this.value + ',');
        });

    }

    updateChart(aList, chartType)

}


function updateChart(aList, chartType) {

    var postData = {"aList": aList, 'chartType': chartType};

    var params = {
        type: 'GET',
        data: postData,
        url: "/chart_api/update-chart"
    };

    $.ajax(params)
        .success(chartUpdate_Success)
        .error(ajaxError);

}


function chartUpdate_Success(data) {

    var subTitle = $('#chartSubTitle');

    var chartSubTitle = data.cities + ' | ' + data.years + data.normalizeTitle + data.weatherTitle;

    var vAxisLabel = data.vAxisLabel;
    var vAxisFormat = data.vAxisFormat;

    var errorMessage = data.errorMessage;
    var messageDiv = $('#averageMessage')[0];

    if (errorMessage == null) {
        $(messageDiv).empty();
    }
    else {
        $(messageDiv).empty();
        $(messageDiv).append(errorMessage);
    }

    $(subTitle).html(chartSubTitle);

    var gData = google.visualization.arrayToDataTable(
        data.columns
    );

    var seriesData = data.seriesData;

    var formatPrefix = data.formatPrefix;
    var formatter = new google.visualization.NumberFormat(
        {pattern: vAxisFormat, negativeColor: 'red', negativeParens: true, allowHtml: true});

    var colLen = data.colLen;
    for (var i = 1; i <= colLen; i++) {

        formatter.format(gData, i);

    }

    var options = {
        width: 920,
        height: 600,
        chartArea: {width: 725},
        bar: {groupWidth: '80%'},
        isStacked: true,
        min: 0,
        backgroundColor: 'transparent',
        legend: {position: 'top', alignment: 'end', textStyle: {fontSize: 11}},
        hAxis: {titleTextStyle: {color: 'red'}},
        vAxis: {title: vAxisLabel, gridlines: {color: '#FFFFFF'}, format: vAxisFormat, width: '200px'},
        seriesType: "bars",
        series: seriesData
    };

    var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
    chart.draw(gData, options);

}


function ajaxError(xhr, options, thrownError) {
    alert(xhr.status);
    alert(thrownError);
}