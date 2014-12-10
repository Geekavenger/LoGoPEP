function setChartTitle(radio) {

    var title = $('#chartTitle');
    var selectedVal = radio.value;
    var chartTitle = '';
    var yearBoxes = $('.year');
    var allYears = $(yearBoxes)[0];
    var firstYear = $(yearBoxes)[1];
    var messageDiv = $('#yearMessage')[0];

    if (selectedVal == 'ind_Total Water') {

        chartTitle = 'Total Water'

    }

    if (selectedVal == 'ind_Total Water by End Use Type') {

        chartTitle = 'Total Water by End Use Type';

        if (allYears.checked) {
            allYears.checked = false;
            firstYear.checked = true;
        }

    }

    if (selectedVal == 'ind_Residential Water') {

        chartTitle = 'Residential Water'

    }

    if (selectedVal == 'ind_Commercial/Industrial Water') {

        chartTitle = 'Commercial/Industrial Water'

    }

    $(title).html(chartTitle);

    $(messageDiv).empty();

}


function unCheckAllYears(checkbox) {

    var yearBoxes = $('.year');
    var allYears = $(yearBoxes)[0];
    var firstYear = $(yearBoxes)[1];
    var totalWater_source = $('#totalWater_source')[0];
    var messageDiv = $('#yearMessage')[0];

    if (checkbox.checked) {

        ///// UN-CHECK YEAR BOXES /////
        yearBoxes.attr('checked', false);

        ///// RE-CHECK ONLY THE SELECTED BOX /////
        checkbox.checked = true;

        $(messageDiv).empty();

    }

    if (allYears.checked) {

        if (totalWater_source.checked) {
            allYears.checked = false;
            firstYear.checked = true;

            var errorTitle = 'Total Water by End Use Type'
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