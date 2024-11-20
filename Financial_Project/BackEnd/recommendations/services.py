import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime
from moneys.models import DepositProduct, SavingProduct


class InvestmentRecommender:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100)
        self.scaler = StandardScaler()

    def prepare_product_features(self, product, option):
        """상품과 옵션에서 특징 추출"""
        features = []
        # 기본 수익률
        features.append(option.intr_rate or 0)
        # 우대 수익률
        features.append(option.intr_rate2 or 0)
        # 저축 기간
        features.append(option.save_trm)
        # 가입 제한 정도
        features.append(product.join_deny or 1)
        return features

    def train_model(self, deposit_products, saving_products):
        """예금과 적금 상품 데이터로 모델 학습"""
        X = []
        y = []

        # 예금 상품 데이터 준비
        for product in deposit_products:
            for option in product.options.all():
                features = self.prepare_product_features(product, option)
                X.append(features)
                # 기본금리와 우대금리가 None인 경우 0으로 대체
                intr_rate = option.intr_rate if option.intr_rate is not None else 0
                intr_rate2 = option.intr_rate2 if option.intr_rate2 is not None else 0
                # 목표 변수: 기본금리와 우대금리의 평균
                y.append((intr_rate + intr_rate2) /
                         2 if intr_rate2 else intr_rate)

        # 적금 상품 데이터 준비
        for product in saving_products:
            for option in product.options.all():
                features = self.prepare_product_features(product, option)
                X.append(features)
                # 기본금리와 우대금리가 None인 경우 0으로 대체
                intr_rate = option.intr_rate if option.intr_rate is not None else 0
                intr_rate2 = option.intr_rate2 if option.intr_rate2 is not None else 0
                y.append((intr_rate + intr_rate2) /
                         2 if intr_rate2 else intr_rate)

        X = np.array(X)
        y = np.array(y)
        # 특징 스케일링
        X_scaled = self.scaler.fit_transform(X)

        # 모델 학습
        self.model.fit(X_scaled, y)

    def generate_investment_plan(self, total_amount, period_months, preferred_banks=None, risk_preference=3):
        deposit_products = DepositProduct.objects.all()
        saving_products = SavingProduct.objects.all()

        if preferred_banks:
            bank_list = preferred_banks.split(',')
            deposit_products = deposit_products.filter(fin_co_no__in=bank_list)
            saving_products = saving_products.filter(fin_co_no__in=bank_list)

        # 투자 기간에 따른 전략 설정
        is_long_term = period_months >= 60  # 5년 이상을 장기 투자로 간주

        deposit_ratio = (6 - risk_preference) / 5
        plan_items = []
        current_month = 0
        available_amount = total_amount
        used_products = set()

        while current_month < period_months:
            deposit_amount = int(available_amount * deposit_ratio)
            saving_amount = int(available_amount * (1 - deposit_ratio))

            # 장기/단기 투자에 따른 추천 개수 조정
            if is_long_term:
                deposit_limit = 1
                saving_limit = 1
                min_investment_period = 24  # 최소 2년
            else:
                deposit_limit = 2
                saving_limit = 1
                min_investment_period = 6   # 최소 6개월

            recommendations = []
            if deposit_amount >= 1000000:
                recommendations.extend(self._get_top_products(
                    products=deposit_products,
                    amount=deposit_amount,
                    remaining_months=period_months - current_month,
                    used_products=used_products,
                    limit=deposit_limit,
                    min_period=min_investment_period,
                    prefer_long_term=is_long_term
                ))

            if saving_amount >= 1000000:
                recommendations.extend(self._get_top_products(
                    products=saving_products,
                    amount=saving_amount,
                    remaining_months=period_months - current_month,
                    used_products=used_products,
                    limit=saving_limit,
                    min_period=min_investment_period,
                    prefer_long_term=is_long_term
                ))

            if not recommendations:
                break

            total_investment = 0
            for rec in recommendations:
                base_amount = available_amount / len(recommendations)
                rounded_amount = round(base_amount / 100000) * 100000

                if rounded_amount < 1000000:
                    continue

                expected_return = self._calculate_expected_return(
                    rounded_amount,
                    rec['option'].intr_rate,
                    rec['option'].intr_rate2,
                    rec['option'].save_trm
                )

                plan_items.append({
                    'product_type': rec['product_type'],
                    'product_id': rec['product'].fin_prdt_cd,
                    'amount': rounded_amount,
                    'start_month': current_month,
                    'period': rec['option'].save_trm,
                    'expected_return': expected_return
                })

                used_products.add(rec['product'].fin_prdt_cd)
                total_investment += rounded_amount

            available_amount -= total_investment
            current_month += max(3, min(item['period']
                                 for item in plan_items[-len(recommendations):]))

            matured_amount = 0
            for item in plan_items:
                if item['start_month'] + item['period'] <= current_month:
                    matured_amount += item['amount'] + item['expected_return']
            available_amount += matured_amount

        return plan_items

    def _get_top_products(self, products, amount, remaining_months, used_products, limit=3, min_period=6, prefer_long_term=False):
        if limit <= 0:
            return []

        recommendations = []

        for product in products:
            if product.fin_prdt_cd in used_products:
                continue

            for option in product.options.all():
                if min_period <= option.save_trm <= remaining_months:
                    features = self.prepare_product_features(product, option)
                    features = np.array([features])
                    scaled_features = self.scaler.transform(features)
                    score = self.model.predict(scaled_features)[0]

                    # 장기 투자 선호도 반영
                    if prefer_long_term:
                        score *= (option.save_trm / 12)  # 기간이 길수록 높은 점수

                    recommendations.append({
                        'product': product,
                        'option': option,
                        'score': score,
                        'product_type': 'deposit' if isinstance(product, DepositProduct) else 'saving',
                        'amount': amount / limit
                    })

        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:limit]

    def _calculate_expected_return(self, amount, intr_rate, intr_rate2, period):
        effective_rate = intr_rate2 if intr_rate2 else intr_rate
        # 단리 계산
        return int(amount * (effective_rate / 100) * (period / 12))
