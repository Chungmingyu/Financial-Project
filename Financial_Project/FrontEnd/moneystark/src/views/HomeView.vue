<template>
  <div id="scrollbar">
    <div class="wrapper">
      <div class="item"><img src="@/assets/1.jpg" alt="" class="background-img" /></div>
      <div class="item">Eaque ullam illum nobis deleniti...</div>
      <div class="item">Animi, porro molestias? Reiciendis dolor...</div>
      <div class="item">Labore, unde amet! Alias delectus hic...</div>
      <div class="item">Quaerat error dolorem aspernatur...</div>
      <div class="item">Rem nobis facere provident magni minima...</div>
      <div class="item">Lorem ipsum, dolor sit amet consectetur...</div>
      <div class="item">Magnam eveniet inventore assumenda ullam...</div>
      <div class="item">Temporibus cum dolor minima consequatur...</div>
      <div class="item">Vitae, tenetur beatae error corrupti...</div>
      <div class="item">Dolor, dolorum beatae accusamus obcaecati...</div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import Scrollbar from "smooth-scrollbar"; // Smooth Scrollbar 라이브러리 import
import { TweenMax, Power4 } from "gsap";

let option = {
  y: 0,
  speed: 1.5,
  limit: 2,
  time: 0.3,
};

let active = 0;
let pag, bullets;

onMounted(() => {
  /*--------------------*/
  /* Init Scrollbar */
  /*--------------------*/
  const scrollbar = Scrollbar.init(document.querySelector("#scrollbar"), {
    damping: 0.1, // 스크롤 감속 비율
    overscrollEffect: "bounce",
    alwaysShowTracks: true,
  });

  const listener = (status) => {
    console.log("scrollbar", status.offset.y);
    active = parseInt(status.offset.y / window.innerHeight);
    bullets.forEach((b) => {
      b.classList.remove("active");
    });
    bullets[active].classList.add("active");
  };
  scrollbar.addListener(listener);

  /*--------------------*/
  /* Pagination */
  /*--------------------*/
  const pagination = () => {
    const items = document.querySelectorAll(".item");
    pag = document.createElement("div");
    pag.classList.add("pagination");
    items.forEach((item, i) => {
      const bullet = document.createElement("button");
      bullet.classList.add("bullet");
      bullet.innerHTML = i;
      pag.appendChild(bullet);
    });
    document.getElementById("scrollbar").appendChild(pag);
    bullets = document.querySelectorAll(".bullet");

    bullets.forEach((b, i) => {
      b.addEventListener("click", (el) => {
        bullets.forEach((el) => {
          el.classList.remove("active");
        });
        el.target.classList.add("active");
        const i = parseInt(el.target.innerHTML);
        active = i;

        let y = window.innerHeight * i;
        if (y > scrollbar.limit.y) {
          y = scrollbar.limit.y;
        }

        TweenMax.to(option, 1, {
          y: y,
          ease: Power4.easeOut,
          onUpdate: () => {
            scrollbar.scrollTo(0, option.y, 0);
          },
        });
      });
    });
  };
  pagination();

  /*--------------------*/
  /* Mousewheel */
  /*--------------------*/
  const verticalScroll = (e) => {
    const delta = parseInt(e.deltaY * option.speed);
    let y = scrollbar.offset.y + delta;
    y = y < 0 ? 0 : y > scrollbar.limit.y ? scrollbar.limit.y : y;

    TweenMax.to(option, option.time, {
      y: y,
      onUpdate: () => {
        scrollbar.scrollTo(0, option.y, 0);
      },
    });
  };
  document.querySelector(".wrapper").addEventListener("mousewheel", (e) => {
    verticalScroll(e);
  });
});
</script>

<style scoped>
*,
*:before,
*:after {
  box-sizing: border-box;
}

body {
  height: 100vh;
  overflow: hidden;
  font-family: "PT Sans", sans-serif;
  color: #444;
}

#scrollbar {
  height: 100vh;
  width: 100%;
  background: #eee;
}

.wrapper {
  display: block; /* 수평에서 수직 레이아웃으로 변경 */
  position: relative;
  z-index: 1;
  counter-reset: item;
}

.item {
  position: relative;
  padding: 150px 80px;
  height: 100vh;
  display: flex;
  align-items: center;
  line-height: 1.7;
  user-select: none;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}
.background-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  position: absolute;
  top: 0;
  left: 0;
  z-index: -1;
}
</style>
