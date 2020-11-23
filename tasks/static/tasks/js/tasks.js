let yesterdayDate = new Date();
yesterdayDate.setDate(yesterdayDate.getDate() - 1);

function formatDateToString(date) {
    const day = (date.getDate() < 10 ? '0' : '') + date.getDate();

    const month = ((date.getMonth() + 1) < 10 ? '0' : '') + (date.getMonth() + 1);

    return date.getFullYear() + '-' + month + '-' + day;
}

const yesterdayDateElement = document.getElementById('date-col-' + formatDateToString(yesterdayDate));

yesterdayDateElement.scrollIntoView();
