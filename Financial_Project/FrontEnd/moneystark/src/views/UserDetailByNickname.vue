<template>
  <div class="detail-page">
    <div v-if="user" class="user-info">
      <button @click.prevent="$router.push({name:'BoardView'})">뒤로가기</button>
      <br>
      <button>아니 아래 원래 나오는데 배경색때문에 안나오는거임</button>
      <h1>회원 정보</h1>
      <!-- <p><strong>이름:</strong> {{ user.username }}</p> -->
      <p><strong>닉네임:</strong> {{ user.nickname }}</p>
      <!-- <p><strong>성별:</strong> {{ user.gender }}</p> -->
      <!-- <p><strong>나이:</strong> {{ user.age }}</p> -->
      <!-- <p><strong>이메일:</strong> {{ user.email }}</p> -->
      <p><strong>칭호:</strong> {{ user.style }}</p>

      <div v-if="user.deposits" class="deposits-section">
        <hr />
        <button class="modal-button" @click="openDepositsModal">{{ user.nickname}} 이/가 가입한 예금 목록 보기</button>
      </div>

      <div v-if="user.post" class="posts-section">
        <hr />
        <button class="modal-button" @click="openPostsModal">{{ user.nickname}} 이/가 작성한 게시글 보기</button>
      </div>

      <!-- <button class="secondary-button" @click="goToEditProfile">회원 정보 수정</button> -->
    </div>

    <div v-else>
      <p>사용자 정보를 불러오는 중...</p>
    </div>

    <!-- <div>
      <button class="secondary-button" @click="$router.push({ name: 'Surveys' })">칭호 생성하기</button>
    </div> -->

    <!-- 가입한 예금 목록 모달 -->
    <div v-if="showDepositsModal" class="modal-overlay" @click.self="closeDepositsModal">
      <div class="modal-content">
        <h2>{{ user.nickname}} 이/가 가입한 예금 목록</h2>
        <p v-for="deposit in user.deposits" :key="deposit.id">
          <div><strong>은행 이름:</strong> {{ deposit.deposit_product_kor_co_nm }}</div>
          <div><strong>예금 이름:</strong> {{ deposit.deposit_product_fin_prdt_nm }}</div>
          <div><strong>넣은 금액:</strong> {{ deposit.amount }}</div>
          <div><strong>시작일:</strong> {{ deposit.deposit_product_dcls_strt_day }}</div>
          <div><strong>금리:</strong> {{ deposit.deposit_product_mtrt_int }}</div>
        </p>
        <button class="close-button" @click="closeDepositsModal">닫기</button>
      </div>
    </div>

    <!-- 내가 작성한 게시글 모달 -->
    <div v-if="showPostsModal" class="modal-overlay" @click.self="closePostsModal">
      <div class="modal-content">
        <h2>{{ user.nickname}} 이/가 작성한 게시글</h2>
        <p v-for="post in user.post" :key="post.id">
          <div><strong>게시글 번호:</strong> {{ post.id }}</div>
          <div><strong>게시글 제목:</strong> {{ post.title }}</div>
          <div><strong>게시글 내용:</strong> {{ post.content }}</div>
          <div><strong>작성일:</strong> {{ post.created_at }}</div>
          <div><strong>좋아요:</strong> {{ post.like_count }}</div>
        </p>
        <button class="close-button" @click="closePostsModal">닫기</button>
      </div>
    </div>
  </div>
</template>

<script>
import { useUserStore } from "../stores/user";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

export default {
  setup() {
    const userStore = useUserStore(); // Pinia store 인스턴스 가져오기
    const user = ref(null); // 사용자 정보
    const error = ref(null); // 에러 상태 관리
    const router = useRouter(); // 라우터 사용

    // 모달 상태
    const showDepositsModal = ref(false);
    const showPostsModal = ref(false);

    // 사용자 정보를 가져오는 함수
    const fetchUserData = async () => {
      try {
        await userStore.fetchUser(); // 사용자 정보 가져오기
        user.value = userStore.user; // 사용자 정보 저장
      } catch (err) {
        error.value = "사용자 정보를 불러오는 데 실패했습니다.";
        console.error(err);
      }
    };

    // 모달 열기/닫기 함수
    const openDepositsModal = () => {
      showDepositsModal.value = true;
    };
    const closeDepositsModal = () => {
      showDepositsModal.value = false;
    };
    const openPostsModal = () => {
      showPostsModal.value = true;
    };
    const closePostsModal = () => {
      showPostsModal.value = false;
    };

    // 수정 페이지로 이동
    const goToEditProfile = () => {
      router.push({ name: "UserChangeView" });
    };

    // 컴포넌트 마운트 시 사용자 정보 가져오기
    onMounted(fetchUserData);

    return {
      user,
      error,
      goToEditProfile,
      showDepositsModal,
      showPostsModal,
      openDepositsModal,
      closeDepositsModal,
      openPostsModal,
      closePostsModal,
    };
  },
};
</script>

<style scoped>
/* 전체 페이지 스타일 */
.detail-page {
  font-family: 'Arial', sans-serif;
  background-color: #f9f9f9;
  padding: 20px;
  max-width: 800px;
  margin: auto;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* 회원 정보 섹션 */
.user-info {
  background: #fff;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-bottom: 20px;
}
.user-info h1 {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 15px;
}
.user-info p {
  font-size: 1rem;
  margin-bottom: 10px;
  line-height: 1.5;
}
.user-info strong {
  color: #555;
}

/* 예금 및 게시글 섹션 버튼 */
.deposits-section, .posts-section {
  margin: 15px 0;
}
.modal-button {
  padding: 10px 15px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.modal-button:hover {
  background-color: #45a049;
}

/* 추가 버튼 스타일 */
.secondary-button {
  padding: 10px 15px;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.secondary-button:hover {
  background-color: #0056b3;
}

/* 모달 스타일 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  width: 80%;
  max-width: 500px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  text-align: left;
}
.modal-content h2 {
  margin-bottom: 15px;
  font-size: 1.5rem;
  color: #333;
}
.modal-content p {
  margin: 10px 0;
}
.close-button {
  background-color: #d9534f;
  color: white;
  padding: 10px 15px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
}
.close-button:hover {
  background-color: #c9302c;
}
</style>