function setChartTitle(radio) {

    var title = $('#chartTitle');
    var selectedVal = radio.value;
    var chartTitle = '';

    if (selectedVal == 'ind_Total Costs') {

        chartTitle = 'Total Costs'

    }

    if (selectedVal == 'ind_Energy-Associated Costs') {

        chartTitle = 'Energy-Associated Costs';

    }

    if (selectedVal == 'ind_Water-Associated Costs') {

        chartTitle = 'Water-Associated Costs';

    }

    if (selectedVal == 'ind_Travel-Associated Costs') {

        chartTitle = 'Travel-Associated Costs'

    }

    if (selectedVal == 'ind_Waste-Associated Costs') {

        chartTitle = 'Waste-Associated Costs'

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