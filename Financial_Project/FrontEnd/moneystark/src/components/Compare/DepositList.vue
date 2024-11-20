<template>
  <div>
    <h2>정기예금 정보</h2>
    <div class="container">
      <div v-if="!selectedDeposit" class="search-container">
        <h3>예금 검색</h3>
        <div class="search-options">
          <label for="bank">은행:</label>
          <select v-model="selectedBank" id="bank" class="form-control">
            <option value="">모든 은행</option>
            <option v-for="bank in banks" :key="bank" :value="bank">{{ bank }}</option>
          </select>

          <label for="period">예치 기간:</label>
          <select v-model="selectedPeriod" id="period" class="form-control">
            <option value="">모든 기간</option>
            <option v-for="period in allPeriods" :key="period" :value="period">{{ period }}개월</option>
          </select>

          <button @click="filterProducts" class="btn btn-primary">검색</button>
        </div>
      </div>

      <div class="content-container">
        <div v-if="!selectedDeposit" class="search-results">
          <table class="table table-striped">
            <thead>
              <tr>
                <th scope="col">공시 제출월</th>
                <th scope="col">금융회사 명</th>
                <th scope="col">금융 상품명</th>
                <th scope="col">
                  1개월
                  <span class="sort-arrows" @click="sortByTerm(1)">
                    <span :class="{ active: sortTerm === 1 && sortAscending }">&uarr;</span>
                    <span :class="{ active: sortTerm === 1 && !sortAscending }">&darr;</span>
                  </span>
                </th>
                <th scope="col">
                  3개월
                  <span class="sort-arrows" @click="sortByTerm(3)">
                    <span :class="{ active: sortTerm === 3 && sortAscending }">&uarr;</span>
                    <span :class="{ active: sortTerm === 3 && !sortAscending }">&darr;</span>
                  </span>
                </th>
                <th scope="col">
                  6개월
                  <span class="sort-arrows" @click="sortByTerm(6)">
                    <span :class="{ active: sortTerm === 6 && sortAscending }">&uarr;</span>
                    <span :class="{ active: sortTerm === 6 && !sortAscending }">&darr;</span>
                  </span>
                </th>
                <th scope="col">
                  12개월
                  <span class="sort-arrows" @click="sortByTerm(12)">
                    <span :class="{ active: sortTerm === 12 && sortAscending }">&uarr;</span>
                    <span :class="{ active: sortTerm === 12 && !sortAscending }">&darr;</span>
                  </span>
                </th>
                <th scope="col">
                  24개월
                  <span class="sort-arrows" @click="sortByTerm(24)">
                    <span :class="{ active: sortTerm === 24 && sortAscending }">&uarr;</span>
                    <span :class="{ active: sortTerm === 24 && !sortAscending }">&darr;</span>
                  </span>
                </th>
                <th scope="col">
                  36개월
                  <span class="sort-arrows" @click="sortByTerm(36)">
                    <span :class="{ active: sortTerm === 36 && sortAscending }">&uarr;</span>
                    <span :class="{ active: sortTerm === 36 && !sortAscending }">&darr;</span>
                  </span>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="deposit in paginatedProducts" :key="deposit.id" @click="selectDeposit(deposit)">
                <td>{{ deposit.dcls_month.slice(0, 4) }}년 {{ deposit.dcls_month.slice(4, 6) }}월</td>
                <td>{{ deposit.kor_co_nm }}</td>
                <td>{{ deposit.fin_prdt_nm }}</td>
                <td>{{ getRate(deposit.options, 1) }}</td>
                <td>{{ getRate(deposit.options, 3) }}</td>
                <td>{{ getRate(deposit.options, 6) }}</td>
                <td>{{ getRate(deposit.options, 12) }}</td>
                <td>{{ getRate(deposit.options, 24) }}</td>
                <td>{{ getRate(deposit.options, 36) }}</td>
              </tr>
            </tbody>
          </table>
          <div class="pagination">
            <button @click="prevPage" :disabled="currentPage === 1">이전</button>
            <span>{{ currentPage }} / {{ totalPages }}</span>
            <button @click="nextPage" :disabled="currentPage === totalPages">다음</button>
          </div>
        </div>

        <div v-if="selectedDeposit" class="item-details full-screen">
          <DepositListItem :deposit="selectedDeposit" @back="selectedDeposit = null" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useProductStore } from "@/stores/product";
import DepositListItem from "./DepositListItem.vue";

const productStore = useProductStore();
const selectedBank = ref("");
const selectedPeriod = ref("");
const filteredProducts = ref([]);
const selectedDeposit = ref(null);
const currentPage = ref(1);
const itemsPerPage = 10;
const sortAscending = ref(true);
const sortTerm = ref(null);

const banks = computed(() => {
  const bankSet = new Set(productStore.depositProduct.map((product) => product.kor_co_nm));
  return Array.from(bankSet);
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
  currentPage.value = 1; // 검색 시 첫 페이지로 이동
  if (selectedPeriod.value) {
    sortByTerm(selectedPeriod.value, true); // 검색 시 내림차순 정렬
  }
};

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

const getRate = (options, term) => {
  const option = options.find((opt) => opt.save_trm === term);
  return option ? option.intr_rate2 || option.intr_rate : "-";
};

const sortByTerm = (term, descending = false) => {
  if (sortTerm.value === term && !descending) {
    sortAscending.value = !sortAscending.value;
  } else {
    sortAscending.value = true;
  }
  sortTerm.value = term;
  filteredProducts.value.sort((a, b) => {
    const rateA = getRate(a.options, term);
    const rateB = getRate(b.options, term);
    if (rateA === "-") return 1;
    if (rateB === "-") return -1;
    return sortAscending.value ? rateA - rateB : rateB - rateA;
  });
  if (descending) {
    filteredProducts.value.reverse();
  }
};

onMounted(async () => {
  await productStore.getDepositProduct();
  filteredProducts.value = productStore.depositProduct;
});
</script>
<style scoped>
h2 {
  color: #333;
  text-align: center;
  margin-bottom: 20px;
  font-family: "Arial", sans-serif;
}

.container {
  display: flex;
  height: 100vh; /* 전체 높이를 차지하도록 설정 */
  padding: 20px;
  background-color: #f4f4f9;
}

.search-container {
  flex: 0.7; /* 검색 영역을 더 줄임 */
  margin-right: 20px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  background-color: #fff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.search-options {
  display: flex;
  flex-direction: column;
}

.search-options label {
  margin-bottom: 5px;
  font-weight: bold;
  color: #555;
}

.search-options select {
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 14px;
}

.search-options button {
  padding: 10px 15px;
  background-color: #333;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
  font-size: 14px;
}

.search-options button:hover {
  background-color: #555;
}

.content-container {
  flex: 3.3; /* 리스트 영역을 더 넓힘 */
  display: flex;
  flex-direction: column;
  background-color: #fff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  position: relative; /* 추가 */
}

.search-results,
.item-details {
  flex: 1;
  overflow-y: auto; /* 내용이 넘칠 경우 스크롤바 표시 */
}

.table {
  width: 100%;
  margin-top: 20px;
  border-collapse: collapse;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  overflow: hidden;
}

.table th,
.table td {
  text-align: center;
  padding: 15px;
  border: 1px solid #ddd;
  font-size: 14px;
}

.table th:first-child,
.table td:first-child {
  width: 120px; /* 첫 번째 컬럼의 너비를 늘림 */
}

.table th {
  background-color: #333;
  color: white;
  white-space: nowrap;
}

.table tbody tr {
  cursor: pointer;
  transition: background-color 0.3s;
}

.table tbody tr:hover {
  background-color: #f1f1f1;
}

.sort-arrows {
  display: inline-block;
  cursor: pointer;
  font-size: 12px;
  margin-left: 5px;
}

.sort-arrows span.active {
  color: #ff6347;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.pagination button {
  padding: 10px 15px;
  margin: 0 5px;
  background-color: #333;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.pagination button:hover:not(:disabled) {
  background-color: #555;
}

.pagination span {
  margin: 0 10px;
}

.full-screen {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: white;
  z-index: 1000;
  overflow-y: auto;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 12px;
}
</style>
<!-- 
<style scoped>
/* 메인 컨테이너 스타일링 */
.container {
  display: flex;
  min-height: 100vh;
  padding: 2rem;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  gap: 2rem;
}

/* 헤더 스타일링 */
h2 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2c3e50;
  text-align: center;
  margin: 2rem 0;
  text-transform: uppercase;
  letter-spacing: 2px;
}

/* 검색 섹션 스타일링 */
.search-container {
  flex: 0.7;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.18);
}

.search-container h3 {
  color: #2c3e50;
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #7700ff;
  padding-bottom: 0.5rem;
}

/* 검색 옵션 스타일링 */
.search-options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.search-options label {
  color: #34495e;
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 0.3rem;
}

.search-options select {
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  background: white;
}

.search-options select:focus {
  border-color: #7700ff;
  outline: none;
  box-shadow: 0 0 0 3px rgba(119, 0, 255, 0.1);
}

.search-options button {
  margin-top: 1rem;
  padding: 12px;
  background: #7700ff;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.search-options button:hover {
  background: #6600cc;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(119, 0, 255, 0.2);
}

/* 테이블 스타일링 */
.table {
  width: 100%;
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
  border: none;
}

.table th {
  background: #7700ff;
  color: white;
  padding: 1rem;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.85rem;
  letter-spacing: 1px;
}

.table td {
  padding: 1rem;
  color: #2c3e50;
  font-size: 0.9rem;
  border: 1px solid #f0f0f0;
}

.table tbody tr {
  transition: all 0.3s ease;
}

.table tbody tr:hover {
  background: rgba(119, 0, 255, 0.05);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

/* 정렬 화살표 스타일링 */
.sort-arrows {
  margin-left: 0.5rem;
  display: inline-flex;
  flex-direction: column;
  gap: 2px;
}

.sort-arrows span {
  font-size: 0.8rem;
  opacity: 0.5;
  transition: all 0.3s ease;
}

.sort-arrows span.active {
  color: white;
  opacity: 1;
  transform: scale(1.2);
}

/* 페이지네이션 스타일링 */
.pagination {
  margin-top: 2rem;
  display: flex;
  gap: 1rem;
  align-items: center;
  justify-content: center;
}

.pagination button {
  padding: 0.8rem 1.5rem;
  background: #7700ff;
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.pagination button:hover:not(:disabled) {
  background: #6600cc;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(119, 0, 255, 0.2);
}

.pagination button:disabled {
  background: #e0e0e0;
  cursor: not-allowed;
}

.pagination span {
  font-weight: 600;
  color: #2c3e50;
}

/* 상세 정보 모달 스타일링 */
.full-screen {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 2rem;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 반응형 디자인 */
@media (max-width: 1200px) {
  .container {
    flex-direction: column;
  }

  .search-container {
    flex: none;
  }
}

@media (max-width: 768px) {
  .table {
    font-size: 0.8rem;
  }

  .search-container {
    padding: 1rem;
  }
}
</style> -->
