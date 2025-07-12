let currentSlide = 0;
const slides = document.querySelectorAll('.slide');
const dots = document.querySelectorAll('.dot');
const slideTitle = document.getElementById("slide-title");
const slideDesc = document.getElementById("slide-desc");

const slideData = [
  {
    title: "Check Your Financial Progress",
    desc: "Stay on top of your investments and track your financial growth over time.",
  },
  {
    title: "Track Daily Spending Easily",
    desc: "Monitor every rupee you spend with smart tracking and real-time insights.",
  },
  {
    title: "Achieve Your Saving Goals",
    desc: "Set goals, stay consistent, and reach your financial dreams faster.",
  }
];

function showSlide(index) {
  slides.forEach((slide, i) => {
    slide.classList.remove('active');
    dots[i].classList.remove('active');
    if (i === index) {
      slide.classList.add('active');
      dots[i].classList.add('active');
    }
  });

  slideTitle.innerText = slideData[index].title;
  slideDesc.innerText = slideData[index].desc;
  currentSlide = index;
}

function autoSlide() {
  currentSlide = (currentSlide + 1) % slides.length;
  showSlide(currentSlide);
}

setInterval(autoSlide, 4000);

function togglePassword(inputId) {
  const passwordInput = document.getElementById(inputId);
  if (passwordInput.type === "password") {
    passwordInput.type = "text";
  } else {
    passwordInput.type = "password";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  showSlide(0);
});
