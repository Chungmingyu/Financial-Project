<template>
  <div class="deposit-page">
    <h2>
      <i class="mdi mdi-bank"></i>
      정기예금 상품 비교
    </h2>
    <!-- 검색 영역을 selectedDeposit이 없을 때만 표시 -->
    <div v-if="!selectedDeposit" class="search-container">
      <div class="search-options">
        <div class="form-group">
          <label for="bank">
            <i class="mdi mdi-office-building"></i>
            은행 선택
          </label>
          <select v-model="selectedBank" id="bank" class="form-control">
            <option value="">전체 은행</option>
            <option v-for="bank in banks" :key="bank" :value="bank">{{ bank }}</option>
          </select>
        </div>
        <div class="form-group">
          <label for="period">
            <i class="mdi mdi-calendar-clock"></i>
            예치 기간
          </label>
          <select v-model="selectedPeriod" id="period" class="form-control">
            <option value="">전체 기간</option>
            <option v-for="period in allPeriods" :key="period" :value="period">{{ period }}개월</option>
          </select>
        </div>
        <button @click="filterProducts" class="search-button">
          <i class="mdi mdi-magnify"></i>
          검색
        </button>
      </div>
    </div>

    <div class="content-container">
      <div v-if="!selectedDeposit" class="search-results">
        <table class="deposit-table">
          <thead>
            <tr>
              <th scope="col">
                <i class="mdi mdi-bank"></i>
                금융회사
              </th>
              <th scope="col">
                <i class="mdi mdi-file-document"></i>
                상품명
              </th>
              <!-- 테이블 헤더 부분 수정 -->
              <th scope="col" @click="toggleSort('maxRate')" class="sortable rate-header">
                <div class="header-content">
                  <span>
                    <i class="mdi mdi-trending-up"></i>
                    최고 금리
                  </span>
                  <span class="sort-icon">
                    <i v-if="sortKey === 'maxRate'" :class="sortAscending ? 'mdi mdi-arrow-up' : 'mdi mdi-arrow-down'"></i>
                  </span>
                </div>
              </th>
              <th scope="col">
                <i class="mdi mdi-calendar"></i>
                예치 기간
              </th>
              <th scope="col">
                <i class="mdi mdi-information"></i>
                상세 정보
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="deposit in paginatedProducts" :key="deposit.id" class="table-row">
              <td>{{ deposit.kor_co_nm }}</td>
              <td>{{ deposit.fin_prdt_nm }}</td>
              <td class="highlight-rate">{{ getMaxRate(deposit.options).toFixed(2) }}%</td>
              <td>{{ getAvailableTerms(deposit.options) }}</td>
              <td>
                <button @click="selectDeposit(deposit)" class="detail-button">
                  <i class="mdi mdi-eye"></i>
                  자세히 보기
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <div class="pagination">
          <button @click="prevPage" :disabled="currentPage === 1">
            <i class="mdi mdi-chevron-left"></i>
            이전
          </button>
          <span>{{ currentPage }} / {{ totalPages }}</span>
          <button @click="nextPage" :disabled="currentPage === totalPages">
            다음
            <i class="mdi mdi-chevron-right"></i>
          </button>
        </div>
      </div>

      <div v-if="selectedDeposit" class="item-details">
        <DepositListItem :deposit="selectedDeposit" @back="selectedDeposit = null" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import { useProductStore } from "@/stores/product";
import DepositListItem from "./DepositListItem.vue";

const productStore = useProductStore();
const selectedBank = ref("");
const selectedPeriod = ref("");
const filteredProducts = ref([]);
const selectedDeposit = ref(null);
const currentPage = ref(1);
const itemsPerPage = 10;

// 정렬 상태 관리 변수
const sortKey = ref("");
const sortAscending = ref(true);

const banks = computed(() => {
  const bankSet = new Set(productStore.depositProduct.map((product) => product.kor_co_nm));
  return Array.from(bankSet).sort();
});

const allPeriods = computed(() => {
  const periodSet = new Set();
  productStore.depositProduct.forEach((product) => {
    product.options.forEach((option) => {
      periodSet.add(option.save_trm);
    });
  });
  return Array.from(periodSet).sort((a, b) => a - b);
});

const totalPages = computed(() => {
  return Math.ceil(filteredProducts.value.length / itemsPerPage);
});

const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return filteredProducts.value.slice(start, end);
});

const filterProducts = () => {
  filteredProducts.value = productStore.depositProduct.filter((product) => {
    return (selectedBank.value === "" || product.kor_co_nm === selectedBank.value) && (selectedPeriod.value === "" || product.options.some((option) => option.save_trm === selectedPeriod.value));
  });
  sortProducts(); // 필터링 후 정렬 적용
  currentPage.value = 1;
};

const sortProducts = () => {
  if (sortKey.value === "maxRate") {
    filteredProducts.value.sort((a, b) => {
      const rateA = getMaxRate(a.options);
      const rateB = getMaxRate(b.options);
      if (sortAscending.value) {
        return rateA - rateB;
      } else {
        return rateB - rateA;
      }
    });
  }
};

const toggleSort = (key) => {
  if (sortKey.value === key) {
    sortAscending.value = !sortAscending.value;
  } else {
    sortKey.value = key;
    sortAscending.value = true;
  }
};

watch([sortKey, sortAscending], () => {
  sortProducts();
});

const selectDeposit = (deposit) => {
  selectedDeposit.value = deposit;
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

const getMaxRate = (options) => {
  const rates = options.map((opt) => parseFloat(opt.intr_rate2 || opt.intr_rate));
  return Math.max(...rates);
};

const getAvailableTerms = (options) => {
  return options.map((opt) => `${opt.save_trm}개월`).join(", ");
};

onMounted(async () => {
  await productStore.getDepositProduct();
  filteredProducts.value = productStore.depositProduct.slice();
  sortProducts(); // 초기 정렬 적용
});
</script>
<style scoped>
:root {
  --primary-color: #1890ff;
  --primary-hover: #40a9ff;
  --success-color: #52c41a;
  --success-hover: #73d13d;
  --warning-color: #faad14;
  --text-primary: #333;
  --text-secondary: #555;
  --background-light: #f9f9f9;
  --border-radius: 8px;
  --box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
.btn {
  padding: 12px 24px;
  border: none;
  border-radius: var(--border-radius);
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: var(--primary-color);
  color: white;
}

.btn-primary:hover {
  background-color: var(--primary-hover);
}

.btn-success {
  background-color: var(--success-color);
  color: white;
}

.btn-success:hover {
  background-color: var(--success-hover);
}

.table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
  box-shadow: var(--box-shadow);
}

.table th,
.table td {
  padding: 15px;
  text-align: center;
  border-bottom: 1px solid #eee;
}

.table th {
  background-color: var(--background-light);
  font-weight: 500;
  color: var(--text-secondary);
}

.table tr:hover {
  background-color: #f5f5f5;
}

.container {
  max-width: 1200px;
  margin: 40px auto;
  padding: 20px;
}

.section {
  background-color: white;
  border-radius: var(--border-radius);
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: var(--box-shadow);
}
/* 전체 페이지 스타일 */
.deposit-page {
  max-width: 1200px;
  margin: 40px auto;
  padding: 20px;
  font-family: "Noto Sans KR", sans-serif;
}

/* 제목 스타일 */
.deposit-page h2 {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  color: #1890ff;
}

.deposit-page h2 i {
  font-size: 2rem;
}

/* 검색 영역 스타일 */
.search-container {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 30px;
  animation: fadeInDown 0.3s ease-out;
}

.search-options {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  flex-wrap: wrap;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 15px;
  flex: 1;
  min-width: 200px;
  margin-right: 20px;
}

.form-group label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #666;
}

.form-group label i {
  color: #1890ff;
}

.form-control {
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding-left: 30px;
  background-position: 8px center;
  background-repeat: no-repeat;
  background-size: 16px;
  transition: all 0.3s ease;
}

.form-control:focus {
  border-color: #1890ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
}

.search-button {
  padding: 12px 30px;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-bottom: 15px;
  align-self: flex-end;
}

.search-button:hover {
  background-color: #40a9ff;
}

.search-button i {
  font-size: 1.2rem;
}

/* 컨텐츠 영역 스타일 */
.content-container {
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
}

/* 테이블 스타일 */
.deposit-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.deposit-table th,
.deposit-table td {
  padding: 15px;
  text-align: center;
  border-bottom: 1px solid #eee;
}

.deposit-table th {
  background-color: #fafafa;
  font-weight: bold;
  color: #555;
}

.deposit-table th i {
  margin-right: 5px;
  color: #1890ff;
}

.deposit-table tr:hover {
  background-color: #f1f1f1;
}

.table-row {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.table-row:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background-color: #f8f9ff !important;
}

.highlight-rate {
  color: #ff4d4f;
  font-weight: bold;
}

.detail-button {
  padding: 8px 15px;
  background-color: #52c41a;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  margin: 0 auto;
}

.detail-button:hover {
  background-color: #73d13d;
}

.detail-button i {
  font-size: 1.1rem;
}

/* 페이지네이션 스타일 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
}

.pagination button {
  padding: 8px 15px;
  margin: 0 5px;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.pagination button:hover:not(:disabled) {
  background-color: #40a9ff;
}

.pagination span {
  margin: 0 10px;
  font-size: 1rem;
  color: #555;
}

/* 애니메이션 효과 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.search-results {
  animation: fadeInUp 0.5s ease-out;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .search-options {
    flex-direction: column;
    align-items: stretch;
  }

  .form-group {
    margin-right: 0;
    margin-bottom: 20px;
  }

  .search-button {
    width: 100%;
    padding: 12px;
  }

  .deposit-table th i {
    display: none;
  }

  .form-group label i {
    font-size: 1.2rem;
  }

  .search-button {
    padding: 15px;
  }
}
/* 컬럼 헤더에 커서 및 강조 효과 추가 */
.sortable {
  cursor: pointer;
  user-select: none;
}

.sortable:hover {
  background-color: #f5f5f5;
}

/* 정렬 아이콘 스타일 */
.sort-icon {
  margin-left: 5px;
  font-size: 0.8rem;
}
/* CSS 수정/추가 */
.deposit-table th {
  background-color: #fafafa;
  font-weight: bold;
  color: #555;
  min-width: 100px; /* 최소 너비 설정 */
  padding: 15px 10px;
}

.rate-header {
  min-width: 140px; /* 정렬 헤더의 최소 너비 증가 */
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  white-space: nowrap;
}

.sort-icon {
  display: inline-flex;
  width: 20px; /* 고정 너비 */
  justify-content: center;
  align-items: center;
}

/* 반응형 대응 */
@media (max-width: 768px) {
  .deposit-table th {
    padding: 12px 8px;
    font-size: 0.9rem;
  }

  .rate-header {
    min-width: 120px;
  }

  .header-content {
    gap: 4px;
  }

  .sort-icon {
    width: 16px;
  }
}

@media (max-width: 576px) {
  .header-content {
    flex-direction: column;
    gap: 2px;
  }

  .sort-icon {
    height: 16px;
  }
}
</style>
