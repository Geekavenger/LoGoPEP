function setChartTitle(radio) {

    var title = $('#chartTitle');
    var selectedVal = radio.value;
    var chartTitle = '';
    var yearBoxes = $('.year');
    var allYears = $(yearBoxes)[0];
    var firstYear = $(yearBoxes)[1];
    var messageDiv = $('#yearMessage')[0];

    if (selectedVal == 'ind_Total Energy') {

        chartTitle = 'Total Energy'

    }

    if (selectedVal == 'ind_Total Energy by Source') {

        chartTitle = 'Total Energy Use by Source';

        if (allYears.checked) {
            allYears.checked = false;
            firstYear.checked = true;
        }

    }

    if (selectedVal == 'ind_Total Energy by Type') {

        chartTitle = 'Total Energy Use by Type';

        if (allYears.checked) {
            allYears.checked = false;
            firstYear.checked = true;
        }

    }

    if (selectedVal == 'ind_Residential Energy') {

        chartTitle = 'Residential Energy'

    }

    if (selectedVal == 'ind_Commercial/Industrial Energy') {

        chartTitle = 'Commercial/Industrial Energy'

    }

    $(title).html(chartTitle);

    $(messageDiv).empty();

}

function hideWeatherNorm() {

    var weather = $('.weather');
    var weather_norm = $('#weather');

    $(weather_norm).attr('checked', false);
    $(weather).fadeOut(300)

}

function showWeatherNorm() {
    $('.weather').fadeIn(300)
}

function unCheckAllYears(checkbox) {

    var yearBoxes = $('.year');
    var allYears = $(yearBoxes)[0];
    var firstYear = $(yearBoxes)[1];
    var totalEnergy = $('#totalEnergy_source')[0];
    var totalEnergy_type = $('#totalEnergy_type')[0];
    var messageDiv = $('#yearMessage')[0];

    if (checkbox.checked) {

        ///// UN-CHECK YEAR BOXES /////
        yearBoxes.attr('checked', false);

        ///// RE-CHECK ONLY THE SELECTED BOX /////
        checkbox.checked = true;

        $(messageDiv).empty();

    }

    if (allYears.checked) {

        var errorTitle = false;

        if (totalEnergy.checked) {
            allYears.checked = false;
            firstYear.checked = true;

            errorTitle = 'Total Energy by Source'
        }

        if (totalEnergy_type.checked) {
            allYears.checked = false;
            firstYear.checked = true;

            errorTitle = 'Total Energy by Type'
        }

        if (errorTitle) {

            $(messageDiv).empty();
            $(messageDiv).append(
                    '<h3 id="noAverageMessage">Sorry, you cannot have all years selected and view ' + errorTitle + '.</h3>'
            );

        }

        else {
            $(messageDiv).empty();
        }

    }

}