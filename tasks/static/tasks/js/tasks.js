const todayDate = new Date();
const navbar = document.getElementById('menu-navbar');

function formatDateToString(date) {
    const day = (date.getDate() < 10 ? '0' : '') + date.getDate();

    const month = ((date.getMonth() + 1) < 10 ? '0' : '') + (date.getMonth() + 1);

    return date.getFullYear() + '-' + month + '-' + day;
}

const todayDateElement = document.getElementById('date-col-' + formatDateToString(todayDate));

// Scrolling to current date element
todayDateElement.scrollIntoView();

// Adding to scroll navbar height + 10px margin
window.scrollBy(0,-(navbar.offsetHeight + 10));
