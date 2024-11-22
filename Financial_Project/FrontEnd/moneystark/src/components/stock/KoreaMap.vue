<template>
  <div class="map-container">
    <h2 class="map-title">{{ selectedType }} 가격 현황</h2>

    <div class="legend">
      <div class="legend-title">가격 범위 (억원)</div>
      <div class="legend-scale">
        <div v-for="(color, i) in legendColors" :key="i" class="legend-item">
          <div class="legend-color" :style="{ backgroundColor: color }"></div>
          <span>{{ legendValues[i] }}</span>
        </div>
      </div>
    </div>

    <div class="map-wrapper">
      <svg viewBox="0 0 800 1200" preserveAspectRatio="xMidYMid meet">
        <g v-for="region in mappedRegions" :key="region.id" :fill="getRegionColor(region.price)" @mousemove="handleMouseMove($event, region)" @mouseleave="hoveredRegion = null" class="region">
          <path :d="region.path" />
          <text :x="region.center?.[0]" :y="region.center?.[1]" class="region-label" stroke="#000" stroke-width="2" stroke-linejoin="round">
            {{ region.name }}
          </text>
          <text :x="region.center?.[0]" :y="region.center?.[1]" class="region-label region-label-front">
            {{ region.name }}
          </text>
        </g>
      </svg>

      <!-- 가격 정보 비콘 -->
      <div v-if="hoveredRegion" class="price-beacon" :style="beaconStyle">
        <div class="beacon-content">
          <h4>{{ hoveredRegion.name }}</h4>
          <p class="price">{{ formatPrice(hoveredRegion.price) }}억원</p>
          <p class="location">{{ hoveredRegion.fullLocation }}</p>
        </div>
      </div>
    </div>

    <!-- 하단 정보 표시 -->
    <div v-if="hoveredRegion" class="bottom-info">
      <div class="info-content">
        <h3>{{ hoveredRegion.name }}</h3>
        <div class="info-details">
          <p class="price-large">{{ formatPrice(hoveredRegion.price) }}억원</p>
          <p class="location-detail">{{ hoveredRegion.fullLocation }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import southKorea from "@svg-maps/south-korea";
import { scaleLinear } from "d3-scale";

const REGION_NAMES = {
  Busan: "부산",
  "North Chungcheong": "충북",
  "South Chungcheong": "충남",
  Daegu: "대구",
  Daejeon: "대전",
  Gangwon: "강원",
  Gwangju: "광주",
  Gyeonggi: "경기",
  "North Gyeongsang": "경북",
  "South Gyeongsang": "경남",
  Incheon: "인천",
  Jeju: "제주",
  "North Jeolla": "전북",
  "South Jeolla": "전남",
  Seoul: "서울",
  Sejong: "세종",
  Ulsan: "울산",
};
export default {
  name: "KoreaMap",
  props: {
    data: {
      type: Array,
      required: true,
    },
    selectedType: {
      type: String,
      default: "아파트",
    },
  },
  data() {
    return {
      hoveredRegion: null,
      mousePosition: { x: 0, y: 0 },
    };
  },
  computed: {
    mappedRegions() {
      console.log("원본 데이터:", this.data);
      const cityData = this.data.reduce((acc, item) => {
        const parts = item.location_full?.split(">") || [];
        const mainRegion = parts[0];

        if (parts.length === 1 || (mainRegion === "서울" && parts.length === 2)) {
          if (!acc[mainRegion] || acc[mainRegion].price < item.price) {
            acc[mainRegion] = {
              location: item.location,
              price: item.price,
              fullLocation: item.location_full,
            };
          }
        }
        return acc;
      }, {});
      // 3. 필터링된 시도 데이터 확인
      console.log("필터링된 시도 데이터:", cityData);

      return southKorea.locations.map((region) => {
        // 영문 지역명을 한글로 변환
        const koreanName = REGION_NAMES[region.name] || region.name;

        console.log("매칭 시도:", {
          originalName: region.name,
          koreanName: koreanName,
        });
        // 매칭 데이터 찾기
        const matchedData = cityData[koreanName];

        console.log("매칭 결과:", {
          region: koreanName,
          matchedData: matchedData,
        });

        return {
          id: region.id,
          name: koreanName, // 한글 지역명 사용
          path: region.path,
          price: matchedData ? matchedData.price : 0,
          center: region.center,
          fullLocation: matchedData ? matchedData.fullLocation : koreanName,
        };
      });
    },
    sortedPrices() {
      const prices = this.mappedRegions
        .filter((r) => r.price > 0)
        .map((r) => r.price)
        .sort((a, b) => a - b);
      return prices;
    },
    priceRange() {
      return {
        min: this.sortedPrices[0] || 0,
        max: this.sortedPrices[this.sortedPrices.length - 1] || 0,
      };
    },
    legendColors() {
      return ["#fff5f0", "#fed4c7", "#fc8e7c", "#e73525", "#67000d"];
    },
    legendValues() {
      const prices = this.data.filter((item) => item.price > 0).map((item) => item.price);

      const min = Math.min(...prices);
      const max = Math.max(...prices);
      const step = (max - min) / 4;

      return Array(5)
        .fill()
        .map((_, i) => {
          const value = min + step * i;
          return this.formatPrice(value);
        });
    },
    tooltipStyle() {
      return {
        left: `${this.mousePosition.x + 10}px`,
        top: `${this.mousePosition.y + 10}px`,
      };
    },
  },
  getRegionColor(price) {
    if (!price || price <= 0) return "#cccccc";

    const { min, max } = this.priceRange;
    const normalized = (price - min) / (max - min);
    const colorIndex = Math.min(Math.floor(normalized * this.legendColors.length), this.legendColors.length - 1);

    return this.legendColors[colorIndex];
  },
  beaconStyle() {
    const rect = this.$el.getBoundingClientRect();
    return {
      left: `${this.mousePosition.x - rect.left}px`,
      top: `${this.mousePosition.y - rect.top - 120}px`,
    };
  },

  methods: {
    getRegionColor(price) {
      //   // 6. 색상 계산 과정 확인
      //   console.log("색상 계산:", {
      //     price: price,
      //     priceRange: this.priceRange,
      //     legendColors: this.legendColors,
      //   });
      if (!price || price <= 0) return "#cccccc";

      const { min, max } = this.priceRange;
      const normalized = (price - min) / (max - min);
      const colorIndex = Math.min(Math.floor(normalized * this.legendColors.length), this.legendColors.length - 1);

      return this.legendColors[colorIndex];
    },
    handleMouseMove(event, region) {
      this.mousePosition = {
        x: event.clientX,
        y: event.clientY,
      };
      this.hoveredRegion = region;
    },
    formatPrice(price) {
      if (!price) return "0";
      const billion = (price * 0.0001).toFixed(2);
      return new Intl.NumberFormat("ko-KR").format(billion);
    },
  },
  watch: {
    data: {
      handler(newData) {
        // console.log("Received data:", newData);
      },
      immediate: true,
    },
  },
};
</script>

<style scoped>
.map-container {
  position: relative;
  width: 95%;
  max-width: 1400px;
  min-height: 900px;
  background: #1e1e1e;
  border-radius: 12px;
  padding: 30px;
  margin: 0 auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.map-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: calc(100% - 100px);
  position: relative;
  margin-top: 20px;
}

svg {
  width: 90%;
  height: 90%;
  max-height: 800px;
}

.region-label {
  fill: #fff;
  font-size: 16px;
  font-weight: bold;
  text-anchor: middle;
  pointer-events: none;
  text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000;
}

.region {
  stroke: #444;
  stroke-width: 1;
  transition: all 0.3s;
  cursor: pointer;
}

.region:hover {
  opacity: 0.85;
  stroke: #fff;
  stroke-width: 2;
  filter: drop-shadow(0 0 8px rgba(255, 255, 255, 0.3));
}

.price-beacon {
  position: absolute;
  pointer-events: none;
  transform: translate(-50%, -100%);
  z-index: 1000;
}

.beacon-content {
  background: rgba(0, 0, 0, 0.9);
  padding: 12px 16px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(4px);
}

.beacon-content h4 {
  margin: 0 0 4px;
  color: #fff;
  font-size: 16px;
}

.beacon-content .price {
  margin: 0;
  color: #4caf50;
  font-size: 18px;
  font-weight: bold;
}

.beacon-content .location {
  margin: 4px 0 0;
  color: #aaa;
  font-size: 12px;
}

.bottom-info {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.95);
  padding: 20px;
  border-radius: 0 0 12px 12px;
  backdrop-filter: blur(10px);
}

.info-content {
  max-width: 800px;
  margin: 0 auto;
  color: #fff;
}

.info-content h3 {
  margin: 0 0 10px;
  font-size: 24px;
}

.info-details {
  display: flex;
  align-items: baseline;
  gap: 20px;
}

.price-large {
  margin: 0;
  font-size: 28px;
  font-weight: bold;
  color: #4caf50;
}

.location-detail {
  margin: 0;
  color: #aaa;
  font-size: 16px;
}

.map-title {
  color: #fff;
  text-align: center;
  margin-bottom: 30px;
  font-size: 2em;
  font-weight: bold;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.legend {
  position: absolute;
  right: 40px;
  top: 40px;
  background: rgba(0, 0, 0, 0.95);
  padding: 20px;
  border-radius: 8px;
  color: white;
  z-index: 1000;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.map-title {
  color: #fff;
  text-align: center;
  margin-bottom: 20px;
  font-size: 1.5em;
  font-weight: bold;
}

.legend {
  position: absolute;
  right: 30px;
  top: 30px;
  background: rgba(0, 0, 0, 0.9);
  padding: 15px;
  border-radius: 4px;
  color: white;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.legend-title {
  margin-bottom: 10px;
  font-weight: bold;
  font-size: 14px;
}

.legend-scale {
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-width: 140px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
}

.legend-color {
  width: 30px;
  height: 20px;
  border: 1px solid #444;
  border-radius: 2px;
}

.region-label {
  fill: #fff;
  font-size: 14px;
  text-anchor: middle;
  pointer-events: none;
}

.region-label-front {
  stroke: none;
}

.region {
  stroke: #333;
  stroke-width: 1;
  transition: all 0.3s;
  cursor: pointer;
}

.region:hover {
  opacity: 0.8;
  stroke: #fff;
  stroke-width: 2;
}

.tooltip {
  position: absolute;
  background: rgba(0, 0, 0, 0.9);
  color: white;
  padding: 15px;
  border-radius: 4px;
  font-size: 14px;
  pointer-events: none;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  min-width: 200px;
}

.tooltip h4 {
  margin: 0 0 8px;
  font-size: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding-bottom: 5px;
}

.tooltip-detail {
  font-size: 12px;
  color: #ccc;
  margin-top: 5px;
}
</style>
