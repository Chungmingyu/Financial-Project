<template>
  <div>
    <h2>정기적금 정보</h2>
    <ul>
      <li v-for="saving in productStore.savingProduct" :key="saving.id">
        공시 제출월 [YYYYMM] : {{ saving.dcls_month }} 금융회사 코드 : {{ saving.fin_co_no }} 금융회사 명 : {{ saving.kor_co_nm }} 금융상품 코드 (고유값) : {{ saving.fin_prdt_cd }} 금융 상품명 :
        {{ saving.fin_prdt_nm }} 가입 방법 : {{ saving.join_way }} 만기 후 이자율 : {{ saving.mtrt_int }} 우대조건 : {{ saving.spcl_cnd }} 가입제한 (예: 1:제한없음, 2:서민전용, 3:일부제한) :
        {{ saving.join_deny }} 가입대상 : {{ saving.join_member }} 기타 유의사항 : {{ saving.etc_note }} 최고한도 (기본값: '없음') : {{ saving.max_limit }} 공시 시작일 :
        {{ saving.dcls_strt_day }} 공시 종료일 (기본값: '없음') : {{ saving.dcls_end_day }} 금융회사 제출일 [YYYYMMDDHH24MI]c : {{ saving.fin_co_subm_day }}
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
  productStore.getSavingProduct();
});
</script>

<style scoped>
h2 {
  color: #2c3e50;
}
</style>
