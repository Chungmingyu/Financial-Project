from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from dj_rest_auth.serializers import UserDetailsSerializer
from .models import User
from moneys.models import DepositProduct, SavingProduct, UserDeposit


# accounts/serializers.py

# from rest_framework import serializers
from dj_rest_auth.serializers import UserDetailsSerializer
from .models import User
from django.conf import settings
Usermodel = settings.AUTH_USER_MODEL


# class BoardSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Board
#         fields = ['id', 'user', 'title', 'content', 'created_at', 'updated_at']
#         read_only_fields = ['user', 'created_at', 'updated_at']


class UserDepositProductSerializer(serializers.ModelSerializer):
    # DepositProduct의 관련 필드들을 UserDeposit 시리얼라이저에 포함
    deposit_product_kor_co_nm = serializers.CharField(
        source='deposit_product.kor_co_nm')
    deposit_product_fin_prdt_nm = serializers.CharField(
        source='deposit_product.fin_prdt_nm')
    deposit_product_mtrt_int = serializers.CharField(
        source='deposit_product.mtrt_int')
    deposit_product_dcls_strt_day = serializers.CharField(
        source='deposit_product.dcls_strt_day')
    deposit_product_dcls_end_day = serializers.CharField(
        source='deposit_product.dcls_end_day')

    class Meta:
        model = UserDeposit
        fields = ['deposit_product_kor_co_nm', 'deposit_product_fin_prdt_nm',
                  'deposit_product_mtrt_int', 'deposit_product_dcls_strt_day',
                  'deposit_product_dcls_end_day', 'amount', 'date_created']


# 유저관련된 시리얼라이저


class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(required=True, max_length=10)
    gender = serializers.ChoiceField(
        choices=(('M', '남성(Man)'), ('W', '여성(Woman)')), required=True)
    age = serializers.IntegerField(required=True, min_value=0)
    email = serializers.EmailField(required=True, allow_blank=False)

    # 예금 관련 필드 추가
    deposit_name = serializers.CharField(
        source='userdeposit.deposit_product.name', read_only=True)
    deposit_interest_rate = serializers.FloatField(
        source='userdeposit.deposit_product.interest_rate', read_only=True)

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'nickname': self.validated_data.get('nickname', ''),
            'gender': self.validated_data.get('gender', ''),
            'age': self.validated_data.get('age', -1),
            'email': self.validated_data.get('email', ''),
            'deposit_name': self.validated_data.get('deposit_name', ''),
            'deposit_interest_rate': self.validated_data.get('deposit_interest_rate', '')
        }

    def save(self, request):
        # 부모 클래스의 save 메서드를 호출하여 사용자 생성
        user = super().save(request)

        # 유효성 검사된 데이터를 사용하여 추가 필드들 저장
        user.nickname = self.validated_data.get('nickname', '')
        user.gender = self.validated_data.get('gender', '')
        user.age = self.validated_data.get('age', -1)
        user.email = self.validated_data.get('email', '')
        user.save()

        return user


class CustomUserDetailsSerializer(UserDetailsSerializer):
    nickname = serializers.CharField()
    gender = serializers.CharField()
    age = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['pk', 'email', 'nickname', 'gender', 'age']
        read_only_fields = ['email', 'pk']

    def to_representation(self, instance):
        """
        This method ensures that the representation of the `User` instance
        includes the related `DepositProduct` objects.
        """
        data = super().to_representation(instance)

        # User 인스턴스에서 관련된 UserDeposit 객체들을 가져오기
        user_deposits = instance.deposits.all()  # User 모델에서 deposits 역참조

        # UserDeposit이 존재하면 시리얼라이즈하여 데이터에 추가
        if user_deposits.exists():
            data['deposits'] = UserDepositProductSerializer(
                user_deposits, many=True).data
        else:
            data['deposits'] = None

        return data


class CustomUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'gender', 'age']

    def update(self, instance, validated_data):
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.age = validated_data.get('age', instance.age)
        instance.save()
        return instance
