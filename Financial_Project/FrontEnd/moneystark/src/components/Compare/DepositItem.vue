<template>
  <div>
    <h2>정기예금 정보</h2>
    <ul>
      <li v-for="deposit in productStore.depositProduct" :key="deposit.id">
        공시 제출월 [YYYYMM] : {{ deposit.dcls_month }} 금융회사 코드 : {{ deposit.fin_co_no }} 금융회사 명 : {{ deposit.kor_co_nm }} 금융상품 코드 (고유값) : {{ deposit.fin_prdt_cd }} 금융 상품명 :
        {{ deposit.fin_prdt_nm }} 가입 방법 : {{ deposit.join_way }} 만기 후 이자율 : {{ deposit.mtrt_int }} 우대조건 : {{ deposit.spcl_cnd }} 가입제한 (예: 1:제한없음, 2:서민전용, 3:일부제한) :
        {{ deposit.join_deny }} 가입대상 : {{ deposit.join_member }} 기타 유의사항 : {{ deposit.etc_note }} 최고한도 (기본값: '없음') : {{ deposit.max_limit }} 공시 시작일 :
        {{ deposit.dcls_strt_day }} 공시 종료일 (기본값: '없음') : {{ deposit.dcls_end_day }} 금융회사 제출일 [YYYYMMDDHH24MI]c : {{ deposit.fin_co_subm_day }}
        <hr />
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useProductStore } from "@/stores/product";

const productStore = useProductStore();

onMounted(() => {
  productStore.getDepositProduct();
});
</script>

<style scoped>
h2 {
  color: #2c3e50;
}
</style>
