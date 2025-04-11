document.addEventListener('DOMContentLoaded', function() {
    let index = 0;
    const slides = document.querySelector('.slides');
    const totalSlides = document.querySelectorAll('.slide').length;

    function nextSlide() {
        index = (index + 1) % totalSlides;
        slides.style.transform = `translateX(-${index * 100}%)`;
    }

    setInterval(nextSlide, 6000); // Giảm tốc độ trượt xuống còn 6 giây
});
