function setChartTitle(radio) {

    var title = $('#chartTitle');
    var selectedVal = radio.value;
    var chartTitle = '';

    if (selectedVal == 'ind_Total GHG Emissions') {

        chartTitle = 'Total GHG Emissions'

    }

    if (selectedVal == 'ind_Energy-Associated GHG Emissions') {

        chartTitle = 'Energy-Associated GHG Emissions';

    }

    if (selectedVal == 'ind_Other GHG Emissions') {

        chartTitle = 'Other GHG Emissions';

    }

    if (selectedVal == 'ind_Travel-Associated GHG Emissions') {

        chartTitle = 'Travel-Associated GHG Emissions'

    }

    if (selectedVal == 'ind_Waste-Associated GHG Emissions') {

        chartTitle = 'Waste-Associated GHG Emissions'

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