from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from dj_rest_auth.serializers import UserDetailsSerializer
from .models import User, DepositProduct, SavingProduct


# accounts/serializers.py

# from rest_framework import serializers
from dj_rest_auth.serializers import UserDetailsSerializer
from .models import User
from django.conf import settings
Usermodel = settings.AUTH_USER_MODEL


class UserDepositProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProduct
        fields = '__all__'


class UserSavingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProduct
        fields = '__all__'


class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(required=True, max_length=10)
    gender = serializers.ChoiceField(
        choices=(('M', '남성(Man)'), ('W', '여성(Woman)')), required=True)
    age = serializers.IntegerField(required=True, min_value=0)
    email = serializers.EmailField(required=True, allow_blank=False)

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'nickname': self.validated_data.get('nickname', ''),
            'gender': self.validated_data.get('gender', ''),
            'age': self.validated_data.get('age', -1),
            'email': self.validated_data.get('email', '')
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
        includes the related `DepositProduct` and `SavingProduct` objects.
        """
        # from .serializers import DepositProductSerializer, SavingProductSerializer  # Lazy import

        data = super().to_representation(instance)

        # deposit_fin_prdt_cd와 saving_fin_prdt_cd가 실제로 존재할 때만 해당 정보를 포함시킴
        if instance.deposit_fin_prdt_cd:
            data['deposit_fin_prdt_cd'] = UserDepositProductSerializer(
                instance.deposit_fin_prdt_cd).data
        else:
            data['deposit_fin_prdt_cd'] = None

        if instance.saving_fin_prdt_cd:
            data['saving_fin_prdt_cd'] = UserSavingProductSerializer(
                instance.saving_fin_prdt_cd).data
        else:
            data['saving_fin_prdt_cd'] = None

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
