<template>
  <div class="deposit-page">
    <h2>정기예금 상품 비교</h2>
    <div class="search-container">
      <div class="search-options">
        <div class="form-group">
          <label for="bank">은행 선택</label>
          <select v-model="selectedBank" id="bank" class="form-control">
            <option value="">전체 은행</option>
            <option v-for="bank in banks" :key="bank" :value="bank">{{ bank }}</option>
          </select>
        </div>
        <div class="form-group">
          <label for="period">예치 기간</label>
          <select v-model="selectedPeriod" id="period" class="form-control">
            <option value="">전체 기간</option>
            <option v-for="period in allPeriods" :key="period" :value="period">{{ period }}개월</option>
          </select>
        </div>
        <button @click="filterProducts" class="search-button">검색</button>
      </div>
    </div>

    <div class="content-container">
      <div v-if="!selectedDeposit" class="search-results">
        <table class="deposit-table">
          <thead>
            <tr>
              <th scope="col">금융회사 명</th>
              <th scope="col">금융 상품명</th>
              <th scope="col" @click="toggleSort('maxRate')" class="sortable">
                최고 금리
                <span class="sort-icon">
                  <span v-if="sortKey === 'maxRate'">
                    <span v-if="sortAscending">▲</span>
                    <span v-else>▼</span>
                  </span>
                </span>
              </th>
              <th scope="col">예치 기간</th>
              <th scope="col">상품 상세</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="deposit in paginatedProducts" :key="deposit.id">
              <td>{{ deposit.kor_co_nm }}</td>
              <td>{{ deposit.fin_prdt_nm }}</td>
              <td>{{ getMaxRate(deposit.options).toFixed(2) }}%</td>
              <td>{{ getAvailableTerms(deposit.options) }}</td>
              <td>
                <button @click="selectDeposit(deposit)" class="detail-button">자세히 보기</button>
              </td>
            </tr>
          </tbody>
        </table>
        <div class="pagination">
          <button @click="prevPage" :disabled="currentPage === 1">이전</button>
          <span>{{ currentPage }} / {{ totalPages }}</span>
          <button @click="nextPage" :disabled="currentPage === totalPages">다음</button>
        </div>
      </div>

      <div v-if="selectedDeposit" class="item-details">
        <DepositListItem :deposit="selectedDeposit" @back="selectedDeposit = null" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useProductStore } from '@/stores/product';
import DepositListItem from './DepositListItem.vue';

const productStore = useProductStore();
const selectedBank = ref('');
const selectedPeriod = ref('');
const filteredProducts = ref([]);
const selectedDeposit = ref(null);
const currentPage = ref(1);
const itemsPerPage = 10;

// 정렬 상태 관리 변수
const sortKey = ref('');
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
    return (
      (selectedBank.value === '' || product.kor_co_nm === selectedBank.value) &&
      (selectedPeriod.value === '' ||
        product.options.some((option) => option.save_trm === selectedPeriod.value))
    );
  });
  sortProducts(); // 필터링 후 정렬 적용
  currentPage.value = 1;
};

const sortProducts = () => {
  if (sortKey.value === 'maxRate') {
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
  return options.map((opt) => `${opt.save_trm}개월`).join(', ');
};

onMounted(async () => {
  await productStore.getDepositProduct();
  filteredProducts.value = productStore.depositProduct.slice();
  sortProducts(); // 초기 정렬 적용
});
</script>
<style scoped>
/* 전체 페이지 스타일 */
.deposit-page {
  max-width: 1200px;
  margin: 40px auto;
  padding: 20px;
  font-family: 'Noto Sans KR', sans-serif;
}

/* 제목 스타일 */
.deposit-page h2 {
  text-align: center;
  font-size: 2rem;
  color: #333;
  margin-bottom: 30px;
}

/* 검색 영역 스타일 */
.search-container {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 30px;
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
  font-size: 1rem;
  color: #555;
  margin-bottom: 8px;
}

.form-control {
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
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
}

.search-button:hover {
  background-color: #40a9ff;
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

.deposit-table tr:hover {
  background-color: #f1f1f1;
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
}

.detail-button:hover {
  background-color: #73d13d;
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
</style>
