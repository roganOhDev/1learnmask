function debounce(func, wait = 10, immediate = true) {
    let timeout;
    return function () {
        const context = this;
        const args = arguments;
        const later = function () {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

function checkScroll() {
    const elements = document.querySelectorAll('.animation-element');

    elements.forEach((element) => {
        const elementTop = element.getBoundingClientRect().top;
        const elementBottom = element.getBoundingClientRect().bottom;

        // 화면에 요소가 보이는지 확인
        const isVisible = elementTop < window.innerHeight && elementBottom >= 0;

        // 보이는 요소에 animate 클래스 추가
        if (isVisible) {
            element.classList.add('animate');
        } else {
            element.classList.remove('animate');
        }
    });
}

window.addEventListener('scroll', debounce(checkScroll));
window.addEventListener('resize', debounce(checkScroll));
checkScroll();