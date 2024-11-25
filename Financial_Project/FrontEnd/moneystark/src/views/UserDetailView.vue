<template>
  <div class="detail-page">
    <div v-if="user" class="user-info">
      <div class="header">
        <h1>회원 정보</h1>
        <button class="delete-button" @click="deleteUser">회원탈퇴</button>
      </div>
      <div class="user-details">
        <p>
          <strong>이름:</strong>
          {{ user.username }}
        </p>
        <p>
          <strong>닉네임:</strong>
          {{ user.nickname }}
        </p>
        <p>
          <strong>성별:</strong>
          {{ user.gender }}
        </p>
        <p>
          <strong>나이:</strong>
          {{ user.age }}
        </p>
        <p>
          <strong>이메일:</strong>
          {{ user.email }}
        </p>
        <p @click="$router.push({ name: 'StyleView' })">
          <strong>칭호:</strong>
          <i :class="getTitleIcon(user.style)"></i>
          {{ user.style }}
        </p>
        <p style="font-weight: lighter">칭호를 눌러보세요!</p>
      </div>

      <div class="action-buttons">
        <button class="modal-button" @click="openDepositsModal">가입한 예금 목록 보기</button>
        <button class="modal-button" @click="openPostsModal">내가 작성한 게시글 보기</button>
        <button class="secondary-button" @click="goToEditProfile">회원 정보 수정</button>
        <button class="secondary-button" @click="$router.push({ name: 'Surveys' })">칭호 생성하기</button>
      </div>
    </div>

    <div v-else class="loading">
      <p>사용자 정보를 불러오는 중...</p>
    </div>

    <!-- 가입한 예금 목록 모달 -->
    <div v-if="showDepositsModal" class="modal-overlay" @click.self="closeDepositsModal">
      <div class="modal-content">
        <h2>가입한 예금 목록</h2>
        <div v-for="deposit in user.deposits" :key="deposit.id" class="deposit-item">
          <p>
            <strong>은행 이름:</strong>
            {{ deposit.deposit_product_kor_co_nm }}
          </p>
          <p>
            <strong>예금 이름:</strong>
            {{ deposit.deposit_product_fin_prdt_nm }}
          </p>
          <p>
            <strong>넣은 금액:</strong>
            {{ deposit.amount }}
          </p>
          <p>
            <strong>시작일:</strong>
            {{ deposit.deposit_product_dcls_strt_day }}
          </p>
          <p>
            <strong>금리:</strong>
            {{ deposit.deposit_product_mtrt_int }}
          </p>
          <hr />
        </div>
        <button class="close-button" @click="closeDepositsModal">닫기</button>
      </div>
    </div>

    <!-- 내가 작성한 게시글 모달 -->
    <div v-if="showPostsModal" class="modal-overlay" @click.self="closePostsModal">
      <div class="modal-content">
        <h2>내가 작성한 게시글</h2>
        <div v-for="post in user.post" :key="post.id" class="post-item">
          <p>
            <strong>게시글 번호:</strong>
            {{ post.id }}
          </p>
          <p>
            <strong>게시글 제목:</strong>
            {{ post.title }}
          </p>
          <p>
            <strong>게시글 내용:</strong>
            {{ post.content }}
          </p>
          <p>
            <strong>작성일:</strong>
            {{ post.created_at }}
          </p>
          <p>
            <strong>좋아요:</strong>
            {{ post.like_count }}
          </p>
          <hr />
        </div>
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
    const titleIcons = {
      "투자 초보": "fas fa-seedling", // 새싹 아이콘
      "무지의 용사": "fas fa-user-shield", // 방패를 든 사용자 아이콘
      "금융 신입": "fas fa-baby", // 아기 아이콘

      "중급 투자자": "fas fa-user-tie", // 넥타이 맨 사용자 아이콘
      "투자 도전자": "fas fa-fist-raised", // 주먹 쥔 손 아이콘
      "금융 중수": "fas fa-graduation-cap", // 졸업 모자 아이콘

      "고급 투자자": "fas fa-chess-knight", // 체스 말 아이콘
      "숙련된 전략가": "fas fa-brain", // 뇌 아이콘
      "금융 마에스트로": "fas fa-magic", // 마법 지팡이 아이콘

      "전설의 투자자": "fas fa-crown", // 왕관 아이콘
      "투자의 마스터": "fas fa-user-secret", // 시크릿 사용자 아이콘
      "엘리트 금융 전문가": "fas fa-gem", // 보석 아이콘
    };
    const getTitleIcon = (title) => {
      return titleIcons[title] || "mdi-account"; // 기본 아이콘 설정
    };

    const userStore = useUserStore();
    const user = ref(null);
    const error = ref(null);
    const router = useRouter();

    // 모달 상태
    const showDepositsModal = ref(false);
    const showPostsModal = ref(false);

    const deleteUser = async () => {
      if (confirm("정말로 회원탈퇴 하시겠습니까?")) {
        await userStore.deleteUser();
        router.push({ name: "home" });
      }
    };

    // 사용자 정보를 가져오는 함수
    const fetchUserData = async () => {
      try {
        await userStore.fetchUser();
        user.value = userStore.user;
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
      deleteUser,
      titleIcons,
      getTitleIcon,
    };
  },
};
</script>

<style scoped>
/* 전체 페이지 스타일 */
.detail-page {
  font-family: "Arial", sans-serif;
  background-color: #f0f2f5;
  padding: 30px;
  max-width: 800px;
  margin: 40px auto;
  border-radius: 10px;
}

/* 로딩 상태 */
.loading {
  text-align: center;
  font-size: 1.2rem;
  color: #555;
}

/* 회원 정보 섹션 */
.user-info {
  background: #fff;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.user-info .header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-info h1 {
  font-size: 2rem;
  color: #333;
}

.user-info .delete-button {
  background-color: #ff4d4f;
  color: #fff;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.user-info .delete-button:hover {
  background-color: #d9363e;
}

.user-details {
  margin-top: 20px;
}

.user-details p {
  font-size: 1.1rem;
  margin-bottom: 12px;
  color: #555;
}

.user-details strong {
  color: #333;
}

.action-buttons {
  margin-top: 30px;
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

/* 버튼 스타일 */
.modal-button,
.secondary-button {
  padding: 12px 20px;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.modal-button {
  background-color: #1890ff;
  color: #fff;
}

.modal-button:hover {
  background-color: #40a9ff;
}

.secondary-button {
  background-color: #52c41a;
  color: #fff;
}

.secondary-button:hover {
  background-color: #73d13d;
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
  padding: 30px;
  border-radius: 10px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.modal-content h2 {
  margin-bottom: 20px;
  font-size: 1.8rem;
  color: #333;
  text-align: center;
}

.modal-content .deposit-item,
.modal-content .post-item {
  margin-bottom: 20px;
}

.modal-content .deposit-item p,
.modal-content .post-item p {
  font-size: 1rem;
  margin-bottom: 8px;
  color: #555;
}

.modal-content strong {
  color: #333;
}

.modal-content hr {
  border: none;
  border-top: 1px solid #e8e8e8;
  margin: 15px 0;
}

.close-button {
  display: block;
  margin: 20px auto 0;
  background-color: #ff7875;
  color: #fff;
  padding: 12px 25px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.close-button:hover {
  background-color: #ff4d4f;
}

/* 반응형 스타일 */
@media (max-width: 768px) {
  .user-info {
    padding: 20px;
  }

  .user-info h1 {
    font-size: 1.5rem;
  }

  .user-details p {
    font-size: 1rem;
  }

  .action-buttons {
    flex-direction: column;
  }

  .modal-content {
    padding: 20px;
  }

  .modal-content h2 {
    font-size: 1.5rem;
  }

  .modal-content .deposit-item p,
  .modal-content .post-item p {
    font-size: 0.9rem;
  }
}
</style>
