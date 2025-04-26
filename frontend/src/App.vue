<template>
  <div class="min-h-screen flex flex-col custom-gradient">
    <!-- Header với Typography cách điệu -->
    <header class="flex-none p-4">
      <div class="max-w-7xl mx-auto text-center flex flex-col items-center">
        <h1 class="header-text montserrat-800 text-7xl text-white">
          NephroScan
        </h1>
        <p class="p-3 text-white montserrat-400 text-xl">Công cụ hỗ trợ phát hiện sỏi thận</p>

        
        <div class="video-container relative mt-12 w-full max-w-4xl">
          <div class="video-glow"></div>
          <iframe width="104%" height="500" src="https://www.youtube.com/embed/scU84FkiTKc" title="YouTube video player"
          frameborder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen class="relative z-10 rounded-2xl shadow-2xl"></iframe>
        </div>
        <!-- Nút Try Now với glassmorphism -->
        <button @click="scrollToMain"
          class="try-now-button mt-8 px-10 py-3 rounded-full text-white font-medium montserrat-400 transition-all duration-300 text-lg">
          Try Now
        </button>
      </div>
    </header>

    <!-- Nội dung chính -->
    <main class="flex-grow overflow-hidden" ref="mainContent">
      <div class="max-w-7xl mx-auto h-full">
        <ImageProcessingApp />
      </div>
      <!-- Các nút xã hội -->
      <div class="max-w-7xl mx-auto flex justify-center space-x-4 mt-8 p-4">
        <a href="https://github.com/p4wndev" target="_blank"
          class="social-button bg-white/10 hover:bg-white/20 rounded-full px-4 py-2 transition-all duration-300 flex items-center space-x-2">
          <i class="fab fa-github text-white text-xl"></i>
          <span class="text-white text-sm">@p4wndev</span>
        </a>
        <a href="https://www.facebook.com/tuitenphuan" target="_blank"
          class="social-button bg-white/10 hover:bg-white/20 rounded-full px-4 py-2 transition-all duration-300 flex items-center space-x-2">
          <i class="fab fa-facebook text-white text-xl"></i>
          <span class="text-white text-sm">@tuitenphuan</span>
        </a>
        <a href="https://www.linkedin.com/in/thaiphuan/" target="_blank"
          class="social-button bg-white/10 hover:bg-white/20 rounded-full px-4 py-2 transition-all duration-300 flex items-center space-x-2">
          <i class="fab fa-linkedin text-white text-xl"></i>
          <span class="text-white text-sm">@thaiphuan</span>
        </a>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import ImageProcessingApp from "./components/ImageProcessingApp.vue";

const mainContent = ref(null);

const scrollToMain = () => {
  mainContent.value?.scrollIntoView({ behavior: 'smooth' });
};
</script>

<style scoped>
.gruppo-regular {
  font-family: "Gruppo", sans-serif;
  font-weight: 400;
  font-style: normal;
}

.fugaz-one-regular {
  font-family: "Fugaz One", sans-serif;
  font-weight: 400;
  font-style: normal;
}

.montserrat-400 {
  font-family: "Montserrat", sans-serif;
  font-optical-sizing: auto;
  font-weight: 200;
  font-style: normal;
}

.montserrat-800 {
  font-family: "Montserrat", sans-serif;
  font-optical-sizing: auto;
  font-weight: 800;
  font-style: normal;
}

.header-text {
  position: relative;
  display: inline-block;
  letter-spacing: 0em;
  transition: all 0.3s ease;
}

/* Tùy chỉnh nút xã hội */
.social-button {
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(5px);
}

.social-button:hover {
  transform: scale(1.05);
}

.video-container {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
  position: relative;
}

.video-glow {
  position: absolute;
  top: -10px;
  left: -10px;
  right: -10px;
  bottom: -10px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.4) 0%, rgba(255, 255, 255, 0.4) 50%, rgba(255, 255, 255, 0.4) 100%);
  border-radius: 30px;
  filter: blur(25px);
  z-index: 1;
  animation: pulse 3s infinite alternate;
}

@keyframes pulse {
  0% {
    opacity: 0.6;
    box-shadow: 0 0 20px 10px rgba(174, 172, 255, 0.5);
  }

  100% {
    opacity: 0.9;
    box-shadow: 0 0 40px 20px rgba(242, 228, 255, 0.7);
  }
}

iframe {
  border: 2px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  aspect-ratio: 16 / 9;
}

iframe:hover {
  transform: scale(1.01);
}

.try-now-button {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.try-now-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg,
      transparent,
      rgba(255, 255, 255, 0.2),
      transparent);
  transition: 0.5s;
}

.try-now-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.3);
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
}

.try-now-button:hover::before {
  left: 100%;
}

/* Cân chỉnh layout */
header {
  padding-top: 2rem;
  padding-bottom: 4rem;
}

@media (max-width: 768px) {
  .header-text {
    font-size: 3.5rem;
  }

  .video-container {
    max-width: 95%;
  }

  iframe {
    height: auto;
  }
}
</style>
