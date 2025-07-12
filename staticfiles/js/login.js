let currentSlide = 0;
const slides = document.querySelectorAll('.slide');
const dots = document.querySelectorAll('.dot');
const slideTitle = document.getElementById("slide-title");
const slideDesc = document.getElementById("slide-desc");

const slideData = [
  {
    title: "Check Your Financial Progress",
    desc: "Lorem ipsum dolor sit amet tristique urna. Lorem sed pellentesque sit amet ipsum.",
  },
  {
    title: "Track Daily Spending Easily",
    desc: "Monitor every rupee you spend with smart tracking and reports.",
  },
  {
    title: "Achieve Your Saving Goals",
    desc: "Set saving goals and reach them faster with automated planning.",
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

  // Update title and description
  slideTitle.innerText = slideData[index].title;
  slideDesc.innerText = slideData[index].desc;

  currentSlide = index;
}

function autoSlide() {
  currentSlide = (currentSlide + 1) % slides.length;
  showSlide(currentSlide);
}

setInterval(autoSlide, 4000);

function togglePassword() {
  const passwordInput = document.getElementById("password");
  if (passwordInput.type === "password") {
    passwordInput.type = "text";
  } else {
    passwordInput.type = "password";
  }
}
