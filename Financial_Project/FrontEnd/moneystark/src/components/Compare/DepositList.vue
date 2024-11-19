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
