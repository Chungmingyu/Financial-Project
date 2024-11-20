<template>
  <div class="container">
    <!-- 상단 섹션 -->
    <div class="top-section">
      <div class="header">
        <button @click="$emit('back')" class="back-button">뒤로가기</button>
        <!-- 은행 로고를 조건에 맞게 표시 -->
        <img v-if="currentBank" :src="currentBank.logo" class="bank-icon" />
      </div>
      <h2>{{ deposit.kor_co_nm }} - {{ deposit.fin_prdt_nm }}</h2>
      <div class="highest-rate">
        <span>최고 금리: {{ highestRate }}% ({{ highestRateTerm }}개월)</span>
      </div>
      <div class="button-group">
        <button v-if="isLoggedIn" @click="joinProduct(deposit.id, depositAmount)" class="join-button">가입하기</button>
        <button @click="goToOfficialSite" class="official-site-button">공식 홈에서 알아보기</button>
      </div>
    </div>

    <!-- 하단 섹션 -->
    <div class="bottom-section">
      <div class="deposit-info">
        <h3>상품 안내</h3>
        <hr />
        <div class="info-item">
          <span class="label">가입 방법</span>
          <span class="value">{{ deposit.join_way }}</span>
        </div>
        <div class="info-item">
          <span class="label">우대조건</span>
          <span class="value">{{ deposit.spcl_cnd }}</span>
        </div>
        <div class="info-item">
          <span class="label">가입제한</span>
          <span class="value">{{ deposit.join_deny }}</span>
        </div>
        <div class="info-item">
          <span class="label">가입대상</span>
          <span class="value">{{ deposit.join_member }}</span>
        </div>
        <div class="info-item">
          <span class="label">기타 유의사항</span>
          <span class="value">{{ deposit.etc_note }}</span>
        </div>
        <div class="info-item">
          <span class="label">최고한도</span>
          <span class="value">{{ deposit.max_limit }}</span>
        </div>
      </div>

      <!-- 금리 안내 섹션 -->
      <div class="rate-info">
        <h3>금리 안내</h3>
        <p>12개월 만기 시 받을 이자</p>
        <label for="depositAmount">예치금액 (원):</label>
        <input type="number" id="depositAmount" v-model.number="depositAmount" @input="calculateInterest" />
        <p>예치금액: {{ (depositAmount / 10000).toLocaleString() }}만원</p>
        <div class="rate-buttons">
          <button :class="{ selected: selectedRate === highestRate }" @click="selectRate(highestRate)">최고 금리: {{ highestRate }}%</button>
          <button :class="{ selected: selectedRate === basicRate }" @click="selectRate(basicRate)">기본 금리: {{ basicRate }}%</button>
        </div>
        <div v-if="selectedRate !== null">
          <p>원금: {{ depositAmount.toLocaleString() }}원</p>
          <p>이자: {{ calculatedInterest.toLocaleString() }}원</p>
          <p>총 합: {{ (depositAmount + calculatedInterest).toLocaleString() }}원</p>
          <small>유의 사항: 세전</small>
        </div>
      </div>

      <!-- 금리 정보 테이블 -->
      <table class="table table-striped">
        <thead>
          <tr>
            <th scope="col">개월 수</th>
            <th scope="col">금리 유형</th>
            <th scope="col">금리 유형명</th>
            <th scope="col">금리</th>
            <th scope="col">최고 우대금리</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="option in deposit.options" :key="option.save_trm">
            <td>{{ option.save_trm }}개월</td>
            <td>{{ option.intr_rate_type }}</td>
            <td>{{ option.intr_rate_type_nm }}</td>
            <td>{{ option.intr_rate }}%</td>
            <td>{{ option.intr_rate2 }}%</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
// import { useUserStore } from "@/stores/user";
import { useDepositStore } from "@/stores/deposit";

const store = useDepositStore();
const props = defineProps({
  deposit: Object,
});

const isLoggedIn = ref(true); // 로그인 상태를 나타내는 변수 (예시로 true로 설정)
const depositAmount = ref(10000000); // 기본값 1000만원
const calculatedInterest = ref(null);
const selectedRate = ref(null);

const banks = ref([
  { name: "우리은행", url: "https://www.wooribank.com", logo: "https://simg.wooribank.com/img/intro/header/h1_01.png" },
  { name: "한국스탠다드차타드은행", url: "https://www.standardchartered.co.kr", logo: "https://www.standardchartered.co.kr/np/assets/images/kr/base/chb_log_reb.png" },
  { name: "아이엠뱅크", url: "https://www.imbank.co.kr/dgb_ebz_main.jsp", logo: "https://www.imbank.co.kr/img/common/main/ebz_top_dgb_logo_up.png?v=20240607" },
  { name: "부산은행", url: "https://www.busanbank.co.kr", logo: "https://blog.kakaocdn.net/dn/18TFu/btqyWKDIInm/GfE8079nzAF9txBlV71XS0/img.jpg" },
  { name: "광주은행", url: "https://www.kjbank.com", logo: "https://imgs.kjbank.com/resource/img/common/logo.png" },
  { name: "제주은행", url: "https://www.jejubank.co.kr", logo: "https://i.namu.wiki/i/DLhrLR38bUexuN_K8jiwwCqAo5gi2nEc7NmDI_MabOpop-ZWaI0G3KYRmjqyf8-7Crc0rv047buDbEChYyFqcQ.svg" },
  { name: "전북은행", url: "https://www.jbbank.co.kr/", logo: "https://www.jbbank.co.kr/img/common/renew-logo.png" },
  { name: "경남은행", url: "https://www.knbank.com", logo: "https://i.namu.wiki/i/dw9S4Oh4zaH3jLwxF8JixDMrQ36XQAJOTBMu0C4sLZ6f6NERx8dnsb5_sCY0DOHF4SuuNOJ7lLe4H1DfNyZjsQ.svg" },
  { name: "중소기업은행", url: "https://www.ibk.co.kr", logo: "https://www.ibk.co.kr/img/navigation/h1_logo_sub.gif" },
  { name: "한국산업은행", url: "https://www.kdb.co.kr", logo: "https://blog.kakaocdn.net/dn/SMJ1N/btqDjHIMQ0r/jAKsKJ2lT2XhGiEIsvZGN0/img.jpg" },
  { name: "국민은행", url: "https://www.kbstar.com", logo: "https://blog.kakaocdn.net/dn/bYyqeR/btqwFAWAKWf/wXPLrundPBKPrhtXgr0Iv1/img.jpg" },
  { name: "신한은행", url: "https://www.shinhan.com", logo: "https://i.namu.wiki/i/Etmt-wojOBWr5gVcPR0qrTxuej558yfzzyYr0xXYSxljpLuEdPWGSPi-aPdJHQrpZY2o7zvuUMb4PE6PvFjQ3Q.svg" },
  { name: "농협은행주식회사", url: "https://www.nonghyup.com", logo: "https://blog.kakaocdn.net/dn/bDOvRh/btqyXx4zjvs/gb3v21tHkeCYrozbCH0AYk/img.jpg" },
  { name: "하나은행", url: "https://www.kebhana.com", logo: "https://image.kebhana.com/cont/common/img/newmain2021/logo.png" },
  { name: "주식회사 케이뱅크", url: "https://www.kbanknow.com", logo: "https://www.kbanknow.com/resource/img/reform/layout/logo_kbank.png" },
  { name: "수협은행", url: "https://suhyup-bank.com", logo: "https://suhyup-bank.com/images/sub_new_main/img_logo.png" },
  { name: "한국씨티은행", url: "https://www.citibank.co.kr", logo: "https://i.namu.wiki/i/MejG2B28te9lfxBlpdWqCguVOnCa6zvyxJrf2u4KamJ7l8lXOG3rCMUyURui3PZhNbcH4aA6CKQK0JMbRjb8kQ.svg" },
  { name: "주식회사 카카오뱅크", url: "https://www.kakaobank.com", logo: "https://i.namu.wiki/i/tcO6LsmBe-rB-laaABweXNy9TaTU1fruiJaYVH39cCCZzg054tDwfbSmzsOvDU_zVZCJZzPS_YRe7vdgED3xQA.svg" },
  { name: "토스뱅크 주식회사", url: "https://www.tossbank.com", logo: "https://static.toss.im/icons/png/4x/logo-bank-blue.png" },
]);

const highestRate = Math.max(...props.deposit.options.map((option) => option.intr_rate2));
const highestRateTerm = props.deposit.options.find((option) => option.intr_rate2 === highestRate).save_trm;
const basicRate = props.deposit.options.find((option) => option.save_trm === 12).intr_rate;

const currentBank = computed(() => {
  return banks.value.find((bank) => bank.name === props.deposit.kor_co_nm);
});

const goToOfficialSite = () => {
  if (currentBank.value) {
    window.open(currentBank.value.url, "_blank");
  }
};

const joinProduct = async (productData, depositAmount) => {
  // 가입한 상품 목록에 상품 ID 추가 로직
  await store.addDeposit(productData, depositAmount);

  if (store.error) {
    alert(store.error);
  } else {
    console.log(`상품 ID ${props.deposit.id}가 가입한 상품 목록에 추가되었습니다.`);
  }
};

const calculateInterest = () => {
  const interest = (depositAmount.value * selectedRate.value * 12) / 1200;
  calculatedInterest.value = interest;
};

const selectRate = (rate) => {
  selectedRate.value = rate;
  calculateInterest();
};

onMounted(() => {
  selectedRate.value = highestRate;
  calculateInterest();
});
</script>
<style scoped>
/* 전체 컨테이너 */
.container {
  width: 90%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px;
  border: 1px solid #ddd;
  border-radius: 12px;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column; /* 수직 방향 정렬 */
  gap: 40px; /* 섹션 간 간격 */
  min-height: 1800px; /* 최소 높이 설정 */
}

/* 상단 섹션 */
.top-section {
  text-align: center; /* 중앙 정렬 */
  padding: 20px;
  border-bottom: 2px solid #ddd; /* 하단에 경계선 추가 */
}

.header {
  margin-bottom: 20px;
  display: flex; /* flex 레이아웃 사용 */
  justify-content: space-between; /* 양쪽 끝으로 정렬 */
  align-items: center; /* 수직 중앙 정렬 */
}

.back-button {
  background-color: #000; /* 검은색 배경 */
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  cursor: pointer;
  font-size: 16px;
}

.back-button:hover {
  background-color: #333;
}
.bank-icon {
  width: 100px;
  height: auto;
  margin-left: 20px;
}

h2 {
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
  font-weight: bolder;
}

.highest-rate {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 20px;
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.join-button {
  width: 220px;
  display: inline-block;
  margin: 20px;
  padding: 12px 24px;
  background-color: #000; /* 파란색 배경 */
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.join-button:hover {
  background-color: #333;
}

.official-site-button {
  width: 220px;
  display: inline-block;
  margin: 20px;
  padding: 12px 24px;
  background-color: #000; /* 검은색 배경 */
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.official-site-button:hover {
  background-color: #333;
}

/* 하단 섹션 */
.bottom-section {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 12px;
}

.deposit-info {
  margin-bottom: 40px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 12px 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #fff;
  margin-bottom: 10px;
}

.label {
  font-weight: bold;
  color: #333;
  margin-right: 20px; /* label과 value 사이에 여백 추가 */
}

.value {
  color: #555;
  flex: 1; /* value가 남은 공간을 차지하도록 설정 */
  text-align: right; /* value를 오른쪽 정렬 */
}

.table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
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

.table th {
  background-color: #ffbf00; /* 노란색 배경 */
  color: white;
}

.table td {
  background-color: #fffbe6; /* 연한 노란색 배경 */
}

.table tr:first-child th:first-child {
  border-top-left-radius: 12px;
}

.table tr:first-child th:last-child {
  border-top-right-radius: 12px;
}

.table tr:last-child td:first-child {
  border-bottom-left-radius: 12px;
}

.table tr:last-child td:last-child {
  border-bottom-right-radius: 12px;
}

/* 금리 안내 섹션 */
.rate-info {
  margin-top: 40px;
  margin-bottom: 40px;
  padding: 20px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.rate-buttons {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 20px;
}

.rate-buttons button {
  padding: 10px 20px;
  background: linear-gradient(145deg, #ffbf00, #ffd700);
  color: black;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 6px 8px rgba(0, 0, 0, 0.1);
  transition: background 0.3s, transform 0.3s, box-shadow 0.3s;
  position: relative;
  overflow: hidden;
}

.rate-buttons button.selected {
  background: linear-gradient(145deg, #ffd700, #ffbf00);
  color: black;
  box-shadow: inset 0 4px 6px rgba(0, 0, 0, 0.2), inset 0 6px 8px rgba(0, 0, 0, 0.2);
}

.rate-buttons button:hover {
  background: linear-gradient(145deg, #ffd700, #ffbf00);
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2), 0 8px 10px rgba(0, 0, 0, 0.2);
}

.rate-buttons button::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 300%;
  height: 300%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1), transparent);
  transition: all 0.3s;
  transform: translate(-50%, -50%) scale(0);
  z-index: 0;
}

.rate-buttons button:hover::before {
  transform: translate(-50%, -50%) scale(1);
}

.rate-buttons button span {
  position: relative;
  z-index: 1;
}

input[type="number"] {
  width: 100%;
  padding: 10px;
  margin-top: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
}
</style>
