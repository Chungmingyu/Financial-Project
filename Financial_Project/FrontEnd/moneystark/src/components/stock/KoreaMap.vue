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
        <g v-for="region in mappedRegions" 
           :key="region.id" 
           :fill="getRegionColor(region.price)" 
           @mousemove="handleMouseMove($event, region)" 
           @mouseleave="hoveredRegion = null" 
           class="region">
          <path :d="region.path" />
          <text :x="region.center?.[0]" 
                :y="region.center?.[1]" 
                class="region-label" 
                stroke="#fff" 
                stroke-width="3" 
                stroke-linejoin="round">
            {{ region.name }}
          </text>
          <text :x="region.center?.[0]" 
                :y="region.center?.[1]" 
                class="region-label region-label-front">
            {{ region.name }}
          </text>
        </g>
      </svg>

      <div v-if="hoveredRegion" class="price-beacon" :style="beaconStyle">
        <div class="beacon-content">
          <h4>{{ hoveredRegion.name }}</h4>
          <p class="price">{{ formatPrice(hoveredRegion.price) }}억원</p>
          <p class="location">{{ hoveredRegion.fullLocation }}</p>
        </div>
      </div>
    </div>

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
      legendColors: ["#e3f2fd", "#90caf9", "#42a5f5", "#1e88e5", "#0d47a1"], // 파란색 계열
    };
  },
  computed: {
    mappedRegions() {
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

      return southKorea.locations.map((region) => {
        const koreanName = REGION_NAMES[region.name] || region.name;
        const matchedData = cityData[koreanName];

        return {
          id: region.id,
          name: koreanName,
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
    beaconStyle() {
      const rect = this.$el.getBoundingClientRect();
      return {
        left: `${this.mousePosition.x - rect.left}px`,
        top: `${this.mousePosition.y - rect.top - 120}px`,
      };
    },
  },
  methods: {
    getRegionColor(price) {
      if (!price || price <= 0) return "#f8fafc"; // 데이터 없는 지역 색상을 약간 더 밝게 조정

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
};
</script>

<style scoped>
.map-container {
  position: relative;
  width: 95%;
  max-width: 1200px;
  margin: 40px auto;
  padding: 30px;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(13, 71, 161, 0.08);
}

.map-title {
  color: #1565c0;
  text-align: center;
  margin-bottom: 30px;
  font-size: 2rem;
  font-weight: 700;
  text-shadow: 1px 1px 2px rgba(13, 71, 161, 0.1);
}

.legend {
  position: absolute;
  right: 30px;
  top: 30px;
  background: rgba(255, 255, 255, 0.95);
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(13, 71, 161, 0.1);
  border: 1px solid #e3f2fd;
  backdrop-filter: blur(8px);
}

.legend-title {
  color: #1565c0;
  font-weight: 700;
  margin-bottom: 12px;
  font-size: 1.1rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
}

.legend-color {
  width: 35px;
  height: 22px;
  border-radius: 6px;
  border: 1px solid rgba(13, 71, 161, 0.1);
  box-shadow: 0 2px 4px rgba(13, 71, 161, 0.05);
}

.region {
  stroke: #ffffff;
  stroke-width: 1.5;
  transition: all 0.3s ease;
  cursor: pointer;
}

.region:hover {
  opacity: 0.9;
  stroke: #1e88e5;
  stroke-width: 2;
  filter: drop-shadow(0 0 10px rgba(13, 71, 161, 0.3));
}

.region-label {
  font-size: 14px;
  text-anchor: middle;
  dominant-baseline: middle;
  fill: #1565c0;
  font-weight: 600;
  pointer-events: none;
}

.price-beacon {
  position: absolute;
  background: rgba(255, 255, 255, 0.98);
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(13, 71, 161, 0.15);
  border: 1px solid #e3f2fd;
  z-index: 1000;
  min-width: 200px;
  backdrop-filter: blur(8px);
  transform: translate(-50%, -100%);
}

.beacon-content h4 {
  color: #1565c0;
  font-size: 1.2rem;
  font-weight: 700;
  margin-bottom: 8px;
}

.beacon-content .price {
  color: #0d47a1;
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 6px;
}

.beacon-content .location {
  color: #1976d2;
  font-size: 0.95rem;
}

.bottom-info {
  margin-top: 20px;
  background: #f8fafc;
  padding: 20px;
  border-radius: 12px;
  border: 1px solid #e3f2fd;
}

.info-content h3 {
  color: #1565c0;
  font-size: 1.4rem;
  font-weight: 700;
  margin-bottom: 10px;
}

.info-details {
  display: flex;
  align-items: baseline;
  gap: 20px;
}

.price-large {
  color: #0d47a1;
  font-size: 1.6rem;
  font-weight: 700;
}

.location-detail {
  color: #1976d2;
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .map-container {
    padding: 20px;
  }
  
  .legend {
    position: static;
    margin-bottom: 20px;
    width: 100%;
  }

  .info-details {
    flex-direction: column;
    gap: 10px;
  }
}
</style>