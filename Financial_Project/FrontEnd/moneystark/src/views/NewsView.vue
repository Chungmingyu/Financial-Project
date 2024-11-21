<template>
  <div class="news-container">
    <div class="search-bar">
      <input :value="localQuery" @input="updateQuery" placeholder="검색어 입력" />
      <button @click="fetchNews">검색</button>
    </div>
    <ul class="news-list">
      <li v-for="(news, index) in newsList" :key="index" class="news-item">
        <a :href="news.link" target="_blank" class="news-link">
          <img :src="news.image" alt="뉴스 이미지" v-if="news.image" class="news-image" />
          <div class="news-content">
            <h3 class="news-title">{{ news.title }}</h3>
            <p class="news-snippet">{{ news.snippet }}</p>
          </div>
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: {
    query: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      localQuery: this.query,
      newsList: [],
    };
  },
  watch: {
    query(newQuery) {
      this.localQuery = newQuery;
      this.fetchNews();
    },
  },
  mounted() {
    this.fetchNews();
  },
  methods: {
    updateQuery(event) {
      this.localQuery = event.target.value;
      this.$emit("update:query", this.localQuery);
    },
    async fetchNews() {
      if (!this.localQuery) return;
      try {
        const response = await fetch(`http://127.0.0.1:8000/news/?q=${encodeURIComponent(this.localQuery)}`);
        const data = await response.json();
        this.newsList = data.news.map((item) => ({
          title: item.title,
          link: item.link,
          snippet: item.snippet,
          image: item.pagemap?.cse_image?.[0]?.src || null,
        }));
      } catch (error) {
        console.error("뉴스를 가져오는 중 오류 발생:", error);
      }
    },
  },
};
</script>

<style>
.news-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.search-bar {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

input {
  width: calc(100% - 100px);
  padding: 10px;
  margin-right: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 10px 20px;
  border: 1px solid #ccc;
  background-color: #ffbf00;
  color: black;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #e6ac00;
}

.news-list {
  list-style: none;
  padding: 0;
  max-height: 600px;
  overflow-y: auto;
  margin-top: 20px; /* 검색창과 결과 목록 사이에 간격 추가 */
}

.news-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 20px;
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
}

.news-link {
  display: flex;
  text-decoration: none;
  color: inherit;
}

.news-image {
  width: 150px;
  height: 100px;
  object-fit: cover;
  margin-right: 20px;
}

.news-content {
  flex: 1;
}

.news-title {
  margin: 0 0 10px;
  font-size: 18px;
}

.news-snippet {
  margin: 0;
  color: #555;
}
</style>
