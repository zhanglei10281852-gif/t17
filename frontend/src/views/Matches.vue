<template>
  <div class="matches-page">
    <a-tabs v-model:activeKey="activeTab">
      <a-tab-pane key="matches" tab="配对成功">
        <div v-if="loading" class="loading-container">
          <a-spin size="large" />
        </div>
        <div v-else-if="matches.length === 0" class="empty-container">
          <a-empty description="暂无配对成功的对象" />
        </div>
        <div v-else class="match-list">
          <a-card
            v-for="item in matches"
            :key="item.id"
            class="match-card card-hover"
          >
            <div class="match-avatar" :class="item.other_user_profile?.gender === 'male' ? 'male' : 'female'">
              {{ item.other_user_profile?.nickname?.charAt(0) || '?' }}
            </div>
            <div class="match-info">
              <h3>{{ item.other_user_profile?.nickname }}</h3>
              <p>{{ item.other_user_profile?.age }}岁 · {{ item.other_user_profile?.city }} · {{ item.other_user_profile?.occupation }}</p>
              <p class="phone">联系方式：{{ item.masked_phone }}</p>
            </div>
            <div class="match-time">
              {{ formatDate(item.created_at) }}
            </div>
          </a-card>
        </div>
      </a-tab-pane>

      <a-tab-pane key="received" tab="谁喜欢我">
        <div v-if="receivedLoading" class="loading-container">
          <a-spin size="large" />
        </div>
        <div v-else-if="receivedLikes.length === 0" class="empty-container">
          <a-empty description="暂时没有人喜欢你" />
        </div>
        <div v-else class="like-list">
          <a-card
            v-for="item in receivedLikes"
            :key="item.id"
            class="like-card card-hover"
          >
            <div class="like-avatar" :class="item.from_user_profile?.gender === 'male' ? 'male' : 'female'">
              {{ item.from_user_profile?.nickname?.charAt(0) || '?' }}
            </div>
            <div class="like-info">
              <h3>{{ item.from_user_profile?.nickname }}</h3>
              <p>{{ item.from_user_profile?.age }}岁 · {{ item.from_user_profile?.city }}</p>
            </div>
            <a-button type="primary" @click="handleLikeBack(item.from_user_id)">
              回心
            </a-button>
          </a-card>
        </div>
      </a-tab-pane>

      <a-tab-pane key="sent" tab="我喜欢的">
        <div v-if="sentLoading" class="loading-container">
          <a-spin size="large" />
        </div>
        <div v-else-if="sentLikes.length === 0" class="empty-container">
          <a-empty description="还没有喜欢的人" />
        </div>
        <div v-else class="like-list">
          <a-card
            v-for="item in sentLikes"
            :key="item.id"
            class="like-card card-hover"
          >
            <div class="like-avatar" :class="item.to_user_profile?.gender === 'male' ? 'male' : 'female'">
              {{ item.to_user_profile?.nickname?.charAt(0) || '?' }}
            </div>
            <div class="like-info">
              <h3>{{ item.to_user_profile?.nickname }}</h3>
              <p>{{ item.to_user_profile?.age }}岁 · {{ item.to_user_profile?.city }}</p>
            </div>
            <a-tag color="orange">等待回应</a-tag>
          </a-card>
        </div>
      </a-tab-pane>
    </a-tabs>

    <a-modal v-model:open="matchModalVisible" title="🎉 配对成功！" @ok="matchModalVisible = false" @cancel="matchModalVisible = false">
      <div class="match-success-content">
        <p>恭喜你们互相心动！</p>
        <p>对方的联系方式已经解锁，快去查看吧~</p>
      </div>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { message } from 'ant-design-vue'
import api from '@/utils/request'
import dayjs from 'dayjs'

const activeTab = ref('matches')
const matches = ref([])
const receivedLikes = ref([])
const sentLikes = ref([])
const loading = ref(false)
const receivedLoading = ref(false)
const sentLoading = ref(false)
const matchModalVisible = ref(false)

function formatDate(date) {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

async function loadMatches() {
  loading.value = true
  try {
    const data = await api.get('/interaction/matches')
    matches.value = data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function loadReceivedLikes() {
  receivedLoading.value = true
  try {
    const data = await api.get('/interaction/likes/received')
    receivedLikes.value = data
  } catch (e) {
    console.error(e)
  } finally {
    receivedLoading.value = false
  }
}

async function loadSentLikes() {
  sentLoading.value = true
  try {
    const data = await api.get('/interaction/likes/sent')
    sentLikes.value = data
  } catch (e) {
    console.error(e)
  } finally {
    sentLoading.value = false
  }
}

async function handleLikeBack(userId) {
  try {
    const data = await api.post(`/interaction/like/${userId}`)
    if (data.is_match) {
      matchModalVisible.value = true
      loadReceivedLikes()
      loadMatches()
    }
  } catch (e) {
    console.error(e)
  }
}

watch(activeTab, (tab) => {
  if (tab === 'matches') loadMatches()
  if (tab === 'received') loadReceivedLikes()
  if (tab === 'sent') loadSentLikes()
})

onMounted(() => {
  loadMatches()
})
</script>

<style scoped>
.matches-page {
  padding: 24px;
  max-width: 1000px;
  margin: 0 auto;
}

.loading-container,
.empty-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}

.match-list,
.like-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.match-card,
.like-card {
  display: flex;
  align-items: center;
  gap: 16px;
}

.match-avatar,
.like-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
  font-weight: bold;
  flex-shrink: 0;
}

.match-avatar.male,
.like-avatar.male {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.match-avatar.female,
.like-avatar.female {
  background: linear-gradient(135deg, #f093fb, #f5576c);
}

.match-info,
.like-info {
  flex: 1;
}

.match-info h3,
.like-info h3 {
  margin: 0 0 4px 0;
  font-size: 18px;
}

.match-info p,
.like-info p {
  margin: 4px 0;
  color: #666;
  font-size: 14px;
}

.phone {
  color: #ff6b6b !important;
  font-weight: bold;
}

.match-time {
  color: #999;
  font-size: 12px;
}

.match-success-content {
  text-align: center;
  padding: 20px 0;
}

.match-success-content p {
  margin: 8px 0;
  font-size: 16px;
}
</style>
