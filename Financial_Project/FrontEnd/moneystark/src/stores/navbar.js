// src/composables/navbar.js
import { ref, onMounted, onUnmounted } from 'vue'

export function useNavbar(imageSection) {
  const isNavbarHidden = ref(false)

  const handleScroll = () => {
    if (!imageSection) return

    const imageSectionBottom = imageSection.offsetTop + imageSection.offsetHeight
    const scrollPosition = window.scrollY

    // Navbar 숨김/표시 처리
    isNavbarHidden.value = scrollPosition > imageSectionBottom
  }

  onMounted(() => {
    window.addEventListener('scroll', handleScroll)
  })

  onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll)
  })

  return {
    isNavbarHidden
  }
}