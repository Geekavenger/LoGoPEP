function setChartTitle(radio) {

    var title = $('#chartTitle');
    var selectedVal = radio.value;
    var chartTitle = '';
    var yearBoxes = $('.year');
    var allYears = $(yearBoxes)[0];
    var firstYear = $(yearBoxes)[1];
    var messageDiv = $('#yearMessage')[0];

    if (selectedVal == 'ind_Total Municipal Solid Waste') {

        chartTitle = 'Total Municipal Solid Waste'

    }

    if (selectedVal == 'ind_Total Municipal Solid Waste by Management Method') {

        chartTitle = 'Total Municipal Solid Waste by Management Method';

        if (allYears.checked) {
            allYears.checked = false;
            firstYear.checked = true;
        }

    }

    $(title).html(chartTitle);

    $(messageDiv).empty();

}


function unCheckAllYears(checkbox) {

    var yearBoxes = $('.year');
    var allYears = $(yearBoxes)[0];
    var firstYear = $(yearBoxes)[1];
    var totalWaste_method = $('#totalWaste_method')[0];
    var messageDiv = $('#yearMessage')[0];

    if (checkbox.checked) {

        ///// UN-CHECK YEAR BOXES /////
        yearBoxes.attr('checked', false);

        ///// RE-CHECK ONLY THE SELECTED BOX /////
        checkbox.checked = true;

        $(messageDiv).empty();

    }

    if (allYears.checked) {

        if (totalWaste_method.checked) {
            allYears.checked = false;
            firstYear.checked = true;

            var errorTitle = 'Total Municipal Solid Waste by Management Method'
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