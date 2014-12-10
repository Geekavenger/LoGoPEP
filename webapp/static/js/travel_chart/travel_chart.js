function setChartTitle(radio) {

    var title = $('#chartTitle');
    var selectedVal = radio.value;
    var chartTitle = '';

    if (selectedVal == 'ind_Total VMT') {

        chartTitle = 'Total VMT'

    }

    $(title).html(chartTitle);

}


function unCheckAllYears(checkbox) {

    var yearBoxes = $('.year');

    if (checkbox.checked) {

        ///// UN-CHECK YEAR BOXES /////
        yearBoxes.attr('checked', false);

        ///// RE-CHECK ONLY THE SELECTED BOX /////
        checkbox.checked = true

    }

}