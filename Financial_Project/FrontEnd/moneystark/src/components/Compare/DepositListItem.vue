<template>
  <div>
    <h2>정기예금 상세 정보</h2>
    <button @click="$emit('back')">뒤로가기</button>
    <div>
      <p>공시 제출월 [YYYYMM] : {{ deposit.dcls_month }}</p>
      <p>금융회사 코드 : {{ deposit.fin_co_no }}</p>
      <p>금융회사 명 : {{ deposit.kor_co_nm }}</p>
      <p>금융상품 코드 (고유값) : {{ deposit.fin_prdt_cd }}</p>
      <p>금융 상품명 : {{ deposit.fin_prdt_nm }}</p>
      <p>가입 방법 : {{ deposit.join_way }}</p>
      <p>우대조건 : {{ deposit.spcl_cnd }}</p>
      <p>가입제한 : {{ deposit.join_deny }}</p>
      <p>가입대상 : {{ deposit.join_member }}</p>
      <p>기타 유의사항 : {{ deposit.etc_note }}</p>
      <p>최고한도 : {{ deposit.max_limit }}</p>
      <p>공시 시작일 : {{ deposit.dcls_strt_day }}</p>
      <p>공시 종료일 : {{ deposit.dcls_end_day }}</p>
      <p>금융회사 제출일 : {{ deposit.fin_co_subm_day }}</p>
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
import { defineProps } from "vue";

const props = defineProps({
  deposit: Object,
});
</script>

<style scoped>
h2 {
  color: #333;
  text-align: center;
  margin-bottom: 20px;
  font-family: "Arial", sans-serif;
}

div {
  width: 100%; /* 리스트와 동일한 너비로 설정 */
  margin: 0 auto;
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 12px;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

button {
  display: block;
  margin: 20px auto;
  padding: 10px 20px;
  background-color: #333;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
  font-size: 14px;
}

button:hover {
  background-color: #555;
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
</style>
