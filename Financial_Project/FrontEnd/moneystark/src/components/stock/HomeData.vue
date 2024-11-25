<template>
  <div class="home-data">
    <h2>
      <i class="mdi mdi-home-city"></i>
      부동산 가격 데이터
    </h2>
    <div class="view-selector">
      <button :class="{ active: !showMap }" @click="showMap = false">
        <i class="mdi mdi-table"></i>
        테이블 보기
      </button>
      <button :class="{ active: showMap }" @click="showMap = true">
        <i class="mdi mdi-map"></i>
        지도 보기
      </button>
    </div>
    <div class="type-selector">
      <button v-for="(type, key) in houseTypes" :key="key" :class="{ active: selectedType === key }" @click="changeType(key)">
        <i class="mdi mdi-home"></i>
        {{ type.name }}
      </button>
    </div>

    <div v-if="!showMap">
      <div v-if="loading" class="loading">
        <i class="mdi mdi-loading mdi-spin"></i>
        데이터를 불러오는 중...
      </div>
      <div v-else-if="error" class="error">
        <i class="mdi mdi-alert-circle"></i>
        {{ error }}
      </div>
      <div v-else class="table-container">
        <div class="pagination-controls">
          <label for="itemsPerPage">
            <i class="mdi mdi-format-list-numbered"></i>
            페이지 당 항목 수
          </label>
          <select v-model="itemsPerPage" id="itemsPerPage" @change="handlePageSizeChange">
            <option value="10">10개씩 보기</option>
            <option value="20">20개씩 보기</option>
            <option value="50">50개씩 보기</option>
          </select>
          <!-- 검색 필터 추가 -->
          <div class="search-filter">
            <input v-model="searchQuery" type="text" placeholder="지역 검색" />
          </div>
        </div>
        <div v-if="nationalData" class="national-data">
          <h3>
            <i class="mdi mdi-earth"></i>
            전국 평균
          </h3>
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
          <button :disabled="currentPage === 1" @click="currentPage--" class="pagination-btn">
            <i class="mdi mdi-chevron-left"></i>
            이전
          </button>
          <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
          <button :disabled="currentPage === totalPages" @click="currentPage++" class="pagination-btn">
            다음
            <i class="mdi mdi-chevron-right"></i>
          </button>
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
      currentPage: 1,
      itemsPerPage: 10,
      searchQuery: "", // 검색어 추가
    };
  },
  computed: {
    filteredData() {
      return this.data.filter((item) => item.location.includes(this.searchQuery) && !item.location_full.includes("전국"));
    },
    sortedData() {
      return this.filteredData.sort((a, b) => b.price - a.price);
    },
    paginatedData() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + parseInt(this.itemsPerPage);
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
        this.currentPage = 1;
      } catch (error) {
        this.error = "데이터를 불러오는데 실패했습니다.";
        console.error("Error:", error);
      } finally {
        this.loading = false;
      }
    },
    formatPrice(price) {
      const billion = (price * 0.001).toFixed(2);
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
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
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
  display: flex;
  align-items: center;
  gap: 8px;
}

.view-selector button.active,
.type-selector button.active {
  background-color: #1890ff;
  border-color: #1890ff;
  color: #fff;
}

/* 검색 필터 스타일 */
.search-filter {
  display: flex;
  justify-content: flex-end;
  width: 70%;
}

.search-filter input {
  width: 300px;
  padding: 10px;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.search-filter input:focus {
  border-color: #1890ff;
  box-shadow: 0 0 8px rgba(24, 144, 255, 0.2);
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

th,
td {
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
  display: flex;
  align-items: center;
  gap: 10px;
}

.pagination-controls label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #666;
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

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-top: 20px;
}

.pagination-btn {
  padding: 8px 16px;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  background: #fff;
  color: #555;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 5px;
}

.pagination-btn:disabled {
  background: #f0f0f0;
  color: #ccc;
  cursor: not-allowed;
}

.page-info {
  font-size: 1rem;
  color: #555;
}

.loading,
.error {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  color: #1890ff;
  font-size: 1.2rem;
  margin-top: 20px;
}
</style>
