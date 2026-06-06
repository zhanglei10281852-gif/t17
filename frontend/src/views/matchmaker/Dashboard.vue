<template>
  <div class="dashboard-page">
    <h2>数据看板</h2>
    
    <a-row :gutter="16" class="stats-row">
      <a-col :span="6">
        <a-card class="stat-card">
          <div class="stat-icon users">👥</div>
          <div class="stat-info">
            <div class="stat-value">{{ statistics?.total_members || 0 }}</div>
            <div class="stat-label">会员总数</div>
          </div>
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card class="stat-card">
          <div class="stat-icon ratio">📊</div>
          <div class="stat-info">
            <div class="stat-value">{{ maleFemaleRatio }}</div>
            <div class="stat-label">男女比</div>
          </div>
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card class="stat-card">
          <div class="stat-icon matches">💕</div>
          <div class="stat-info">
            <div class="stat-value">{{ statistics?.total_matches || 0 }}</div>
            <div class="stat-label">配对成功数</div>
          </div>
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card class="stat-card">
          <div class="stat-icon activities">🎉</div>
          <div class="stat-info">
            <div class="stat-value">{{ statistics?.total_activities || 0 }}</div>
            <div class="stat-label">活动总数</div>
          </div>
        </a-card>
      </a-col>
    </a-row>

    <a-row :gutter="16" class="chart-row">
      <a-col :span="12">
        <a-card title="性别分布">
          <div ref="genderChartRef" style="height: 300px"></div>
        </a-card>
      </a-col>
      <a-col :span="12">
        <a-card title="活动参与率">
          <div ref="activityChartRef" style="height: 300px"></div>
        </a-card>
      </a-col>
    </a-row>

    <a-card title="其他数据" class="other-stats">
      <a-row :gutter="16">
        <a-col :span="8">
          <div class="other-stat">
            <span class="other-stat-value">{{ statistics?.pending_profiles || 0 }}</span>
            <span class="other-stat-label">待审核资料</span>
          </div>
        </a-col>
        <a-col :span="8">
          <div class="other-stat">
            <span class="other-stat-value">{{ statistics?.total_registrations || 0 }}</span>
            <span class="other-stat-label">活动报名人次</span>
          </div>
        </a-col>
        <a-col :span="8">
          <div class="other-stat">
            <span class="other-stat-value">{{ participationPercent }}%</span>
            <span class="other-stat-label">活动参与率</span>
          </div>
        </a-col>
      </a-row>
    </a-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue'
import api from '@/utils/request'
import * as echarts from 'echarts'

const statistics = ref(null)
const genderChartRef = ref(null)
const activityChartRef = ref(null)
let genderChart = null
let activityChart = null

const maleFemaleRatio = computed(() => {
  if (!statistics.value) return '-'
  const { male_count, female_count } = statistics.value
  if (female_count === 0) return '-'
  return `${male_count}:${female_count}`
})

const participationPercent = computed(() => {
  if (!statistics.value) return 0
  return (statistics.value.activity_participation_rate * 100).toFixed(1)
})

async function loadStatistics() {
  try {
    const data = await api.get('/matchmaker/statistics')
    statistics.value = data
    await nextTick()
    initCharts()
  } catch (e) {
    console.error(e)
  }
}

function initCharts() {
  if (genderChartRef.value && statistics.value) {
    genderChart = echarts.init(genderChartRef.value)
    genderChart.setOption({
      tooltip: { trigger: 'item' },
      series: [{
        type: 'pie',
        radius: ['40%', '70%'],
        data: [
          { value: statistics.value.male_count, name: '男', itemStyle: { color: '#667eea' } },
          { value: statistics.value.female_count, name: '女', itemStyle: { color: '#f093fb' } }
        ],
        label: {
          formatter: '{b}: {c}人'
        }
      }]
    })
  }

  if (activityChartRef.value && statistics.value) {
    activityChart = echarts.init(activityChartRef.value)
    activityChart.setOption({
      tooltip: { trigger: 'axis' },
      xAxis: {
        type: 'category',
        data: ['会员参与率']
      },
      yAxis: {
        type: 'value',
        max: 100,
        axisLabel: { formatter: '{value}%' }
      },
      series: [{
        type: 'bar',
        data: [participationPercent.value],
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#667eea' },
            { offset: 1, color: '#764ba2' }
          ])
        },
        barWidth: 60,
        label: {
          show: true,
          position: 'top',
          formatter: '{c}%'
        }
      }]
    })
  }
}

onMounted(() => {
  loadStatistics()
})
</script>

<style scoped>
.dashboard-page {
  padding: 0;
}

.dashboard-page h2 {
  margin-top: 0;
  margin-bottom: 20px;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
}

.stat-icon.users { background: #e8f4fd; }
.stat-icon.ratio { background: #f0f9eb; }
.stat-icon.matches { background: #fef0f0; }
.stat-icon.activities { background: #fdf6ec; }

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.stat-label {
  font-size: 13px;
  color: #999;
  margin-top: 4px;
}

.chart-row {
  margin-bottom: 20px;
}

.other-stats {
  margin-top: 20px;
}

.other-stat {
  text-align: center;
  padding: 20px;
}

.other-stat-value {
  display: block;
  font-size: 28px;
  font-weight: bold;
  color: #ff6b6b;
}

.other-stat-label {
  display: block;
  font-size: 13px;
  color: #999;
  margin-top: 8px;
}
</style>
