<template>
  <div class="home-data">
    <h2>부동산 가격 데이터</h2>
    <div class="view-selector">
      <button :class="{ active: !showMap }" @click="showMap = false">테이블 보기</button>
      <button :class="{ active: showMap }" @click="showMap = true">지도 보기</button>
    </div>
    <div class="type-selector">
      <button v-for="(type, key) in houseTypes" :key="key" :class="{ active: selectedType === key }" @click="changeType(key)">
        {{ type.name }}
      </button>
    </div>
    
    <div v-if="!showMap">
      <div v-if="loading">데이터를 불러오는 중...</div>
      <div v-else-if="error">{{ error }}</div>
      <div v-else class="table-container">
        <div class="pagination-controls">
          <select v-model="itemsPerPage" @change="handlePageSizeChange">
            <option value="10">10개씩 보기</option>
            <option value="20">20개씩 보기</option>
            <option value="50">50개씩 보기</option>
          </select>
        </div>
        <div v-if="nationalData" class="national-data">
          <h3>전국 평균</h3>
          <p>{{ nationalData.location_full }}: {{ formatPrice(nationalData.price) }}억원</p>
        </div>

        <table>
          <thead>
            <tr>
              <th>지역</th>
              <th>상세 위치</th>
              <th>가격 (억원)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in paginatedData" :key="item.location">
              <td>{{ item.location }}</td>
              <td>{{ item.location_full }}</td>
              <td>{{ formatPrice(item.price) }}억</td>
            </tr>
          </tbody>
        </table>

        <div class="pagination">
          <button :disabled="currentPage === 1" @click="currentPage--" class="pagination-btn">이전</button>
          <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
          <button :disabled="currentPage === totalPages" @click="currentPage++" class="pagination-btn">다음</button>
        </div>
      </div>
    </div>
    <korea-map v-if="showMap" :data="data" :selectedType="houseTypes[selectedType].name" v-show="!loading" />
  </div>
</template>

<script>
import axios from "axios";
import KoreaMap from "./KoreaMap.vue";

export default {
  components: {
    KoreaMap,
  },
  name: "HomeData",
  data() {
    return {
      houseTypes: {
        house: { name: "주택종합" },
        apartment: { name: "아파트" },
        row_house: { name: "연립/다세대" },
        single_house: { name: "단독주택" },
      },
      showMap: false,
      selectedType: "apartment",
      data: [],
      loading: false,
      error: null,
      nationalData: null,
      currentPage: 1, // pagination 관련 값들을 여기로 이동
      itemsPerPage: 10,
    };
  },
  computed: {
    sortedData() {
      return this.data.filter((item) => !item.location_full.includes("전국")).sort((a, b) => b.price - a.price);
    },
    paginatedData() {
      // template에서 sortedData 대신 paginatedData 사용
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + parseInt(this.itemsPerPage); // select의 value가 문자열일 수 있으므로 parseInt 추가
      return this.sortedData.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.sortedData.length / this.itemsPerPage);
    },
  },
  methods: {
    async fetchData() {
      try {
        this.loading = true;
        this.error = null;
        const response = await axios.get(`http://127.0.0.1:8000/moneys/home_data/?type=${this.selectedType}`);
        this.data = response.data.data;
        this.nationalData = this.data.find((item) => item.location_full.includes("전국"));
        this.currentPage = 1; // 데이터 새로 불러올 때 첫 페이지로 이동
      } catch (error) {
        this.error = "데이터를 불러오는데 실패했습니다.";
        console.error("Error:", error);
      } finally {
        this.loading = false;
      }
    },
    formatPrice(price) {
      const billion = (price * 0.0001).toFixed(2);
      return new Intl.NumberFormat("ko-KR").format(billion);
    },
    changeType(type) {
      this.selectedType = type;
      this.fetchData();
    },
    handlePageSizeChange() {
      this.currentPage = 1;
    },
  },
  mounted() {
    this.fetchData();
  },
};
</script>

<style scoped>
.home-data {
  max-width: 1200px;
  margin: 40px auto;
  padding: 20px;
  font-family: "Noto Sans KR", sans-serif;
}

h2 {
  color: #1890ff;
  text-align: center;
  margin-bottom: 30px;
  font-size: 1.8rem;
}

.view-selector,
.type-selector {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 30px;
}

.view-selector button,
.type-selector button {
  padding: 12px 24px;
  background-color: #fff;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  color: #555;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
}

.view-selector button.active,
.type-selector button.active {
  background-color: #1890ff;
  border-color: #1890ff;
  color: #fff;
}

.table-container {
  background: #fff;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.national-data {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
  border: 1px solid #e9ecef;
}

table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin-top: 20px;
}

th, td {
  padding: 15px;
  text-align: left;
  border-bottom: 1px solid #e9ecef;
}

th {
  background: #f8f9fa;
  font-weight: 600;
  color: #333;
}

tr:hover {
  background: #f0f7ff;
}

.pagination-controls {
  margin-bottom: 20px;
}

.pagination-controls select {
  padding: 8px 16px;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  background: #fff;
  color: #555;
  cursor: pointer;
  transition: all 0.3s ease;
}
</style>